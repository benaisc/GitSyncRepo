#!/bin/bash

directory_raws="/home/guru/STAGE/CODES/Developpements/DNG_scripts/DATABAZ/fiveK_sample"

for filename in $directory_raws/*.dng; do # iterate over files in given dir
    exiv2 -M"set Exif.Photo.UserComment mathieu.massaviol@protonmail.com, https://mathieumassaviol.fr" $filename
done
