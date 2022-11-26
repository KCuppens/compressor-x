def get_compressed_file_path(initial_file_obj):
    """
    Get the path of the initial file
    """
    return initial_file_obj.file.name.replace("initial_files", "compressed_files")
