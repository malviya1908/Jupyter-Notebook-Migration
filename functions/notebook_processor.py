import os
import pandas as pd
import nbformat
from .notebook_metadata import get_notebook_metadata
from .kernel_migration import migrate_kernel_in_memory
from .gcs_upload import upload_notebook_to_gcs
# from .config_reader import read_config

# # Read JSON config
# config = read_config()
# LOCAL_NOTEBOOK_DIR = config["LOCAL_NOTEBOOK_DIR"]
# BUCKET_NAME = config["BUCKET_NAME"]
# SERVICE_ACCOUNT_FILE = config["SERVICE_ACCOUNT_FILE"]
# TARGET_KERNEL_VERSION = config["TARGET_KERNEL_VERSION"]
# OUTPUT_CSV = config["OUTPUT_CSV"]

def process_all_notebooks(config):
    """
    Walk through all notebooks, migrate kernel, collect metadata,
    upload to GCS, and save a report CSV.
    """

    LOCAL_NOTEBOOK_DIR = config["LOCAL_NOTEBOOK_DIR"]
    BUCKET_NAME = config["BUCKET_NAME"]
    SERVICE_ACCOUNT_FILE = config["SERVICE_ACCOUNT_FILE"]
    TARGET_KERNEL_VERSION = config["TARGET_KERNEL_VERSION"]
    OUTPUT_CSV = config["OUTPUT_CSV"]

    all_metadata = []
    folder_counter = 0
    total_files = 0

    for root, _, files in os.walk(LOCAL_NOTEBOOK_DIR):
        if ".ipynb_checkpoints" in root:
            continue

        folder_counter += 1
        print(f"\n[{folder_counter}] Processing folder: {root}")

        file_counter = 0
        for file in files:
            if file.endswith(".ipynb") :
                file_counter += 1
                total_files += 1
                local_path = os.path.join(root, file)

                print(f"   [{folder_counter}.{file_counter}] Processing file: {file} (Total processed: {total_files})")

                # Original notebook metadata
                nb_original = nbformat.read(local_path, as_version=4)
                original_metadata = get_notebook_metadata(local_path, nb_original)

                # Migrate kernel
                nb_migrated = migrate_kernel_in_memory(local_path, TARGET_KERNEL_VERSION)
                migrated_metadata = get_notebook_metadata(local_path, nb_migrated)

                # Merge metadata
                record = {
                    "owner" : original_metadata["owner"],
                    "file_creation_time" : original_metadata["creation_time"],
                    "full_path": local_path,
                    "size_bytes": original_metadata["size_bytes"],
                    "kernel_name": original_metadata["kernel_name"],
                    "original_kernel_version": original_metadata["kernel_version"],
                    "migrated_kernel_version": migrated_metadata["kernel_version"],
                    "file_extension": original_metadata["file_extension"],
                    "total_cells": original_metadata["total_cells"],
                    "times_executed": original_metadata["times_executed"],
                    "last_execution_count": original_metadata["last_execution_count"],
                }
                all_metadata.append(record)

                # Upload to GCS
                rel_path = os.path.relpath(local_path, LOCAL_NOTEBOOK_DIR)
                upload_notebook_to_gcs(nb_migrated, BUCKET_NAME, rel_path, SERVICE_ACCOUNT_FILE)

    # Save DataFrame
    df = pd.DataFrame(all_metadata)
    print("\n Migration Summary:")
    print(df.head())

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n Metadata report saved at: {OUTPUT_CSV}")

    # Final summary
    print(f"\n Total folders processed: {folder_counter}")
    print(f"Total notebooks processed/migrated: {total_files}")

    return df


