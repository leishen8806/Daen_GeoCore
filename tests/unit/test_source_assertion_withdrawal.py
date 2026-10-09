# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportMissingParameterType=false, reportReturnType=false, reportUnusedImport=false

from dataclasses import replace

from daen_geocore.application.source_assertion_withdrawal import (
    WITHDRAW_FACT_TYPE,
    SourceAssertionWithdrawalOutcome,
    WithdrawSourceAssertion,
    WithdrawSourceAssertionCommand,
)
from daen_geocore.domain.references import SourceAssertionRef
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.persistence.records import (
    AssertionHistoryFact,
    AssertionHistoryFactRef,
    OpaqueEncodedPayload,
    StateWitness,
)
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueRequestIdentity,
)
from tests.unit.test_source_assertion_transition import (
    NOW,
    Assertions,
    Candidates,
    Factory,
    FakeTransitionClock,
    Gate,
    _setup,
)


def _command(request: str = "withdraw"):
    return WithdrawSourceAssertionCommand(
        IdempotencyBindingKey(OpaqueClientIdentity("client"), OpaqueRequestIdentity(request)),
        IntentFingerprint("withdraw-source-assertion"),
        SourceAssertionRef("old"),
        OpaqueEncodedPayload("mutation", b"operator"),
    )


def _operation(assertions, committed, audit, evidence=None, candidates=None, clock=None):
    return WithdrawSourceAssertion(
        Factory(assertions, committed, audit),
        Gate(),
        candidates or Candidates(),
        clock or FakeTransitionClock(),
    )


def test_applied_withdrawal_changes_only_history_and_head() -> None:
    old, assertions, committed, audit, _, _, _, candidates, clock, _ = _setup()
    operation = _operation(assertions, committed, audit, candidates=candidates, clock=clock)
    result = operation.execute(_command())
    assert result.value.outcome is SourceAssertionWithdrawalOutcome.APPLIED
    assert assertions.records[old.source_assertion_ref] == old
    assert assertions.history[old.source_assertion_ref][0].fact_type == WITHDRAW_FACT_TYPE
    assert assertions.history[old.source_assertion_ref][0].related_source_assertion_ref is None
    assert assertions.heads[old.source_assertion_ref].state_witness != StateWitness("w1")
    assert candidates.calls == 2 and clock.calls == 1
    assert len(audit.records) == 1 and len(committed.bindings) == 1


def test_already_holds_is_accepted_and_replays_as_already_holds() -> None:
    old, assertions, committed, audit, _, _, _, candidates, clock, _ = _setup()
    assertions.history[old.source_assertion_ref] = [
        AssertionHistoryFact(
            AssertionHistoryFactRef("withdrawn"),
            old.source_assertion_ref,
            WITHDRAW_FACT_TYPE,
            NOW,
            None,
            OpaqueEncodedPayload("mutation", b"old"),
        )
    ]
    operation = _operation(assertions, committed, audit, candidates=candidates, clock=clock)
    command = _command("already")
    result = operation.execute(command)
    assert result.value.outcome is SourceAssertionWithdrawalOutcome.ALREADY_HOLDS
    assert candidates.calls == 0 and len(assertions.history[old.source_assertion_ref]) == 1
    replay = operation.execute(command)
    assert replay.value.outcome is SourceAssertionWithdrawalOutcome.REPLAY
    assert replay.value.replayed_outcome is SourceAssertionWithdrawalOutcome.ALREADY_HOLDS
    assert len(audit.records) == 1 and len(committed.bindings) == 1


def test_applied_replay_precedes_mutable_state() -> None:
    old, assertions, committed, audit, _, _, _, candidates, clock, _ = _setup()
    operation = _operation(assertions, committed, audit, candidates=candidates, clock=clock)
    command = _command()
    first = operation.execute(command)
    assert first.value.outcome is SourceAssertionWithdrawalOutcome.APPLIED
    calls, ticks = candidates.calls, clock.calls
    replay = operation.execute(command)
    assert replay.value.outcome is SourceAssertionWithdrawalOutcome.REPLAY
    assert replay.value.replayed_outcome is SourceAssertionWithdrawalOutcome.APPLIED
    assert candidates.calls == calls and clock.calls == ticks


def test_missing_target_and_head_fail_closed() -> None:
    _, _, committed, audit, _, _, _, candidates, clock, _ = _setup()
    missing = Assertions()
    operation = _operation(missing, committed, audit, candidates=candidates, clock=clock)
    result = operation.execute(_command("missing"))
    assert result.value.outcome is SourceAssertionWithdrawalOutcome.TARGET_ASSERTION_NOT_FOUND
    _, assertions, committed, audit, _, _, _, candidates, clock, _ = _setup()
    assertions.heads.clear()
    result = _operation(assertions, committed, audit, candidates=candidates, clock=clock).execute(
        _command("no-head")
    )
    assert result.value.outcome is SourceAssertionWithdrawalOutcome.TARGET_STANDING_HEAD_MISSING
    assert candidates.calls == 0 and clock.calls == 0


def test_new_request_same_key_different_intent_conflicts() -> None:
    _, assertions, committed, audit, _, _, _, candidates, clock, _ = _setup()
    operation = _operation(assertions, committed, audit, candidates=candidates, clock=clock)
    command = _command("conflict")
    assert operation.execute(command).value.outcome is SourceAssertionWithdrawalOutcome.APPLIED
    conflict = operation.execute(replace(command, intent_fingerprint=IntentFingerprint("other")))
    assert conflict.value.outcome is SourceAssertionWithdrawalOutcome.IDEMPOTENCY_CONFLICT
