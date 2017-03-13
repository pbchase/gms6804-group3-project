
dummy:
	@echo "Read the Makefile for info on what to do"

download:
	./download-pgp-hms-data.py

clean:
	rm adna/txt/hu* 23andmedata/txt/*  23andmedata/unknown/* conversion_log.csv temp/*

clean_vcf:
	rm 23andmedata/vcf/*

convert:
	./make-file-types-consistent.py

query_text_files_for_rs4149056:
	echo "subject	rsid	chromosome	position	genotype" >rs4149056_v2.txt
	ls -1 23andmedata/txt/hu* | xargs -i grep rs4149056 {} /dev/null | sed -e "s#23andmedata/txt/##; s/.txt:/\t/;" >>rs4149056_v2.txt

query_vcf_files_for_rs4149056:
	./query_vcf_by_snp_id.py > rs4149056_v3_from_vcf.tsv

