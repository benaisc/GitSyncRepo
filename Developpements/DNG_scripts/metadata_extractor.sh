#!/bin/bash

# http://www.exiv2.org/manpage.html


regex="([^:]*):(.*)"

csv_filename="fiveK_metadata.csv"
echo "File name,File size,MIME type,\
Image size,Camera make,Camera model,\
Image timestamp,Image number,Exposure time,\
Aperture,Exposure bias,Flash,\
Flash bias,Focal length,Subject distance,\
ISO speed,Exposure mode,Metering mode,\
Macro mode,Image quality,Exif Resolution,\
White balance,Thumbnail,Copyright,Exif comment" > $csv_filename

for filename in fiveK_sample/*.*; do # iterate over files in given dir

	metadata=$(exiv2 --print summary $filename) # print dng metadata with exiv2 tool

	formatted_lines=""

	while read -r line; do # itérate over each line of printed metadata
		if [[ $line =~ $regex ]]; then # disjoin @:
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