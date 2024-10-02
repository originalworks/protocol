mod beacon_chain;
mod constants;
mod ddex_sequencer;
mod errors;

use alloy::providers::ProviderBuilder;
use std::env;
use std::error::Error;
pub struct Config {
    pub rpc_url: String,
    pub beacon_rpc_url: String,
    pub ws_url: String,
    pub start_block: u64,
}

impl Config {
    fn get_env_var(key: &str) -> Result<String, Box<dyn Error>> {
        env::var(key).map_err(|err| {
            format!("Error getting environment variable `{}`: {:?}", key, err).into()
        })
    }

    pub fn build() -> Result<Config, Box<dyn Error>> {
        let rpc_url = Config::get_env_var("RPC_URL")?;
        let beacon_rpc_url = Config::get_env_var("BEACON_RPC_URL")?;
        let ws_url = Config::get_env_var("WS_URL")?;
        let start_block = Config::get_env_var("START_BLOCK")?.parse::<u64>()?;

        Ok(Config {
            rpc_url,
            beacon_rpc_url,
            ws_url,
            start_block,
        })
    }
}

pub async fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let provider =
        ProviderBuilder::new().on_http(config.rpc_url.parse().expect("RPC_URL parsing error:"));
    let ddex_sequencer_context = ddex_sequencer::DdexSequencerContext::build(&provider).await?;

    let queue_head_data = ddex_sequencer_context.get_queue_head_data(&config).await?;

    let blob = beacon_chain::find_blob(
        &config.beacon_rpc_url,
        queue_head_data.commitment,
        queue_head_data.parent_beacon_block_root,
    )
    .await?;

    println!("Blob found for the queue head in the DdexSequencer contract: {blob}");
    Ok(())
}
