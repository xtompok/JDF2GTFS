#!/bin/sh


mkdir -p data/input

cd data

rm -rf JDF.zip input/*
wget "ftp://ftp.cisjr.cz/JDF/JDF.zip"
unzip -qod input JDF.zip
cd input
for f in `ls`
do
	echo Extracting $f
	NUM="${f%.*}"
	mkdir -p $NUM
	unzip -qf -d $NUM $f
done

