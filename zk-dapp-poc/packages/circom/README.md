# Circom PoC app

## Overview
Purpose of this project is to give a brief overview of how end to end system could look like using Circom to generate/validate proofs.
Stack includes:
    - CLI tools (node & rust) to compile circom circuits & generate code used by web2 backend & web3 backend,
    - NestJS web2 backend app with endpoint to create witness & proof,
    - Hardhat environment to deploy smart contracts,
    - Solidity smart contracts (web3 backend) which verifies proofs onchain

## Installation
1. `$ docker-compose -f docker/docker-compose.circom.yml build`
2. `$ docker-compose -f docker/docker-compose.circom.yml run test-runner bash`
3. Inside container run `$ bun install`

## File generation
Inside container run
1. `bun run circom:compile`
2. `bun run generate:zkey`
3. `bun run generate:verifier`
4. `bun run hardhat:compile`

## Testing
Inside container run `bun run test`