# STAGE 1 - Build
FROM python:3.12-slim AS build

WORKDIR /app
COPY pyproject.toml uv.lock* ./

ARG PROXY
ENV http_proxy=${PROXY}
ENV https_proxy=${PROXY}
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv ~/.local/bin/uv /usr/local/bin && \
    uv sync --frozen --no-dev && \
    uv venv --relocatable .venv


# STAGE 2
FROM python:3.12-slim
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY ./app ./app
EXPOSE 8080
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]