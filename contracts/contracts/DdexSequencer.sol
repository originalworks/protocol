// SPDX-License-Identifier: MIT
import "hardhat/console.sol";
import "./Whitelist/WhitelistConsumer.sol";
import "./IStakeVault.sol";

pragma solidity ^0.8.24;

contract DdexSequencer is WhitelistConsumer {
    event NewBlobSubmitted(bytes commitment);
    enum BlobStatus {
        NO_EXIST,
        SUBMITTED
    }

    struct Blob {
        bytes32 nextBlob;
        BlobStatus status;
        address proposer;
    }

    bytes1 public constant DATA_PROVIDERS_WHITELIST = 0x01;
    bytes1 public constant VALIDATORS_WHITELIST = 0x02;

    bytes32 public blobQueueHead;
    bytes32 public currentBlob;

    IStakeVault stakeVault;
    mapping(bytes32 => Blob) public blobs;

    constructor(
        address dataProvidersWhitelist,
        address validatorsWhitelist,
        address stakeVaultAddress
    ) {
        _setWhitelistAddress(dataProvidersWhitelist, DATA_PROVIDERS_WHITELIST);
        _setWhitelistAddress(validatorsWhitelist, VALIDATORS_WHITELIST);
        stakeVault = IStakeVault(stakeVaultAddress);
    }

    function submitNewBlob(
        bytes memory commitment
    ) public isWhitelistedOn(DATA_PROVIDERS_WHITELIST) {
        bytes32 newBlobhash;
        assembly {
            newBlobhash := blobhash(0)
        }
        require(newBlobhash != bytes32(0), "Blob not found in tx");
        require(
            blobs[newBlobhash].status == BlobStatus.NO_EXIST,
            "Blob already submitted"
        );

        blobs[newBlobhash].status = BlobStatus.SUBMITTED;
        blobs[newBlobhash].proposer = msg.sender;

        blobs[blobQueueHead].nextBlob = newBlobhash;
        blobQueueHead = newBlobhash;
        emit NewBlobSubmitted(commitment);
    }

    function submitProofOfProcessing(
        bool proof
    ) external isWhitelistedOn(VALIDATORS_WHITELIST) {
        bool isValid = proof; // TODO: implement actual logic of checking the proof

        require(isValid, "Invalid proof");

        _deleteCurrentBlob();
    }

    function submitProofForFraudulentBlob(
        bool proof
    ) external isWhitelistedOn(VALIDATORS_WHITELIST) {
        bool isValid = proof; // TODO: implement actual logic of checking the proof

        require(isValid, "Invalid proof");

        stakeVault.slashStake(blobs[currentBlob].proposer);

        _deleteCurrentBlob();
    }

    function _deleteCurrentBlob() private {
        bytes32 newCurrentBlob = blobs[currentBlob].nextBlob;
        blobs[currentBlob].status = BlobStatus.NO_EXIST;
        blobs[currentBlob].nextBlob = bytes32(0);
        blobs[currentBlob].proposer = address(0);
        currentBlob = newCurrentBlob;
    }
}
