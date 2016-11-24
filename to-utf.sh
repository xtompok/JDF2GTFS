#!/bin/sh

rm -rf data/utf/*
for d in `ls -d data/input/*/`;
	do
		echo $d;
		DIR=`basename $d`
		mkdir -p data/utf/$DIR;
		for f in `ls data/input/$DIR`
		do
			cat data/input/$DIR/$f | iconv -f windows-1250 -t utf-8 >data/utf/$DIR/$f
			dos2unix -q data/utf/$DIR/$f 
		done
	done

