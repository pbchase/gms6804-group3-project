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


def write_dummy_file(path_to_output_file):
    """
    write an empty file as a place holder
    """
    with open(path_to_output_file, 'w') as inF:
        inF.write("")


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
        write_dummy_file(path_to_output_file)
        return "%s is a bad zip file. Skipping file" % path_to_input_file
    zip_info_list = zf.infolist()
    mylog.log([input_file, "archive_member_count", len(zip_info_list)])
    # extract file from one-member zip files
    if len(zip_info_list) == 1:
        member = zip_info_list[0]
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

    write_dummy_file(path_to_output_file)
    mylog.log([input_file, "archive_content", "unsure_what_to_do_with_content"])
    return("unsure what to do with zip file")


def is_adna_file(input_file):
    """
    Search for an Ancestry DNA header line in input_file
    """
    return(search_file_for_header(input_file, header_line='#AncestryDNA raw data download'))


def is_23andme_file(input_file):
    """
    Search for a 23andMe header line in input_file
    rs3094315       1       742429  AA
    ^rs\d+\s+\d+\s\d+\s+[A-Z]{2}\s*$
    """
    with open(input_file, 'r') as inF:
        for line in inF:

            if re.match("^rs\d+\s+\d+\s\d+\s+[A-Z]{2}\s*$", line) :
                return True
    return False


def is_vcf_file(input_file):
    """
    Search for a VCF header line in input_file
    """
    return(search_file_for_header(input_file, header_line='##fileformat=VCFv'))


def search_file_for_header(input_file, header_line):
    with open(input_file, 'r') as inF:
        for line in inF:
            if header_line in line:
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


def sort_text_file_by_subtype(input_file, input_file_path, txt_dir, vcf_dir, adna_dir, uk_dir):
    mylog.log([input_file, "download_type", "text"])
    if is_adna_file(input_file_path):
        print copy_ascii_to_output(input_file, input_file_path, adna_dir)
        mylog.log([input_file, "text_file_subtype", "AncestryDNA"])
    elif is_23andme_file(input_file_path):
        print copy_ascii_to_output(input_file, input_file_path, txt_dir)
        mylog.log([input_file, "text_file_subtype", "23andMe"])
    elif is_vcf_file(input_file_path):
        print copy_ascii_to_output(input_file, input_file_path, vcf_dir)
        mylog.log([input_file, "text_file_subtype", "vcf"])
    else:
        print copy_ascii_to_output(input_file, input_file_path, uk_dir)
        mylog.log([input_file, "text_file_subtype", "unknown"])


def input_needs_processing(input_file_path, output_file_path, vcf_file_path, adna_file_path, uk_file_path):
    if not child_younger_than_parent(input_file_path, output_file_path) \
        and not child_younger_than_parent(input_file_path, vcf_file_path) \
        and not child_younger_than_parent(input_file_path, adna_file_path) \
        and not child_younger_than_parent(input_file_path, uk_file_path):
        return True
    else:
        return False


def convert_raw_input_to_txt_or_vcf(input_dir, txt_dir, vcf_dir, adna_dir, uk_dir, temp_dir):
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        input_file_path = os.path.join(input_dir, input_file)
        output_file_path = os.path.join(txt_dir, input_file + ".txt")
        temp_archive_output_file_path = os.path.join(temp_dir, input_file)
        vcf_file_path = os.path.join(vcf_dir, input_file + ".vcf")
        adna_file_path = os.path.join(adna_dir, input_file + ".txt")
        uk_file_path = os.path.join(uk_dir, input_file + ".txt")
        if input_needs_processing(input_file_path, output_file_path, vcf_file_path, adna_file_path, uk_file_path):
            file_format = magic.from_file(input_file_path)
            mylog.log([input_file, "actual_file_type_from_magic_number", file_format])
            print "Processing %s" % input_file_path ,
            if re.search("^Zip archive data, at least", file_format):
                print extract_zip_to_txt(input_file, input_file_path, temp_archive_output_file_path, temp_dir)
                mylog.log([input_file, "download_type", "archive"])
                mylog.log([input_file, "member_type_from_magic_number", magic.from_file(temp_archive_output_file_path)])
                sort_text_file_by_subtype(input_file, temp_archive_output_file_path, txt_dir, vcf_dir, adna_dir, uk_dir)
            elif file_format == "ASCII text, with CRLF line terminators":
                sort_text_file_by_subtype(input_file, input_file_path, txt_dir, vcf_dir, adna_dir, uk_dir)
            elif re.search("^gzip compressed data", file_format):
                print extract_gzip_to_txt(input_file_path, temp_archive_output_file_path, temp_dir)
                mylog.log([input_file, "download_type", "archive"])
                mylog.log([input_file, "actual_file_type_from_magic_number", magic.from_file(temp_archive_output_file_path)])
                sort_text_file_by_subtype(input_file, temp_archive_output_file_path, txt_dir, vcf_dir, adna_dir, uk_dir)
            elif re.search("^Variant Call Format", file_format):
                os.rename(input_file_path,vcf_file_path)
                print "moving %s to %s" % (input_file_path,vcf_file_path)
                mylog.log([input_file, "download_type", "text"])
                mylog.log([input_file, "text_file_subtype", "vcf"])
            else:
                print "%s is %s" % (input_file_path, file_format)
                mylog.log([input_file, "download_type", "other"])


def run_vcf_step(base_name_of_file, command):
    exit_status = os.WEXITSTATUS(os.system(command))
    if exit_status > 0:
        mylog.log([base_name_of_file, "indexed_vcf_available", "False"])
        return (exit_status)


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
        exit_status = run_vcf_step(base_name_of_file, "./plink --23file %s --snps-only just-acgt --recode vcf --out %s" % (input_file, output_file_parameter_for_plink))
        if exit_status > 0:
            return (exit_status)
        exit_status = run_vcf_step(base_name_of_file, "cat %s | bgzip > %s" % (name_of_vcf_file, name_of_compressed_vcf_file))
        if exit_status > 0:
            return (exit_status)
        os.unlink(name_of_vcf_file)
        exit_status = run_vcf_step(base_name_of_file, "tabix -f -p vcf %s" % name_of_compressed_vcf_file)
        if exit_status > 0:
            return (exit_status)
        mylog.log([base_name_of_file, "indexed_vcf_available", "True"])


input_dir = "23andmedata/raw"
txt_dir = "23andmedata/txt"
vcf_dir = "23andmedata/vcf"
adna_txt = "adna/txt"
unknown_txt = "23andmedata/unknown"
temp_dir = "temp"

conversion_log = "conversion_log.csv"
mylog = Log(conversion_log)

convert_raw_input_to_txt_or_vcf(input_dir, txt_dir, vcf_dir, adna_txt, unknown_txt, temp_dir)


compressed_and_indexed_vcf_dir = "23andmedata/unified"
# convert everything to 23andMe text files
# convert every 23andme text file to compress and indexed vcf

input_files = os.listdir(txt_dir)
for filename in input_files:
    if re.search('.txt$', filename):
        convert_23andme_to_vcf(filename, txt_dir, compressed_and_indexed_vcf_dir)

