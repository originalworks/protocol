const fs = require("fs");
const path = require("path");
const { SubscriptionManager, simulateScript } = require("@chainlink/functions-toolkit");
const ethers = require("ethers");
const { Signer, Provider } = require("@ethersproject/abstract-signer");
require("@chainlink/env-enc").config();
const subscriptionId = 102; // REPLACE this with your subscription ID
const donId = "fun-base-sepolia-1";
const simulateRequest = async () => {
    // hardcoded for base sepolia
    const routerAddress = "0xf9B8fc078197181C841c296C876945aaa425B278";
    const linkTokenAddress = "0xe4ab69c077896252fafbd49efd26b5d171a32410";
    // Initialize functions settings
    const source = fs.readFileSync(path.resolve("chainlink", "retrieveAndValidateDDEX.js")).toString();
    const args = ["Qmbb5Q2fwaFDJKFgmnr2CpCUhRDwkSVwRb4deHCx4rNHy3"];
    const gasLimit = 300000;
    // Initialize ethers signer and provider to interact with the contracts onchain
    const privateKey = process.env.PRIVATE_KEY; // fetch PRIVATE_KEY
    if (!privateKey) throw new Error("private key not provided - check your environment variables");
    const rpcUrl = "https://sepolia.base.org";
    if (!rpcUrl) throw new Error(`rpcUrl not provided  - check your environment variables`);
    const provider = new ethers.JsonRpcProvider(rpcUrl);
    console.log(`provider ${provider._getConnection()}`);
    const signer = new ethers.Wallet(privateKey, provider);
    // const signer = wallet.connect(provider); // create ethers signer for signing transactions
    console.log(`signer ${signer} issigner ${signer._isSigner} is provider ${signer._isProvider}`);
    //console.log(` is signer ${Signer.isSigner(wallet)} is provider ${Provider.isProvider(provider)}`);
    /// ////// START SIMULATION ////////////
    console.log("Start simulation...");
    const response = await simulateScript({
        source: source,
        args: args,
        bytesArgs: [], // bytesArgs - arguments can be encoded off-chain to bytes.
        secrets: {}, // no secrets in this example
    });
    //
    console.log("Simulation result", response);
    /// ///// ESTIMATE REQUEST COSTS ////////
    console.log("\nEstimate request costs...");
    // Initialize and return SubscriptionManager
    const subscriptionManager = new SubscriptionManager({
        signer: signer,
        linkTokenAddress: linkTokenAddress,
        functionsRouterAddress: routerAddress,
    });
    await subscriptionManager.initialize();

    // estimate costs in Juels

    const gasPriceWei = await signer.getGasPrice(); // get gasPrice in wei

    const estimatedCostInJuels = await subscriptionManager.estimateFunctionsRequestCost({
        donId: donId, // ID of the DON to which the Functions request will be sent
        subscriptionId: subscriptionId, // Subscription ID
        callbackGasLimit: gasLimit, // Total gas used by the consumer contract's callback
        gasPriceWei: BigInt(gasPriceWei), // Gas price in gWei
    });

    console.log(`Fulfillment cost estimated to ${ethers.utils.formatEther(estimatedCostInJuels)} LINK`);
};

simulateRequest().catch((e) => {
    console.error(e);
    process.exit(1);
});
