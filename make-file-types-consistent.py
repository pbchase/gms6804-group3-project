#!/usr/local/bin/python

# Make file types consistent

import zipfile
import magic
import os
import re
import shutil
import gzip
from StringIO import StringIO
import csv


class Log:
    def __init__(self, output_file=''):
        self.output = csv.writer(open(output_file, 'a'), delimiter=',')

    def log(self, line):
        self.output.writerow(line)


def child_younger_than_parent(parent_file, child_file):
    if os.path.isfile(parent_file) and os.path.isfile(child_file):
        age_of_child_since_parent = os.stat(child_file).st_mtime - os.stat(parent_file).st_mtime
        if age_of_child_since_parent > 0:
            return True
        else:
            return False
    else:
        return False

def extract_one_member_from_zip(zf, member, output_dir, path_to_output_file, input_file):
    zf.extract(member, output_dir)
    old_name = (os.path.join(output_dir, member.filename))
    os.rename(old_name, path_to_output_file)
    mylog.log([input_file, "member_name", member.filename])
    return("wrote %s from zip" % path_to_output_file)


def extract_zip_to_txt(input_file, path_to_input_file, path_to_output_file, output_dir):
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
        mylog.log([input_file, "archive_content", "archive_is_bad"])
        return "%s is a bad zip file. Skipping file" % path_to_input_file
    zip_info_list = zf.infolist()
    mylog.log([input_file, "archive_member_count", len(zip_info_list)])
    # extract file from one-member zip files
    if len(zip_info_list) == 1:
        member = zip_info_list[0]
        mylog.log([input_file, "archive_content", "single_member"])
        if re.search('^genome.*\.txt', member.filename):
            mylog.log([input_file, "archive_content", "name_is_genome_mumble_txt"])
        return(extract_one_member_from_zip(zf, member, output_dir, path_to_output_file, input_file))

    # extract a very common name for 23andMe files
    for member in zip_info_list:
        if re.search('^genome.*\.txt', member.filename):
            mylog.log([input_file, "archive_content", "name_is_genome_mumble_txt"])
            return(extract_one_member_from_zip(zf, member, output_dir, path_to_output_file, input_file))

    # extract the single file not in a __MACOSX dir
    member_count = len(zip_info_list)
    for member in zip_info_list:
        if re.search('^__MACOSX', member.filename):
            member_count -= 1
        if member_count == 1:
            mylog.log([input_file, "archive_content", "archive_has_macosx_artifacts"])
            return(extract_one_member_from_zip(zf, member, output_dir, path_to_output_file, input_file))

    mylog.log([input_file, "archive_content", "unsure_what_to_do_with_content"])
    return("unsure what to do with zip file")


def is_adna_file(input_file):
    """
    Search for an Ancestry DNA header line in input_file
    """
    with open(input_file, 'r') as inF:
        for line in inF:
            if '#AncestryDNA raw data download' in line:
                return True
    return False


def copy_ascii_to_output(my_file, my_path, output_path):
    new_name = (os.path.join(output_path, my_file + ".txt"))
    shutil.copy(my_path, new_name)
    return("wrote %s from ascii to %s" % (new_name, output_path))


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


def convert_raw_input_to_txt_or_vcf(input_dir, txt_dir, vcf_dir, adna_dir):
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        input_file_path = os.path.join(input_dir, input_file)
        output_file_path = os.path.join(txt_dir, input_file + ".txt")
        vcf_file_path = os.path.join(vcf_dir, input_file + ".vcf")
        adna_file_path = os.path.join(adna_dir, input_file + ".txt")
        if not child_younger_than_parent(input_file_path, output_file_path) \
                and not child_younger_than_parent(input_file_path, vcf_file_path) \
                and not child_younger_than_parent(input_file_path, adna_file_path):
            file_format = magic.from_file(input_file_path)
            mylog.log([input_file, "actual_file_type_from_magic_number", file_format])
            print "Processing %s" % input_file_path ,
            if re.search("^Zip archive data, at least", file_format):
                print extract_zip_to_txt(input_file, input_file_path, output_file_path, txt_dir)
                mylog.log([input_file, "download_type", "archive"])
            elif file_format == "ASCII text, with CRLF line terminators":
                if is_adna_file(input_file_path):
                    print copy_ascii_to_output(input_file, input_file_path, adna_dir)
                    mylog.log([input_file, "download_type", "text"])
                    mylog.log([input_file, "text_file_subtype", "AncestryDNA"])
                else:
                    print copy_ascii_to_output(input_file, input_file_path, txt_dir)
                    mylog.log([input_file, "download_type", "text"])
                    mylog.log([input_file, "text_file_subtype", "23andMe"])
            elif re.search("^gzip compressed data", file_format):
                print extract_gzip_to_txt(input_file_path, output_file_path, txt_dir)
                mylog.log([input_file, "download_type", "archive"])
                magic_number = magic.from_file(output_file_path)
                mylog.log([input_file, "member_type_from_magic_number", file_format])
                print "file type of %s is %s" % (output_file_path, magic_number)
                if not re.search('ASCII (English |)text, with CRLF line terminators', magic.from_file(output_file_path)):
                    os.rename(output_file_path,vcf_file_path)
                    mylog.log([input_file, "text_file_subtype", "vcf"])
                    print "moving %s to %s" % (output_file_path,vcf_file_path)
                else:
                    mylog.log([input_file, "text_file_subtype", "23andMe"])

            elif re.search("^Variant Call Format", file_format):
                os.rename(input_file_path,vcf_file_path)
                print "moving %s to %s" % (input_file_path,vcf_file_path)
                mylog.log([input_file, "download_type", "text"])
                mylog.log([input_file, "text_file_subtype", "vcf"])
            else:
                print "%s is %s" % (input_file_path, file_format)
                mylog.log([input_file, "download_type", "other"])


def convert_23andme_to_vcf(filename, input_dir, output_dir):
    print ' '.join([filename, input_dir, output_dir])
    input_file = os.path.join(input_dir, filename)
    base_name_of_file = re.match('(.*).txt', filename).group(1)
    name_of_vcf_file = os.path.join(output_dir, base_name_of_file + ".vcf")
    name_of_compressed_vcf_file = os.path.join(output_dir, base_name_of_file + ".vcf.gz")
    name_of_vcf_index_file = os.path.join(output_dir, base_name_of_file + ".vcf.gz")
    if not child_younger_than_parent(input_file, name_of_compressed_vcf_file) \
            and not child_younger_than_parent(name_of_compressed_vcf_file, name_of_vcf_index_file):
        output_file_parameter_for_plink = os.path.join(output_dir, base_name_of_file)
        os.system("./plink --23file %s --snps-only just-acgt --recode vcf --out %s" %
            (input_file, output_file_parameter_for_plink))
        os.system("cat %s | bgzip > %s" %
            (name_of_vcf_file, name_of_compressed_vcf_file))
        os.unlink(name_of_vcf_file)
        os.system("tabix -f -p vcf %s" % name_of_compressed_vcf_file)
        mylog.log([base_name_of_file, "indexed_vcf_available", "True"])


input_dir = "23andmedata/raw"
txt_dir = "23andmedata/txt"
vcf_dir = "23andmedata/vcf"
adna_txt = "adna/txt"

conversion_log = "conversion_log.csv"
mylog = Log(conversion_log)

convert_raw_input_to_txt_or_vcf(input_dir, txt_dir, vcf_dir, adna_txt)


compressed_and_indexed_vcf_dir = "23andmedata/unified"
# convert everything to 23andMe text files
# convert every 23andme text file to compress and indexed vcf

input_files = os.listdir(txt_dir)
for filename in input_files:
    if re.search('.txt$', filename):
        convert_23andme_to_vcf(filename, txt_dir, compressed_and_indexed_vcf_dir)

