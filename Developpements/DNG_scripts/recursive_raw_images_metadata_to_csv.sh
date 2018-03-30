#!/bin/bash
# @Author: Charles-Eric BENAIS-HUGOT, 27/03/2018


directory_raws="/home/guru/STAGE/CODES/Developpements/DNG_scripts/DATABAZ" # directory containing raw databases directories
logfile="${0##*/}.log" # the script name .log
echo $(date '+%d-%m-%Y %H:%M:%S') >> $logfile


metadata_to_csv () {

	csv_filename=""
	regex="([^:]*):(.*)"

	shopt -s globstar
	for filename in $directory_raws/**/*; do # iterate over given dir
		
		if [[ -d $filename ]]; then
			csv_filename="metadata_${filename##*/}.csv"
			echo "File name,File size,MIME type,\
Image size,Camera make,Camera model,\
Image timestamp,Image number,Exposure time,\
Aperture,Exposure bias,Flash,\
Flash bias,Focal length,Subject distance,\
ISO speed,Exposure mode,Metering mode,\
Macro mode,Image quality,Exif Resolution,\
White balance,Thumbnail,Copyright,Exif comment" > $csv_filename
			continue
		fi

		metadata=`exiv2 --print summary "$filename" 2>> $logfile` # print dng metadata with exiv2 tool, redirect errors to logfile
		
		formatted_lines=""

		while read -r line; do # iterate over each line of printed metadata
			if [[ $line =~ $regex ]]; then # disjoin between ':'
				#read -rd '' tag <<<"${BASH_REMATCH[1]}" # get first match group, trim whitespaces
				read -rd '' val <<<"${BASH_REMATCH[2]}" # get second match group, trim whitespaces

				#echo "$tag -> $val"
				formatted_lines="$formatted_lines,\"$val\"" # quote values because it may contain comma :( note that it also may contain quote...
			else
				echo "$line doesn't match" >&2
			fi
		done <<< "$metadata"

		echo "${formatted_lines:1}" >> $csv_filename # append data without first ','
		
	done
}

progressBar () {
	PID=$!
	BAR='##########'   # this is full bar, mine is 20 chars

	while kill -0 $PID 2> /dev/null; do
		for i in {1..10}; do
			printf "\r${BAR:0:$i}" # print $i chars of $BAR from 0 position
			sleep .1
		done
		echo -ne "\033[1K"
	done
	printf '\n'
}

sTime=`date +%s`
metadata_to_csv 2>> "$logfile" & progressBar
fTime=`date +%s`
rTime=$((fTime-sTime))
echo "Runtime : $rTime seconds ($((rTime / 60)) minutes)"
echo "Check $logfile for errors ;)"
