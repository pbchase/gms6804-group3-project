#!/usr/local/bin/python

# Make file types consistent

import zipfile
import magic
import os
import re
import shutil
import gzip
from StringIO import StringIO


def child_younger_than_parent(parent_file, child_file):
    if os.path.isfile(parent_file) and os.path.isfile(child_file):
        age_of_child_since_parent = os.stat(child_file).st_mtime - os.stat(parent_file).st_mtime
        if age_of_child_since_parent > 0:
            return True
        else:
            return False
    else:
        return False

def extract_one_member_from_zip(zf, member, output_dir, path_to_output_file):
    zf.extract(member, output_dir)
    old_name = (os.path.join(output_dir, member.filename))
    os.rename(old_name, path_to_output_file)
    return("wrote %s from zip" % path_to_output_file)


def extract_zip_to_txt(path_to_input_file, path_to_output_file, output_dir):
    """
    :param path_to_input_file: the zip file we will read
    :param path_to_output_file: the final filename we must write
    :param output_dir: the directory into which the genome*.txt file should be extracted
    :return: an informational string about what we did.
    """
    # extract genome*.txt from the zip file and name it subject_id.txt
    try:
        zf = zipfile.ZipFile(path_to_input_file, 'r')
    except zipfile.BadZipfile:
        return "%s is a bad zip file. Skipping file" % path_to_input_file
    zip_info_list = zf.infolist()
    if len(zip_info_list) == 1:
        member = zip_info_list[0]
        return(extract_one_member_from_zip(zf, member, output_dir, path_to_output_file))
    else:
        for member in zip_info_list:
            if re.search('^genome.*\.txt', member.filename):
                return(extract_one_member_from_zip(zf, member, output_dir, path_to_output_file))
    return("unsure what to do with zip file")


def copy_ascii_to_output(my_file, my_path, output_path):
    new_name = (os.path.join(output_path, my_file + ".txt"))
    shutil.copy(my_path, new_name)
    return("wrote %s from ascii" % new_name)


def extract_gzip_to_txt(path_to_input_file, path_to_output_file, output_dir):
    """
    :param path_to_input_file: the gzip file we will read
    :param input_file: the bare name of the input file
    :param output_dir: the directory into which the file should be extracted
    :return: an informational string about what we did.
    """
    #
    gz_file_name = path_to_output_file + '.gz'
    shutil.copy(path_to_input_file, gz_file_name)
    os.system("gunzip %s" % gz_file_name)
    return("wrote %s from gzip" % path_to_output_file)


input_dir = "23andmedata/raw"
output_dir = "23andmedata/unified"
vcf_dir = "23andmedata/vcf"

input_files = os.listdir(input_dir)
for input_file in input_files:
    input_file_path = os.path.join(input_dir, input_file)
    output_file_path = os.path.join(output_dir, input_file + ".txt")
    vcf_file_path = os.path.join(vcf_dir, input_file + ".vcf")
    if not child_younger_than_parent(input_file_path, output_file_path) \
            and not child_younger_than_parent(input_file_path, vcf_file_path):
        file_format = magic.from_file(input_file_path)
        print "Processing %s" % input_file_path ,
        if re.search("^Zip archive data, at least", file_format):
            print extract_zip_to_txt(input_file_path, output_file_path, output_dir)
        elif file_format == "ASCII text, with CRLF line terminators":
            print copy_ascii_to_output(input_file, input_file_path, output_dir)
        elif re.search("^gzip compressed data", file_format):
            print extract_gzip_to_txt(input_file_path, output_file_path, output_dir)
            if not magic.from_file(output_file_path) == "ASCII English text, with CRLF line terminators":
                os.rename(output_file_path,vcf_file_path)
                print "moving %s to %s" % (output_file_path,vcf_file_path)
        elif re.search("^Variant Call Format", file_format):
            os.rename(input_file_path,vcf_file_path)
            print "moving %s to %s" % (input_file_path,vcf_file_path)
        else:
            print "%s is %s" % (input_file_path, file_format)

