#!/bin/sh

psql gtfs_bus -c "DROP MATERIALIZED VIEW IF EXISTS kraje_simplified,kraje_stops CASCADE;"
psql gtfs_bus -c "DROP TABLE IF EXISTS kraje CASCADE;"
ogr2ogr -f "PostgreSQL" PG:"dbname=gtfs_bus" $1 -nln kraje -append
psql gtfs_bus -c "CREATE MATERIALIZED VIEW kraje_simplified AS SELECT ogc_fid AS kraj_id,name,ST_SetSRID(st_simplify(wkb_geometry,0.01),4326) as geometry FROM kraje;"
psql gtfs_bus -c "CREATE INDEX ON kraje_simplified USING GIST(geometry);"
psql gtfs_bus -c "CREATE MATERIALIZED VIEW kraje_stops AS SELECT kraj_id,stop_id FROM gtfs_stops INNER JOIN kraje_simplified ON ST_Contains(geometry,ST_SetSRID(ST_MakePoint(stop_lon,stop_lat),4326));"
 
