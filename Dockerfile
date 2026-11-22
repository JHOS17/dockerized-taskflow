FROM python:3.15-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /install && \
    /install/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.15-slim AS runtime

WORKDIR /app

RUN groupadd -g 1001 taskflow && \
    useradd -u 1001 \
    --gid taskflow \
    --shell /usr/sbin/nologin \
    taskflow

COPY --from=builder --chown=taskflow:taskflow /install /install

ENV PATH="/install/bin:$PATH"

COPY --chown=taskflow:taskflow ./app ./app

USER taskflow:taskflow

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]