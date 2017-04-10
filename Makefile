
dummy:
	@echo "Read the Makefile for info on what to do"

download:
	./download-pgp-hms-data.py

clean:
	rm adna/txt/hu* 23andmedata/txt/*  23andmedata/unknown/* conversion_log.csv temp/*

clean_vcf:
	rm 23andmedata/vcf/*

convert_download_to_text:
	./make-file-types-consistent.py

convert_text_to_indexed_vcf:
	./convert_23andme_to_vcf.py

combine_conversion_logs:
	cat conversion_log.csv conversion_log_to_indexed_vcf.csv > combined_conversion_log.csv

query_text_files_for_rs4149056:
	echo "subject	rsid	chromosome	position	genotype" >rs4149056_v2.txt
	ls -1 23andmedata/txt/hu* | xargs -i grep rs4149056 {} /dev/null | sed -e "s#23andmedata/txt/##; s/.txt:/\t/;" >>rs4149056_v2.txt

query_vcf_files_for_rs4149056:
	./query_vcf_by_snp_id.py > rs4149056_v3_from_vcf.tsv

