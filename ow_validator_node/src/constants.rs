use alloy::primitives::{address, Address, FixedBytes};

pub const DDEX_SEQUENCER_ADDRESS: Address = address!("B965D10739e19a9158e7f713720B0145D996E370");
pub const GET_BEACON_BLOCK_API_PATH: &str = "/eth/v2/beacon/blocks/";
pub const GET_SIDECARS_API_PATH: &str = "/eth/v1/beacon/blob_sidecars/";
pub const EMPTY_QUEUE_HEAD: FixedBytes<32> = FixedBytes::repeat_byte(0);
