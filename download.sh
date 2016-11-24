#!/bin/sh


mkdir -p data/input

cd data

rm -f JDF.zip
wget "ftp://ftp.cisjr.cz/JDF/JDF.zip"
unzip -qfd input JDF.zip
cd input
for f in `ls`
do
	echo Extracting $f
	NUM="${f%.*}"
	mkdir -p $NUM
	unzip -qf -d $NUM $f
done

