#!/usr/local/bin/python

# Make file types consistent

import zipfile
import magic
import os
import re
import shutil

def extract_zip_to_txt(my_file, my_path, output_path):
    # extract genome*.txt from the zip file and name it subject_id.txt
    zf = zipfile.ZipFile(my_path,'r')
    zip_info_list = zf.infolist()
    for member in zip_info_list:
        if re.search('^genome.*\.txt', member.filename):
            zf.extract(member,output_path)
            old_name = (os.path.join(output_path, member.filename))
            new_name = (os.path.join(output_path, my_file + ".txt"))
            os.rename(old_name, new_name)
            return("wrote %s from zip" % new_name)


def copy_ascii_to_output(my_file, my_path, output_path):
    new_name = (os.path.join(output_path, my_file + ".txt"))
    shutil.copy(my_path, new_name)
    return("wrote %s from ascii" % new_name)


def crlf_terminators_to_ascii(input_file):
    """
    Convert text

        from: "ASCII English text, with CRLF line terminators"
        to: "ASCII text"

    """

    f = open(input_file, 'rU')

path = "23andmedata/raw"
output_path = "23andmedata/unified"
dirs = os.listdir(path)

for my_file in dirs:
    my_path = os.path.join(path,my_file)
    file_format = magic.from_file(my_path)

    if file_format == "Zip archive data, at least v2.0 to extract":
        extract_zip_to_txt(my_file, my_path, output_path)
    elif file_format == "ASCII text, with CRLF line terminators":
        copy_ascii_to_output(my_file, my_path, output_path)
    else:
        print "%s is %s" % (my_path, file_format)

