use std::error::Error;
use std::fmt;

#[derive(Debug)]
pub enum OwDataProviderCliError {
    MissingEnvVar(String),
    MissingCliArg(String),
    InvalidBlobProof(),
}

impl fmt::Display for OwDataProviderCliError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::MissingEnvVar(var_name) => {
                write!(f, "Missing variable in .env file: {}", var_name)
            }
            Self::MissingCliArg(arg_name) => {
                write!(f, "Missing command line argument: {}", arg_name)
            }
            Self::InvalidBlobProof() => {
                write!(f, "c_kzg error during proof validation")
            }
        }
    }
}

impl Error for OwDataProviderCliError {}
