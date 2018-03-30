#!/bin/bash
# Naive recursive version assuming there is no spaces in subdirectory names


directory_raws='/home/guru/STAGE/CODES/Developpements/DNG_scripts/DATABAZ' # directory containing files with spaces

shopt -s globstar

for f in $directory_raws/**/*\ *; do mv "$f" "${f// /_}"; done
