import os
from pathlib import Path

from scylla_arms.configparser import properties_parser, build_metadata_parser

cur_dir = Path(__file__).parent.resolve()


def test_read_properties():
    assert os.path.exists(f"{cur_dir}/sample_file/general.properties")
    general_p = properties_parser(f"{cur_dir}/sample_file/general.properties")
    build_metadata_file = general_p.get("buildMetadataFile")
    assert build_metadata_file == "00-Build.txt"
    assert os.path.exists(f"{cur_dir}/sample_file/branch-specific.properties")
    branch_p = properties_parser(f"{cur_dir}/sample_file/branch-specific.properties")
    product_name = branch_p.get("productName")
    assert product_name == "scylla"


def test_read_build_metadata():
    assert os.path.exists(f"{cur_dir}/sample_file/00-Build.txt")
    metadata_p = build_metadata_parser(f"{cur_dir}/sample_file/00-Build.txt")
    product = metadata_p.get("scylla-product")
    assert product == "scylla"
    ami_base_os = metadata_p.get("ami-base-os")
    assert ami_base_os == "ubuntu:20.04"


def test_write_properties():
    ami_p = properties_parser("/var/tmp/amiId.properties", new_file=True)
    ami_p.set("scylla_ami_id", "ami-00000000")
    ami_p.commit()
    with open("/var/tmp/amiId.properties") as f:
        prop_txt = f.read()
    assert prop_txt == "scylla_ami_id=ami-00000000\n"
    os.remove("/var/tmp/amiId.properties")


def test_write_build_metadata():
    metadata_p = build_metadata_parser("/var/tmp/00-Build.txt", new_file=True)
    metadata_p.set("scylla-product", "scylla")
    metadata_p.set("ami-base-os", "ubuntu:20.04")
    metadata_p.commit()
    with open("/var/tmp/00-Build.txt") as f:
        prop_txt = f.read()
    assert prop_txt == "scylla-product: scylla\nami-base-os: ubuntu:20.04\n"
    os.remove("/var/tmp/00-Build.txt")


def test_file_not_found_properties():
    try:
        ami_p = properties_parser("/nonexistent.properties")
    except FileNotFoundError:
        pass


def test_file_not_found_build_metadata():
    try:
        metadata_p = build_metadata_parser("/nonexistent.txt")
    except FileNotFoundError:
        pass
