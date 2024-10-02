use std::error::Error;
use std::fmt;

#[derive(Debug)]
pub enum OwValidatorNodeError {
    BlockNotFound(u64),
    BlockNotFoundInLog(),
    QueueHeadNotFound(),
    FailedToFindBlobSidecar(String),
}

impl fmt::Display for OwValidatorNodeError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::BlockNotFound(block_no) => {
                write!(
                    f,
                    "Could not fetch the block info for block no: {}",
                    block_no
                )
            }
            Self::BlockNotFoundInLog() => {
                write!(f, "Failed to extract block number from log")
            }
            Self::QueueHeadNotFound() => {
                write!(f, "Details about the queue head could not be found")
            }
            Self::FailedToFindBlobSidecar(commitment) => {
                write!(
                    f,
                    "Failed to find BlobSidecar in the beacon chain for the commitment: {}",
                    commitment
                )
            }
        }
    }
}

impl Error for OwValidatorNodeError {}
