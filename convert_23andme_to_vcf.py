#!/usr/local/bin/python3

import os
import re
import csv

class Log:
    def __init__(self, output_file=''):
        self.output = csv.writer(open(output_file, 'a'), delimiter=',')

    def write_header(self):
        header_row = ['subject','attribute','value']
        self.log(header_row)

    def log(self, line):
        self.output.writerow(line)


def run_vcf_step(base_name_of_file, command):
    exit_status = os.WEXITSTATUS(os.system(command))
    if exit_status > 0:
        mylog.log([base_name_of_file, "indexed_vcf_available", "False"])
        return (exit_status)
    else:
        return (0)


def convert_23andme_to_vcf(filename, input_dir, output_dir):
    print(' '.join([filename, input_dir, output_dir]))
    input_file = os.path.join(input_dir, filename)
    base_name_of_file = re.match('(.*).txt', filename).group(1)
    name_of_vcf_file = os.path.join(output_dir, base_name_of_file + ".vcf")
    name_of_compressed_vcf_file = os.path.join(output_dir, base_name_of_file + ".vcf.gz")
    name_of_vcf_index_file = os.path.join(output_dir, base_name_of_file + ".vcf.gz")
    if not os.path.isfile(name_of_compressed_vcf_file):
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


txt_dir = "23andmedata/txt"
compressed_and_indexed_vcf_dir = "23andmedata/unified"
# convert everything to 23andMe text files
# convert every 23andme text file to compress and indexed vcf

conversion_log = "conversion_log_to_indexed_vcf.csv"
mylog = Log(conversion_log)

input_files = os.listdir(txt_dir)
for filename in input_files:
    if re.search('.txt$', filename):
        convert_23andme_to_vcf(filename, txt_dir, compressed_and_indexed_vcf_dir)

