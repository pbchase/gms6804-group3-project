# GMS6803 Group 3 Project

The April 2017 class of GMS 6803 was split into groups for class projects. Group 3 was composed of Philip Chase, Caitrin McDonough, Alex Loiacono, and Sheldon Waugh.  This repo describes some of the data acquisition, exploratory data analysis, and cleaning done for that project. It looks at SNP data and microbiome data from the Harvard Medical School Personal Genome Project, ([https://my.pgp-hms.org](https://my.pgp-hms.org)). 

## Requirements

The Python3 scripts require a few libraries. They can be installed with pip3 like this:

```
pip3 install bs4
pip3 install lxml
pip3 install python-magic
pip3 install docopt
```

Download and install `plink` from [https://www.cog-genomics.org/plink2](https://www.cog-genomics.org/plink2)


The scripts require a few directories exist before running.  Create them with 

```
mkdir -p 23andmedata/raw
mkdir -p 23andmedata/txt
mkdir -p 23andmedata/unknown
mkdir -p 23andmedata/vcf
mkdir -p 23andmedata/unified
mkdir -p adna/txt
```

## Using these tools

This data work is executed in separate scripts that reflect the stages of the data exploration. Some of these scripts are prerequisite to the others. The scripts are organized together in a Makefile that provides shortcuts for executing each correctly. 

The commands are best executed in the sequence described here.

Note the analysis was done on a Mac. Many of the commands described here a POSIX or Bash shell commands. These will work just fine on a Linux or Mac computer. If you are a Windows computer you might need to install Gitbash or some whatever modern Bash shell is available in a modern Windows.


### Download

Execute the command `python3 download-pgp-hms-data.py` to download the vcf files from my.pgp-hms.org. As of November 2019, there are 702 files of SNP data in the PGP-HMS collection. Allow about an hour to download them all.


### Convert download to text

The SNP files downloaded above are a mix of file types from 23andMe, Ancestry DNA, and other sources compressed with a mix of compression algorithms. Each downloaded has to be IDed. Compressed files have to be uncompressed. The contents of each uncompressed file have to be IDed as well. Once the file of SNP data in each download is located and IDed, it has to be sorted into the appropriate bucket for later processing. To extract and ID the SNP files run `python3 make-file-types-consistent.py` 


### Convert text to indexed VCF

The 23andMe files need to be converted into VCF to allow them to be processed with the other files. Run `python3 convert_23andme_to_vcf.py` to do the conversion. This step takes about 25 minutes to run.

### Combine conversion logs

The two file conversion steps generate log files to describe what was found in each file and what was done with the contents in each case. These two log files share an `subject,attribute,value` schema which allows them to be combined and analyzed together. To combine the log files run 

```
cat conversion_log.csv conversion_log_to_indexed_vcf.csv > combined_conversion_log.csv
```

### Cleaning the output files

Note that the creation of the log files is somewhat clumsy. To make a good combined log file suitable for analysis, you should erase the contents of the output directories and all of the log files before doing the conversion steps. 

Sorry if this seems tedious, but that's what we have. If the conversion steps didn't run right on the first try, you should really erase all the output and do it all over again or the combined log file is garbage input for the analysis.

This command will do the trick to erase the output:

```
rm adna/txt/hu* 23andmedata/txt/*  23andmedata/unknown/* temp/*
rm combined_conversion_log.csv conversion_log.csv  conversion_log_to_indexed_vcf.csv
rm 23andmedata/vcf/*
```

Then rerun the conversions.


### Analyse the log files

The log file analysis is done in RMarkDown.  Use RStudio to open `gms6804-group3-project.Rproj` and Knit `acquisition_and_cleaning_of_23andme_genomic_data.Rmd`. 

The analysis should make it clear why this code doesn't include the Ancestry DNA data in the output; very subjects submitted genetic data from Ancestry DNA.


### Querying SNP data

This analysis provides two different ways of querying for a SNP. One can query the `txt` files or the `VCF` files. In theory the latter should be faster as indicies are available, but it was not clear how to query those indices. Each method takes about 5 minutes to query the 700-ish files. These methods are implemented in the Makefile as `query_text_files_for_rs4149056`
 and `query_vcf_files_for_rs4149056` and write the output to the files `rs4149056_v2.txt` and `rs4149056_v3_from_vcf.tsv`, respectively


### Querying a SNP of your choosing

`query_vcf_by_snp_id.py` can accept a SNP as a parameter.

```
Usage:
 query_vcf_by_snp_id.py SNP
 query_vcf_by_snp_id.py (-h | --help | --version)
```

You can redirect the output to a file. E.g., to query for a SNP of your choosing, invoke the command like this:

```
./query_vcf_by_snp_id.py rs4149056 > my_snp.tsv
```

## Microbiome data

This repo contains code about the microbiome data as well, but it has not been documented here.
