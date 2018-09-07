#!/bin/sh

baseDomain=$1
series=$2
type=$3
key=$4
domain=$5
address=$6
ext=".pdf"
convertResult=0
out=""

dir=`python /ick/ick.py $baseDomain $series $type`

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
	# Email
	curl -H 'Content-Type:multipart/form-data' -s --user "api:$key" https://api.mailgun.net/v3/$domain/messages -F from="ick <postmaster@$domain>" -F to="User <$address>" -F subject="Incoming! $out" -F text="$out" -F attachment=@/tmp/$dir/$out
	# Cleanup
	#rm -rf $dir
	#rm -rf /tmp/$dir/
	exit 0
fi