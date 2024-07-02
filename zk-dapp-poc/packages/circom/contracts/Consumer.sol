// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

interface IPlonkVerifier {
    function verifyProof(
        uint256[24] calldata _proof,
        uint256[3] calldata _pubSignals
    ) external view returns (bool);
}

contract Consumer {
    address public plonkVerifierAddress;

    event ProofResult(bool result);

    constructor(address _plonkVerifierAddress) {
        plonkVerifierAddress = _plonkVerifierAddress;
    }

    function dateInRange(
        uint256[24] calldata proof,
        uint256[3] calldata pubSignals
    ) public view returns (bool) {
        bool result = IPlonkVerifier(plonkVerifierAddress).verifyProof(
            proof,
            pubSignals
        );
        return result;
    }
}
