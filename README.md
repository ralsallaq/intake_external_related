# intake_external_related
code related to external intake
The next step after downloading raw fastq data is to intake the fastqs and process them. In order to intake fastqs, two mapping files are usually needed: 

1. a research operation mapping file that maps in-house identifier to one or more fastq identifiers 
2. a mapping file that can map fastqs to the in-house indentifier using fastq identifiers

**create_namemap.py** serves to get the second mapping file. 

```
create_namemap.py -h
usage: create_namemap.py [-h] --res_op_map RES_OP_MAP --data_dir DATA_DIR
                         --out_file OUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  --res_op_map RES_OP_MAP, -i RES_OP_MAP
                        csv file that is provided by Research Operations team
  --data_dir DATA_DIR, -d DATA_DIR
                        a valid email for NCBI server inquiries
  --out_file OUT_FILE, -o OUT_FILE
                        csv file with seqname, tax_id, species_name titles
```

As shown in the help menue above, it requires the first mapping file (input to the **-i** option) in specific format; it must have at least two columns: 

*CompBio ID* and *alt_id1*

optionally it might also have alt_id2, alt_d3, alt_id4 which serve as alternative identifiers for fastqs.
