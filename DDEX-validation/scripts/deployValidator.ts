// We require the Hardhat Runtime Environment explicitly here. This is optional
import fs from "fs";

import { ethers, run } from "hardhat";
import path from "path";

async function main() {
    const operator = "0xA9FDc00274d32FC32e3105c416Ab865DED621a72";
    const router = "0xf9B8fc078197181C841c296C876945aaa425B278";
    const OriginalWorksValidator = await ethers.getContractFactory("OriginalWorksValidator");
    const source = fs.readFileSync(path.resolve("chainlink", "retrieveAndValidateDDEX.js")).toString();
    const subscriptionId = "102";
    const donId = "0x66756e2d626173652d7365706f6c69612d310000000000000000000000000000"; //  ethers.encodeBytes32String("fun-base-sepolia-1");
    const gasLimit = "300000";

    const validator = await OriginalWorksValidator.deploy(
        operator,
        router,
        source,
        subscriptionId,
        donId,
        gasLimit
    );
    console.log("verifying deployment of Original works validator");
    await validator.waitForDeployment();
    const validatorAddress = await validator.getAddress();
    console.log(`Original works validator  deployed at : ${validatorAddress}`);

    // console.log(`verification of contract  Original works validator`);
    // await run("verify:verify", {
    //     address: validatorAddress,
    //     constructorArguments: [
    //         operator,
    //         router,
    //         source,
    //         subscriptionId,
    //         ethers.encodeBytes32String(donId),
    //         gasLimit,
    //     ],
    // });
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
