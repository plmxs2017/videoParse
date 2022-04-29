from shutil import rmtree

def del_file(temp_dir):
    rmtree(rf'{temp_dir}', ignore_errors=True)