.PHONY: utf
.PHONY: database
.PHONY: GTFS
.PHONY: all


all: download utf database GTFS

schema:
	psql jdf < schema.sql

download:
	./download.sh

utf:
	./to-utf.sh

database: 
	psql jdf <schema.sql
	./import-to-db
	./import-stop-pos
	psql jdf <GTFS/views.sql

GTFS:
	./export.py
	./postprocess.py			
	cd output && zip gtfs-bus-out.zip *.txt		

JDFversion:
	cd data/utf/; for i in `ls`; do cat $$i/VerzeJDF.txt; done | sort | uniq -c

old:
	rm -rf GTFS/dump/
	mkdir GTFS/dump
	rm -rf GTFS/output/
	mkdir GTFS/output
	mysql --user=jdf --password=kokoko JDF <GTFS/views.sql
	./export-GTFS agency
	./export-GTFS stops
	./export-GTFS routes
	./export-GTFS trips
	./export-GTFS stop_times
	./export-GTFS calendar
	for i in `ls GTFS/dump`; do cp GTFS/dump/$$i GTFS/output/$$i;done;
	cd GTFS && ./postprocess.py
	cd GTFS/output && zip GTFS.zip agency.txt stops.txt routes.txt trips.txt stop_times.txt calendar.txt
