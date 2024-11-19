//SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.24;

import "@chainlink/contracts/src/v0.8/functions/v1_0_0/FunctionsClient.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract OriginalWorksValidator is FunctionsClient, Ownable {
    using FunctionsRequest for FunctionsRequest.Request;

    event OriginalWorksValidatorDeployed(address validator);
    event SourceHashUpdated(bytes32 hash);
    event RequestError(bytes32 requestId);
    event RequestProcessed(bytes32 requestId);
    event DDEXValidationPassed(string ipfsId);
    event DDEXValidationFailed(string ipfsId);

    error MalformedData();

    enum RequestStatus {
        NONE,
        REQUESTED,
        COMPLETE,
        ERROR
    }

    mapping (bytes32 => RequestStatus) public requests;
    mapping (bytes32 => string) public requestsToDDEX;
    mapping(string => bool) public validatedDDEX;
    bytes32 public sourceHash;
    bytes32 public donId;
    uint64 public subscriptionId;
    uint32 public gasLimit;

    constructor(
        address operator,
        address router,
        string memory _source,
        uint64 _subscriptionId,
        bytes32 _donId,
        uint32 _gasLimit
    ) FunctionsClient(router) Ownable(operator) {
        require(operator != address(0), "invalid operator");
        require(router != address(0), "invalid router");
        updateFunctionParameter(_source, _subscriptionId, _donId, _gasLimit);
        _transferOwnership(operator);
        emit OriginalWorksValidatorDeployed(address(this));
    }

    function updateSourceHash(string memory _source) public onlyOwner {
        bytes32 _sourceHash = keccak256(abi.encodePacked(_source));
        sourceHash = _sourceHash;
        emit SourceHashUpdated(_sourceHash);
    }

    function updateFunctionParameter(
        string memory _source,
        uint64 _subscriptionId,
        bytes32 _donId,
        uint32 _gasLimit
    ) public onlyOwner {
        require(bytes(_source).length > 0, "invalid source");
        require(_subscriptionId > 0, "invalid subscription id");
        require(_gasLimit > 0, "invalid gas limit");
        require(_donId != bytes32(0), "invalid don id");
        updateSourceHash(_source);
        subscriptionId = _subscriptionId;
        donId = _donId;
        gasLimit = _gasLimit;
    }


    function sendRequest(
        string memory source,
        string memory ipfsId) external onlyOwner returns (bytes32) {

        //TODO: Add source validation
        //bytes32 computedHash = keccak256(abi.encodePacked(source));
        //require( computedHash == sourceHash, "invalid code to execute");

        FunctionsRequest.Request memory req;
        req.initializeRequestForInlineJavaScript(source);
        string[] memory args = new string[](1);
        args[0] = ipfsId;
        req.setArgs(args);
        bytes32 requestId = _sendRequest(
            req.encodeCBOR(),
            subscriptionId,
            gasLimit,
            donId
        );
        requests[requestId] = RequestStatus.REQUESTED;
        requestsToDDEX[requestId] = ipfsId;
        return requestId;
    }

    /**
     * @notice Store latest result/error
     * @param requestId The request ID, returned by sendRequest()
     * @param response Aggregated response from the user code
     * @param err Aggregated error from the user code or from the execution pipeline
     * Either response or error parameter will be set, but never both
     */
    function fulfillRequest(
        bytes32 requestId,
        bytes memory response,
        bytes memory err
    ) internal override {
        require(requests[requestId] == RequestStatus.REQUESTED, "invalid request");
        //check for error
        if (response.length == 0 && err.length != 0) {
            requests[requestId] = RequestStatus.ERROR;
            emit RequestError(requestId);
            return;
        }
        uint result = _readUint256(response, 0); // result should be in first 32 bytes
        string memory ipfsId = requestsToDDEX[requestId];
        if (result == 1) {
            validatedDDEX[ipfsId] = true;
            emit DDEXValidationPassed(ipfsId);
        } else {
            validatedDDEX[ipfsId] = false;
            emit DDEXValidationFailed(ipfsId);
        }

        requests[requestId] = RequestStatus.COMPLETE;
        emit RequestProcessed(requestId);
    }

    function _readUint256(bytes memory data, uint256 offset) internal pure returns (uint256 result) {
        //bounds check
        if (offset + 32 > data.length) revert MalformedData();
        assembly {
        //load 32 byte word accounting for 32 bit length and offset
            result := mload(add(add(data, 32), offset))
        }
    }

}