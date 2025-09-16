import os
from datetime import datetime
import getpass

def get_notebook_metadata(local_path, nb):
    """
    Extracts metadata about the notebook file.
    """
    file_stats = os.stat(local_path)

    # Kernel info
    kernel_name = nb.metadata.get("kernelspec", {}).get("name", "N/A")
    kernel_version = nb.metadata.get("language_info", {}).get("version", "N/A")

    # File extension
    file_extension = os.path.splitext(local_path)[1]

    # Cell info
    total_cells = len(nb.cells)
    execution_counts = [
        cell.get("execution_count") for cell in nb.cells if cell.get("execution_count") is not None
    ]
    times_executed = len(execution_counts)
    last_execution = max(execution_counts) if execution_counts else None

    # File creation time
    creation_time = datetime.fromtimestamp(file_stats.st_ctime)

    # File owner
    owner = getpass.getuser()

    return {
        "full_path": local_path,
        "size_bytes": file_stats.st_size,
        "kernel_name": kernel_name,
        "kernel_version": kernel_version,
        "file_extension": file_extension,
        "total_cells": total_cells,
        "times_executed": times_executed,
        "last_execution_count": last_execution,
        "owner": owner,
        "creation_time": creation_time
    }
