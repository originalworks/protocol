FROM node:16.18-buster

ARG UID=1000
ARG GID=1000

WORKDIR /tmp

RUN \
    groupmod -g "${GID}" node && \
    usermod -u "${UID}" -g "${GID}" node && \
    mkdir -p /app && \
    chown -R node:node /app /home/node && \
    npm install -g bun@1.0.26 snarkjs@0.7.4

USER node

RUN \
    curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y && \ 
    . "$HOME/.cargo/env" && . ~/.bashrc && \
    git clone https://github.com/iden3/circom.git --branch v2.1.9 --depth 1 && \
    cd circom && \
    cargo build --release && \
    cargo install --path circom

WORKDIR /app
