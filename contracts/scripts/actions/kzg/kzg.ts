import fs from "fs";
import {
  BYTES_PER_BLOB,
  Blob,
  Bytes48,
  blobToKzgCommitment,
  computeBlobKzgProof,
  loadTrustedSetup,
  verifyBlobKzgProof,
} from "c-kzg";
import { KzgOutput } from "../blobs/types";
import { ethers } from "hardhat";

export class KzgHelper {
  constructor() {
    loadTrustedSetup(0);
  }

  static blobhashFromCommitment(commitment: Uint8Array): string {
    return `0x01${ethers.sha256(commitment).slice(4)}`;
  }

  generate(filePath: string): KzgOutput {
    const file: Blob = fs.readFileSync(filePath);
    let fileHexString = "";

    for (let i = 0; i < file.buffer.byteLength; i++) {
      fileHexString = fileHexString + file.at(i)?.toString(16);
    }

    const blobFile = Buffer.alloc(BYTES_PER_BLOB, fileHexString);
    const commitment = blobToKzgCommitment(blobFile);
    const proof: Bytes48 = computeBlobKzgProof(blobFile, commitment);
    verifyBlobKzgProof(blobFile, commitment, proof);

    return { proof, commitment, blobFile, blobFileHexString: fileHexString };
  }
}
