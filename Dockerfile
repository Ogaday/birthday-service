# Base image

FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=true

# Create user and install application run-time dependencies.
RUN addgroup --gid 1000 --system birthday && \
    adduser --uid 1000 --system --no-create-home --ingroup birthday birthday

RUN mkdir -p /opt/birthday-service && \
    chown 1000:1000 /opt/birthday-service

COPY --chown=1000:1000 ./scripts /opt/birthday-service/scripts/

# Builder image

FROM python:3.10 AS builder

RUN mkdir /build && \
    mkdir /install && \
    mkdir /dev_install

WORKDIR /build

RUN pip install -U pip

COPY pyproject.toml setup.cfg /build/

COPY birthday_service /build/birthday_service/

RUN pip install --no-cache-dir --prefix /install .

RUN pip install --no-cache-dir --prefix /dev_install ".[dev]"

# Dev image

FROM base AS dev

WORKDIR /opt/birthday-service

COPY --from=builder /dev_install /usr/local

COPY tests/ /opt/birthday-service/tests/

USER birthday

ENTRYPOINT ["/bin/bash"]

# Prod image

FROM base

WORKDIR /opt/birthday-service

COPY --from=builder /install /usr/local

USER birthday

ENTRYPOINT ["/bin/bash"]

CMD ["./scripts/serve.sh"]
