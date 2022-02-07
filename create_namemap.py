#!/usr/bin/env python 
import numpy as np 
import pandas as pd
import glob
import os
import sys
import argparse



def main():
    """ creates a text file that maps fastqs (first column) to CompBio IDs (second column) 

        INPUT: 

        - a mapping file that maps ComBio IDs to:
          1. alt_id1: the main id used to fetch festqs
          2. alt_id2,...,alt_idk other ids used to identify fastqs
          the format is CompBio ID,alt_id1,alt_id2, ..etc as columns
     
        - a data directory where fastqs to be found: the assumption is that all
          the fastqs to be found are present directly under this directory or inside
          subdirectories within this directory

        OUTPUT:
        namemap.txt which can be used for intake

    """

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--res_op_map','-i', help='csv file that is provided by Research Operations team', required=True)
    args_parser.add_argument('--data_dir','-d', help='a valid email for NCBI server inquiries', required=True)
    args_parser.add_argument('--out_file','-o', help='csv file with seqname, tax_id, species_name titles', required=True)
    args = args_parser.parse_args()

    # First handle the files
    res_op_map = args.res_op_map
    data_dir = args.data_dir
    out_file = args.out_file

 
    fastqFs = glob.glob(data_dir+"/**/*.f*q.gz",recursive = True) + glob.glob(data_dir+"/**/*.f*q",recursive = True)

    fastqs = pd.DataFrame(fastqFs)
    fastqs.columns = ['file']
    fastqs.loc[:,'FASTQ'] = fastqs['file'].apply(lambda r:os.path.basename(r).strip())

    print("found {} FASTQS \n".format(fastqs.shape[0]), file=sys.stderr)

    #### deduplicate
    idx_duplicated = fastqs['FASTQ'].duplicated()

    if fastqs.loc[idx_duplicated].shape[0] > 0 :
        print("found {} duplicated FASTQ files saved in duplicated_removed_fastqs.txt and then removed \n".format(idx_duplicated.sum()), file=sys.stderr)
        fastqs.loc[idx_duplicated].to_csv("duplicated_removed_fastqs.txt", sep="\t", index=False)

        fastqs = fastqs.loc[~idx_duplicated]
        print("{} FASTQS remained after removing duplicates \n".format(fastqs.shape[0]), file=sys.stderr)


    #### sequence operation map file need to have the correct columns
    df_res_op_map = pd.read_csv(res_op_map)

    assert(df_res_op_map.columns.isin(['CompBio ID','alt_id1']).sum()==2),'missing required columns CompBio ID and/or alt_id1'

    assert(df_res_op_map.shape[0]>0), "empty Research Ops mapping file"

    alt_id_cols_idx = df_res_op_map.columns.isin(['alt_id1','alt_id2','alt_id3','alt_id4'])
    alt_id_cols = df_res_op_map.columns[alt_id_cols_idx]

    print("found the following alternative ids in the research operations file: {} \n".format(alt_id_cols.values), file=sys.stderr) 

    
    def getCompBioID(row1):
        for j, row2 in df_res_op_map.iterrows():
            for iid in row2.index.drop('CompBio ID'):
                if row2[iid] in row1['FASTQ']:
                    return row2['CompBio ID']

    fastqs.loc[:,'CompBio ID'] = fastqs.apply(lambda r: getCompBioID(r), axis=1)


    namemap = fastqs.loc[~fastqs['CompBio ID'].isnull(), ['FASTQ','CompBio ID','file']]
    #namemap = fastqs.loc[~fastqs['CompBio ID'].isnull(), ['FASTQ','CompBio ID']]

    namemap = namemap.sort_values(by='FASTQ')

    print("{} fastqs were mapped to CompBio IDs in the namemap.txt file \n".format(namemap.shape[0]))

    namemap.to_csv(out_file, sep="\t", index=False, header=None)



if __name__ == "__main__":

    main()
