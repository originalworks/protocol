import { handleIPFSData } from "./subgraph/src/mapping";

const newCids = [
  "QmNewCid1",
  "QmNewCid2",
  "QmNewCid3",
  // Add more CIDs here
];

for (const cid of newCids) {
  handleIPFSData(cid);
}

