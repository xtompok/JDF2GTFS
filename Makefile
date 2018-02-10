.PHONY: utf
.PHONY: database
.PHONY: GTFS
.PHONY: all


all: download utf preformat database GTFS

schema:
	psql jdf < schema.sql

download:
	./download.sh

utf:
	./to-utf.sh

preformat: preformat.c


database: 
	psql jdf <schema.sql
	./import-to-db
	./import-stop-pos
	psql jdf <GTFS/views.sql

GTFS:
	mkdir -p output/
	./export.py
	./postprocess.py			
	cd output && zip gtfs-bus-out.zip *.txt		

JDFversion:
	cd data/utf/; for i in `ls`; do cat $$i/VerzeJDF.txt; done | sort | uniq -c
