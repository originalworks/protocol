use c_kzg::BYTES_PER_BLOB;
use std::error::Error;
use std::fs;
use std::path::Path;
pub mod decoder;
pub mod encoder;
pub mod validator;

fn append_to_blob<'a>(
    kzg_blob: &'a mut [u8; BYTES_PER_BLOB],
    path: &Path,
    cursor: &'a mut usize,
) -> &'a mut [u8; BYTES_PER_BLOB] {
    let compressed_xml = encoder::file_to_vec(path).unwrap();
    if compressed_xml.len() + *cursor > BYTES_PER_BLOB {
        panic!(
            "Not enough space in the BLOB! Overflow at file: {}",
            path.display()
        );
    }
    kzg_blob[*cursor..*cursor + compressed_xml.len()].copy_from_slice(&compressed_xml);
    *cursor += compressed_xml.len();
    kzg_blob
}

pub fn blob_from_dir(path: &str) -> Result<[u8; BYTES_PER_BLOB], Box<dyn Error>> {
    let dir = Path::new(path);
    let mut kzg_blob: [u8; BYTES_PER_BLOB] = [0; BYTES_PER_BLOB];
    let mut blob_cursor = 0;
    if dir.is_dir() {
        let files = fs::read_dir(dir).unwrap();
        let mut empty_folder = true;
        for file_entry in files {
            let path = file_entry.unwrap().path();
            if path.is_file() && path.extension().unwrap().to_str().unwrap() == "xml" {
                validator::validate_xml(&path).unwrap();
                append_to_blob(&mut kzg_blob, &path, &mut blob_cursor);
                empty_folder = false;
            }
        }
        if empty_folder {
            panic!("No xml files at folder {}", dir.display());
        }
    } else {
        panic!("{path} is not a directory");
    }
    Ok(kzg_blob)
}

pub fn blob_from_file(path: &str) -> Result<[u8; BYTES_PER_BLOB], Box<dyn Error>> {
    let path = Path::new(path);
    let mut kzg_blob: [u8; BYTES_PER_BLOB] = [0; BYTES_PER_BLOB];
    let mut blob_cursor = 0;

    if path.is_file() && path.extension().unwrap().to_str().unwrap() == "xml" {
        validator::validate_xml(&path).unwrap();
        append_to_blob(&mut kzg_blob, path, &mut blob_cursor);
    } else {
        panic!("{} is not an xml file", path.display());
    }
    Ok(kzg_blob)
}

#[test]
#[should_panic]
fn panic_for_empty_dir() {
    blob_from_dir("./tests/assets").unwrap();
}

#[test]
#[should_panic]
fn panic_for_non_dir() {
    blob_from_dir("./tests/assets/pierogi").unwrap();
}

#[test]
#[should_panic]
fn panic_for_non_xml_file() {
    blob_from_file("./tests/assets/test.txt").unwrap();
}

#[test]
#[should_panic]
fn panic_for_non_wrong_path() {
    blob_from_file("./tests/kapusta").unwrap();
}

#[test]
fn encode_file_into_blob_from_valid_xml() {
    let blob = blob_from_file("./tests/assets/valid_xml/ERN_example_1.xml").unwrap();

    assert_ne!(blob, [0; BYTES_PER_BLOB]);
}

#[test]
fn encode_dir_files_into_blob() {
    let blob = blob_from_dir("./tests/assets/valid_xml").unwrap();

    assert_ne!(blob, [0; BYTES_PER_BLOB]);
}
