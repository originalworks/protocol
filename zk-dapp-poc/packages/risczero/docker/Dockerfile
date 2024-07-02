FROM node:18.20-bookworm

ARG UID=1000
ARG GID=1000

WORKDIR /tmp

RUN \
    groupmod -g "${GID}" node && \
    usermod -u "${UID}" -g "${GID}" node && \
    mkdir -p /app && \
    chown -R node:node /app /home/node && \
    npm install -g bun@1.0.26

USER node

RUN \
    curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y && \ 
    . "$HOME/.cargo/env" && . ~/.bashrc && \
    cargo install cargo-binstall && \
    cargo binstall cargo-risczero@1.0.0 --no-confirm && \
    cargo risczero install

WORKDIR /app
