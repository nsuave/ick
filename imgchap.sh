#!/bin/sh

baseDomain=$1
series=$2
type=$3
ext=".pdf"
convertResult=0
out=""

dir=`python /imgchap/imgchap.py $baseDomain $series $type`

if [ $? -ne 0 ]; then
	echo "Error:"
	echo $dir
	exit 1
else
	# Output directory setup
	mkdir /tmp/$dir

	# Remove trailing slash and add ext
	out=${dir::-1}
	out=$out$ext

	# Add * for directory path
	dirstar=$dir\*

	# Convert
	/usr/bin/convert $dirstar /tmp/$dir/$out
	convertResult=$?
fi

if [ $convertResult -ne 0 ]; then
	echo "Conversion Failure:"
	echo $convertResult
	exit 1
else
	echo "Conversion Success!"
	echo "/tmp/$dir$out"
	# Cleanup
	rm -rf $dir
	exit 0
fi
