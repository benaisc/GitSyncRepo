#!/bin/bash
# @Author: Charles-Eric BENAIS-HUGOT, 27/03/2018


# directory containing raw databases directories
rawDir='/home/guru/STAGE/CODES/Developpements/DNG_scripts/DATABAZ'
if [[ ! -d $rawDir ]]; then
	echo 'WARNING: specified rawDir does not exist.'
	exit
fi

# destination directory containing raw images developped (pgm)
pgmDir='/home/guru/STAGE/CODES/Developpements/DNG_scripts/DEVELOPPED_DATABASE'
if [[ ! -e $pgmDir ]]; then
    # creating developped images directory
    mkdir -p $pgmDir
    echo "$pgmDir created"
else
	echo 'WARNING: pgmDir already exist, resume development ?'
    read -p 'Enter to continue, CTRL+C otherwise: ' uservar
fi


# configuration file used with ufraw
tmpcfg=`mktemp `
echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>
<UFRaw Version='7'>
<WindowMaximized>1</WindowMaximized>
<Interpolation>ppg</Interpolation>
<WB>Camera WB</WB>
<LensfunAuto>no</LensfunAuto>
<BaseLinearCurve Current='yes'></BaseLinearCurve>
<LinearCurve Current='yes'></LinearCurve>
<MatrixInputProfile Current='yes'>Color matrix</MatrixInputProfile>
<sRGBOutputProfile Current='yes'>sRGB</sRGBOutputProfile>
<SystemDisplayProfile Current='yes'>System default</SystemDisplayProfile>
</UFRaw>" > $tmpcfg


shopt -s globstar
current_dir=''
cpt=0
for filename in $rawDir/**/*; do # iterate recursively over given dir

	if [[ -d $filename ]]; then
		current_dir="${filename##*/}"
		echo -e "\n######## Directory: $current_dir ########"
		mkdir -p "$pgmDir/$current_dir"
		cpt=1
		continue
	fi

	i=${filename##*/}
	echo -en "\r\033[K($cpt)... $i"

    # Used to resume a stopped dev
    if [[ -e "$pgmDir/$current_dir/${i%.*}.pgm" ]]; then
        echo " skipped"
        continue
    fi

	#########################
	#    macroProductPGM    #
	#########################
	#Raw Conversion
    ufraw-batch --conf=$tmpcfg $filename --output="/tmp/${i%.*}.ppm" --silent || continue
    #Convertion into PGM and auto orientation to have an oriented image
    convert -auto-orient "/tmp/${i%.*}.ppm" "/tmp/${i%.*}.pgm"

    arg1=`identify "/tmp/${i%.*}.pgm" | cut -d " " -f3-3`
    length=`echo $arg1 | cut -d "x" -f1-1`
    height=`echo $arg1 | cut -d "x" -f2-2`

    if [ "$height" -lt "$length" ] ; then 
		maxSize=`echo $length`
		newLength=`echo $length*256/$height | bc`
		newHeight=256
		newShiftLength=`echo $newLength/2-256/2 |bc`
		newShiftHeight=0
        convert -resize x`echo $newHeight` /tmp/${i%.*}.pgm /tmp/${i%.*}.R.pgm
    
	else
		maxSize=`echo $height`
		newLength=256
		newHeight=`echo $height*256/$length | bc`
		newShiftLength=0
		newShiftHeight=`echo $newHeight/2-256/2 |bc`
		convert -resize `echo $newLength`x /tmp/${i%.*}.pgm /tmp/${i%.*}.R.pgm
    fi


    convert -crop 256x256+`echo $newShiftLength`+`echo $newShiftHeight` "/tmp/${i%.*}.R.pgm"  "$pgmDir/$current_dir/${i%.*}.pgm"

    rm "/tmp/${i%.*}.pgm"
    rm "/tmp/${i%.*}.ppm"
    rm "/tmp/${i%.*}.R.pgm"
	cpt=$((cpt+1))
done

rm $tmpcfg -f
