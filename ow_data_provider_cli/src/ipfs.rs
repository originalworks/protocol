use reqwest::{multipart, Body};
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;
use std::{
    error::Error,
    io::{BufReader, BufWriter},
    path::Path,
};
use tokio_util::codec::{BytesCodec, FramedRead};

use crate::constants::{IMAGE_FILE_CID_TAG, IPFS_CIDS_ROOT_TAG, OUTPUT_FILES_DIR};
use crate::{
    constants::{IPFS_API_ADD_FILE, IPFS_API_BASE_URL},
    errors::OwDataProviderCliError,
};

use quick_xml::events::{BytesStart, BytesText, Event};
use quick_xml::Reader;
use quick_xml::Writer;

#[derive(Deserialize, Debug)]
#[allow(non_snake_case)]
struct IpfsResponse {
    Hash: String,
}

struct AttachCidAndSaveInput {
    image_file_cid: String,
    xml_file_path: String,
    output_file_name: String,
}

async fn file_to_multipart_form(file_path: String) -> Result<multipart::Form, Box<dyn Error>> {
    let file = tokio::fs::File::open(file_path).await?;
    let file_stream = FramedRead::new(file, BytesCodec::new());
    let multipart_stream = multipart::Part::stream(Body::wrap_stream(file_stream));
    let multipart_form = multipart::Form::new().part("file", multipart_stream);
    Ok(multipart_form)
}

pub async fn pin_file(file_path: String) -> Result<String, Box<dyn Error>> {
    let multipart_form = file_to_multipart_form(file_path).await?;
    let client = reqwest::Client::new();

    let response = client
        .post(format!("{}{}", IPFS_API_BASE_URL, IPFS_API_ADD_FILE))
        .multipart(multipart_form)
        .send()
        .await?;

    let result = response.json::<IpfsResponse>().await?;

    Ok(result.Hash)
}

async fn attach_cid_and_save(input: AttachCidAndSaveInput) -> Result<(), Box<dyn Error>> {
    let mut buf = Vec::new();

    let file = fs::File::open(&input.xml_file_path)?;
    let reader = BufReader::new(file);
    let mut reader = Reader::from_reader(reader);

    fs::create_dir_all(OUTPUT_FILES_DIR)?;
    let output_file = fs::File::create(format!("{}/{}", OUTPUT_FILES_DIR, input.output_file_name))?;
    let writer = BufWriter::new(output_file);
    let mut writer = Writer::new(writer);

    loop {
        match reader.read_event_into(&mut buf) {
            Ok(Event::Eof) => break,
            Ok(Event::Start(ref e)) => {
                writer.write_event(Event::Start(e.to_owned()))?;
                if e == &BytesStart::new(IPFS_CIDS_ROOT_TAG) {
                    let tag = BytesStart::new(IMAGE_FILE_CID_TAG);
                    writer.write_event(Event::Start(tag.to_owned()))?;
                    writer.write_event(Event::Text(BytesText::new(&input.image_file_cid)))?;
                    writer.write_event(Event::End(tag.to_end()))?;
                }
            }
            Ok(Event::Text(ref e)) => {
                writer.write_event(Event::Text(e.to_owned()))?;
            }
            Ok(Event::End(ref e)) => {
                writer.write_event(Event::End(e.to_owned()))?;
            }

            Err(e) => return Err(Box::new(e)),
            _ => {}
        }
        buf.clear();
    }

    Ok(())
}

async fn process_asset_folder(
    asset_folder_path: PathBuf,
    folder_index: usize,
) -> Result<(), Box<dyn Error>> {
    if asset_folder_path.is_dir() {
        let asset_files = fs::read_dir(asset_folder_path)?;
        let mut xml_file_path = String::new();
        let mut image_file_cid = String::new();
        for asset_file in asset_files {
            let asset_path = asset_file?.path();
            if asset_path.is_dir() == false {
                let kind = infer::get_from_path(&asset_path)?.ok_or_else(|| {
                    Box::new(OwDataProviderCliError::ErrorReadingFile(
                        asset_path.to_string_lossy().to_string(),
                    ))
                })?;
                if kind.mime_type().starts_with("image/") {
                    image_file_cid = pin_file(asset_path.to_string_lossy().to_string()).await?;
                }
                if kind.extension() == "xml" {
                    xml_file_path = asset_path.to_string_lossy().to_string();
                }
            }
        }
        attach_cid_and_save(AttachCidAndSaveInput {
            image_file_cid,
            xml_file_path,
            output_file_name: format!("{}.xml", folder_index),
        })
        .await?;
    }
    Ok(())
}

pub async fn create_output_files(folder_path: &String) -> Result<(), Box<dyn Error>> {
    let root_folder_dir = Path::new(&folder_path);

    if root_folder_dir.is_dir() {
        let asset_folders = fs::read_dir(root_folder_dir)?;

        for (index, asset_folder) in asset_folders.into_iter().enumerate() {
            let asset_folder_path = asset_folder?.path();
            process_asset_folder(asset_folder_path, index).await?;
        }
    } else {
        return Err(Box::new(OwDataProviderCliError::SourcePathIsNotDir(
            root_folder_dir.to_string_lossy().to_string(),
        )));
    }
    Ok(())
}
