FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
COPY README.md ./README.md
RUN uv sync --frozen --no-dev
USER appuser
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "daen_geocore.transport.http.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
