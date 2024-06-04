import { ipfs, json, Bytes, log } from "@graphprotocol/graph-ts";
import { Resource } from "../generated/schema";

const IPFS_GATEWAY_URL = "https://ipfs.original.works/";

export function handleIPFSData(cid: string): void {
  // Fetch the JSON file from a specific IPFS gateway
  let url = IPFS_GATEWAY_URL + cid;
  let response = ipfs.http.get(url);

  if (response.statusCode == 200) {
    let data = Bytes.fromUint8Array(response.body);
    let jsonData = json.fromBytes(data).toObject();
    let id = cid;
    let resource = new Resource(id);

    // Extract data from the JSON file
    if (jsonData) {
      resource.cid = cid;
      resource.version = jsonData.get("Version").toString();
      resource.rightsControllerName = jsonData.get("RightsControllerName").toString();
      resource.signature = jsonData.get("Signature").toString();
      resource.isrc = jsonData.get("ISRC").toString();
      resource.rightsCoverage = jsonData.get("RightsCoverage").toString();
      resource.territory = jsonData.get("Territory").toString();

      let factsheet = jsonData.get("Factsheet").toObject();
      resource.title = factsheet.get("title").toString();
      resource.artist = factsheet.get("artist").toString();
      resource.album = factsheet.get("album").toString();
      resource.releaseDate = factsheet.get("release_date").toString();
      resource.genre = factsheet.get("genre").toString();
      resource.duration = factsheet.get("duration").toString();

      resource.timestamp = jsonData.get("Timestamp").toString();
      resource.tokenContract = jsonData.get("TokenContract").toString();
      resource.blockchain = jsonData.get("Blockchain").toString();

      // Save the entity
      resource.save();
    } else {
      log.error("JSON data is null for CID: {}", [cid]);
    }
  } else {
    log.error("Unable to fetch data from IPFS for CID: {}. Status code: {}", [cid, response.statusCode.toString()]);
  }
}
