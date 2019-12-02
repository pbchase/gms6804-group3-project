#!/usr/local/bin/python3

"""
Usage:
 query_vcf_by_snp_id.py SNP
 query_vcf_by_snp_id.py (-h | --help | --version)

"""

from docopt import docopt
import os
import re

def view_snp_id(snp_id, subject_name, vcf_filename):
    query_output = os.popen("bcftools view -H -i '%%ID=\"%s\"' %s" % (snp_id, vcf_filename)).read().rstrip()
    if len(query_output) > 0:
    	return(subject_name + "\t" + query_output)
    else:
    	return("")


args = docopt(__doc__, version='1.1.0')
snp_id = args['SNP']

compressed_and_indexed_vcf_dir = "23andmedata/unified"

print("SUBJECT\tCHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tFAM001_ID001")
input_files = os.listdir(compressed_and_indexed_vcf_dir)
for filename in input_files:
    if re.search('.vcf.gz$', filename):
        full_path_to_file = os.path.join(compressed_and_indexed_vcf_dir, filename)
        subject_id = re.match('(^.*).vcf.gz', filename).group(1)
        row = view_snp_id(snp_id, subject_id, full_path_to_file)
        if len(row) > 0:
        	print(row)
