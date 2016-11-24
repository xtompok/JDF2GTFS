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
	./clear_database.sh
	mysql --user=jdf --password=kokoko JDF <schema.sql
	for i in `ls utf`; do ./import-to-db $$i; done;

GTFS:
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
