// We require the Hardhat Runtime Environment explicitly here. This is optional
import fs from "fs";
// but useful for running the script in a standalone fashion through `node <script>`.
//
// When running the script with `npx hardhat run <script>` you'll find the Hardhat
// Runtime Environment's members available in the global scope.
import { ethers } from "hardhat";
import path from "path";
import {OriginalWorksValidator} from "../typechain-types";

async function main() {
    const validatorAddress = "0x46f1f2409d9ff657925703ea86a87eb13a507e37";
    const source = fs.readFileSync(path.resolve("chainlink", "retrieveAndValidateDDEX.js")).toString();
    const ValidatorFactory = await ethers.getContractFactory("OriginalWorksValidator");
    const validatorContract = await ValidatorFactory.attach(validatorAddress);
    const validator = validatorContract as unknown as OriginalWorksValidator;
    console.log(`source is ${source}`);
    const txn = await validator.sendRequest(source, "Qmbb5Q2fwaFDJKFgmnr2CpCUhRDwkSVwRb4deHCx4rNHy3");
    await txn.wait();
    console.log(`finished transaction ${txn.hash}`);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
