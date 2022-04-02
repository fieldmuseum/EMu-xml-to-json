# Cleanup (if any JSON output)
# from https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/

from zipfile import ZipFile
import zipfile, sys
from decouple import config
    
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
        # For python versions <3.7, exclude the new compresslevel option
        if float(sys.version[0:3]) < 3.7:
            with ZipFile(out_zip_file, 'w', compression=zipfile.ZIP_DEFLATED) as zipObj:

                # Add multiple files to the zip
                for inp_file in inp_file_names:
                    zipObj.write(inp_file)
        
        else:
            with ZipFile(out_zip_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=8) as zipObj:

                # Add multiple files to the zip
                for inp_file in inp_file_names:
                    zipObj.write(inp_file)


    except FileNotFoundError as e:
        print(f' *** Exception occurred during zip process - {e}')


if __name__ == '__main__':
    file_compress(inp_file_names="", out_zip_file="out.zip")
