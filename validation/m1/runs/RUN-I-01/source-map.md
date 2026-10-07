# RUN-I-01 — Source and Provenance Map

> VALIDATION FIXTURE — NOT A SPECIFICATION, NOT A DATABASE SCHEMA, NOT AN API CONTRACT.

## Commit anchors

- H acceptance baseline: `afd22cb483d57cd813c17969700b760b55330250`
- I target erratum commit: `13af031692b8f8e57085fc1ccd6c6ab39f2b87d8`
- I input-freeze commit: this controlled commit adding `inputs.md` and `source-map.md`; exact SHA is recorded in the later operator evidence and reviewer packet.

## P20 closure mappings

| Label | Meaning | Frozen source / boundary | Class |
|---|---|---|---|
| `I-PLACE-P20` | Former White Building Place context | `validation/m1/corpus-register.csv` P20 and `validation/m1/corpus-evidence.md` P20 | REAL |
| `PUB-I-P20-DEMOLITION` | Physical demolition assertion | Frozen P20 public demolition/historical-building evidence in corpus evidence | REAL |
| `SYN-I-CLOSE-P20` | Controlled closure action | RUN-I-01 controlled validation action | SYNTHETIC |

## P03 withdrawal mappings

| Label | Meaning | Frozen source / boundary | Class |
|---|---|---|---|
| `I-PLACE-P03` | Raffles Hotel Le Royal Phnom Penh Place context | `validation/m1/corpus-register.csv` P03 and `validation/m1/corpus-evidence.md` P03 | REAL |
| `SYN-I-P03-REF-HIST` | Controlled historical provider/reference fixture | RUN-I-01 inputs; not a real provider ID | SYNTHETIC |
| `SYN-I-WITHDRAW-P03` | Controlled withdrawal action | RUN-I-01 controlled validation action | SYNTHETIC |

All Quality values are `unknown`. P03 operational closure/rebranding is not used as Place closure. P20 redevelopment identity is not decided.
