const ipfsId = args[0];
const url = `https://gateway.pinata.cloud/ipfs/${ipfsId}/`;
const metadataRequest = Functions.makeHttpRequest({
    url: url,
    headers: {
        "Content-Type": "application/json",
    },
});
const metadataResponse = await metadataRequest;
if (metadataResponse.error) {
    console.error(metadataResponse.error);
    throw Error("Request failed");
}
//TODO: validate the response
const validationResult = 1;
var encodedValidationResult = Functions.encodeUint256(Math.floor(validationResult));
var encodedReturnValue = new Uint8Array(encodedValidationResult.length);
encodedReturnValue.set(encodedValidationResult);

return encodedReturnValue;
