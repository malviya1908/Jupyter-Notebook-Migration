import nbformat

def migrate_kernel_in_memory(nb_path, target_version):
    """
    Read a notebook from nb_path and update its kernel version metadata.
    Returns the updated notebook object (in memory).
    """
    nb = nbformat.read(nb_path, as_version=4)

    # Update kernelspec
    if "kernelspec" in nb.metadata:
        nb.metadata["kernelspec"]["display_name"] = f"Python {target_version}"
    else:
        nb.metadata["kernelspec"] = {
            "display_name": f"Python {target_version}",
            "language": "python",
            "name": "python3"
        }

    # Update language_info
    if "language_info" in nb.metadata:
        nb.metadata["language_info"]["version"] = target_version
    else:
        nb.metadata["language_info"] = {"name": "python", "version": target_version}

    return nb