#!/usr/local/bin/python

import os
import re

def view_snp_id(snp_id, subject_name, vcf_filename):
    query_output = os.popen("bcftools view -H -i '%%ID=\"%s\"' %s" % (snp_id, vcf_filename)).read().rstrip()
    return(subject_name + "\t" + query_output)


snp_id = 'rs4149056'
compressed_and_indexed_vcf_dir = "23andmedata/unified"

print "SUBJECT\tCHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tFAM001_ID001"
input_files = os.listdir(compressed_and_indexed_vcf_dir)
for filename in input_files:
    if re.search('.vcf.gz$', filename):
        full_path_to_file = os.path.join(compressed_and_indexed_vcf_dir, filename)
        subject_id = re.match('(^.*).vcf.gz', filename).group(1)
        print view_snp_id(snp_id, subject_id, full_path_to_file)
