# Cleanup (if any JSON output)
# from https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/

from zipfile import ZipFile
    
# Function : file_compress
def file_compress(inp_file_names="", out_zip_file="out.zip"):
    """
    function : file_compress
    args : inp_file_names : list of filenames to be zipped
    out_zip_file : output zip file
    return : none
    assumption : Input file paths and this code are in same directory.
    """

    try:
        with ZipFile(out_zip_file, 'w') as zipObj:

            # Add multiple files to the zip
            for inp_file in inp_file_names:
                zipObj.write(inp_file)

    except FileNotFoundError as e:
        print(f' *** Exception occurred during zip process - {e}')


if __name__ == '__main__':
    file_compress(inp_file_names="", out_zip_file="out.zip")
