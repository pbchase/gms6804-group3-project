#!/usr/local/bin/python

# Make file types consistent

import zipfile
import magic
import os
import re
import shutil
import gzip
from StringIO import StringIO


def extract_zip_to_txt(path_to_input_file, path_to_output_file, output_dir):
    """
    :param path_to_input_file: the zip file we will read
    :param path_to_output_file: the final filename we must write
    :param output_dir: the directory into which the genome*.txt file should be extracted
    :return: an informational string about what we did.
    """
    # extract genome*.txt from the zip file and name it subject_id.txt
    zf = zipfile.ZipFile(path_to_input_file, 'r')
    zip_info_list = zf.infolist()
    for member in zip_info_list:
        if re.search('^genome.*\.txt', member.filename):
            zf.extract(member, output_dir)
            old_name = (os.path.join(output_dir, member.filename))
            os.rename(old_name, path_to_output_file)
            return("wrote %s from zip" % path_to_output_file)


def copy_ascii_to_output(my_file, my_path, output_path):
    new_name = (os.path.join(output_path, my_file + ".txt"))
    shutil.copy(my_path, new_name)
    return("wrote %s from ascii" % new_name)


def extract_gzip_to_txt(path_to_input_file, path_to_output_file):
    """
    :param path_to_input_file: the gzip file we will read
    :param path_to_output_file: the final filename we must write
    :return: an informational string about what we did.
    """
    #
    zf = zipfile.ZipFile(path_to_input_file, 'r')
    zip_info_list = zf.infolist()
    for member in zip_info_list:
        if re.search('^genome.*\.txt', member.filename):
            zf.extract(member, output_dir)
            old_name = (os.path.join(output_dir, member.filename))
            os.rename(old_name, path_to_output_file)
            return("wrote %s from zip" % path_to_output_file)


def crlf_terminators_to_ascii(input_file):
    """
    Convert text

        from: "ASCII English text, with CRLF line terminators"
        to: "ASCII text"

    """

    f = open(input_file, 'rU')

input_dir = "23andmedata/raw"
output_dir = "23andmedata/unified"

input_files = os.listdir(input_dir)
for input_file in input_files:
    output_file = os.path.join(output_dir, input_file + ".txt")
    if not os.path.isfile(output_file):
        input_file_path = os.path.join(input_dir, input_file)
        file_format = magic.from_file(input_file_path)
        if file_format == "Zip archive data, at least v2.0 to extract":
            extract_zip_to_txt(input_file_path, input_file, output_dir)
        elif file_format == "ASCII text, with CRLF line terminators":
            copy_ascii_to_output(input_file, input_file_path, output_dir)
        else:
            print "%s is %s" % (input_file_path, file_format)

