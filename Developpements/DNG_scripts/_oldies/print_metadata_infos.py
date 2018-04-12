# coding: utf-8
# Script containing what is necessary to collect & manipulate CSV metadata extracted from EXIF of RAW images
# Author: Charles-Eric BENAIS-HUGOT, 28/03/2018

import sys, os
import pandas as pd


def usage():
	print("Usage: python {} path/to/data.csv".format(sys.argv[0]))
	print("i.e: python {} $(find . -type f -name \"*.csv\")".format(sys.argv[0]))
	sys.exit()

def print_column_names(df):
    print(list(df.columns.values))

def print_infos(df):
    print("Number of unique models: {}".format(df['Camera model'].nunique()))
    print("List of unique models:\n{}".format(df['Camera model'].unique()))
    print("Value Count:\n{}".format(df['Camera model'].value_counts()))
    print("Number of files: {}".format(df['File name'].nunique()))
	
    # Extract column 'TIFF' from csv, write it to csv file
    #df['NEF'].to_csv('RAISE_all_nef_urls.csv', header=False, index=False, mode='w')


def launch_():
    for metadata_csv in sys.argv[1:]:
        if(os.path.isfile(metadata_csv)):
            print("___ {} ___".format(os.path.basename(metadata_csv)))
            df = pd.read_csv(metadata_csv, index_col=False)
            #print_column_names(df)
            print_infos(df)

        else:
            usage()


launch_() if len(sys.argv) > 1 else usage()
