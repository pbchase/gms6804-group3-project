
dummy:
	@echo "Read the Makefile for info on what to do"

setup:
	mkdir -p 23andmedata/raw
	mkdir -p 23andmedata/txt
	mkdir -p 23andmedata/unknown
	mkdir -p 23andmedata/vcf
	mkdir -p 23andmedata/unified
	mkdir -p adna/txt

download:
	python3 download-pgp-hms-data.py

clean:
	rm adna/txt/hu* 23andmedata/txt/*  23andmedata/unknown/* temp/*
	rm combined_conversion_log.csv conversion_log.csv  conversion_log_to_indexed_vcf.csv

clean_vcf:
	rm 23andmedata/vcf/*

convert_download_to_text:
	python3 make-file-types-consistent.py

convert_text_to_indexed_vcf:
	python3 convert_23andme_to_vcf.py

combine_conversion_logs:
	cat conversion_log.csv conversion_log_to_indexed_vcf.csv > combined_conversion_log.csv

SNP = rs4149056
query_text_files_for_rs4149056: 
	echo "subject	rsid	chromosome	position	genotype" >${SNP}_v2.txt
	ls -1 23andmedata/txt/hu53* | xargs -I {} grep ${SNP} {} /dev/null | sed -e "s#23andmedata/txt/##;" | awk '{gsub(".txt:","\t",$$0); print;}' >>${SNP}_v2.txt

query_vcf_files_for_rs4149056:
	./query_vcf_by_snp_id.py rs4149056 > rs4149056_v3_from_vcf.tsv

