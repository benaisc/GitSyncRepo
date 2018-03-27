#!/bin/bash

# http://www.exiv2.org/manpage.html

# @Author: Charles-Eric BENAIS-HUGOT, 27/03/2018

directory_raws="/media/icar/269f599f-6a72-48fd-b97c-941595d7b39f/Charles/RAW_DATABASE/RAISE_RAW"

regex="([^:]*):(.*)"

csv_filename="metadata_raise.csv"

echo "File name,File size,MIME type,\
Image size,Camera make,Camera model,\
Image timestamp,Image number,Exposure time,\
Aperture,Exposure bias,Flash,\
Flash bias,Focal length,Subject distance,\
ISO speed,Exposure mode,Metering mode,\
Macro mode,Image quality,Exif Resolution,\
White balance,Thumbnail,Copyright,Exif comment" > $csv_filename


for filename in $directory_raws/*.*; do # iterate over files in given dir

	metadata=$(exiv2 --print summary "$filename") # print dng metadata with exiv2 tool
	
	formatted_lines=""

	while read -r line; do # iterate over each line of printed metadata
		if [[ $line =~ $regex ]]; then # disjoin between ':'
			#read -rd '' tag <<<"${BASH_REMATCH[1]}" # get first match group, trim whitespaces
			read -rd '' val <<<"${BASH_REMATCH[2]}" # get second match group, trim whitespaces

			#echo "$tag -> $val"
			formatted_lines="$formatted_lines,$val"
		else
		    echo "$line doesn't match" >&2
		fi
	done <<< "$metadata"

	echo "${formatted_lines:1}" >> $csv_filename # append data without first ','
	
done

echo "Done!"
