#!/usr/bin/python3

import sys
sys.path.append("./gtfstools")
from gtfs import load_gtfs,save_gtfs,load_gtfs_table,save_gtfs_table
from dicttable import DictTable
from shutil import move as mv

#gtfs = load_gtfs("output/gtfs-bus.zip")
#
## Filter stops to only used stops
#used_stops = set(map(lambda x: x["stop_id"],gtfs["stop_times"]))
#outstops = []
#for stop in gtfs["stops"]:
#	if stop["stop_id"] in used_stops:
#		outstops.append(stop)
#gtfs["stops"] = outstops
#
#save_gtfs("output/gtfs-bus2.zip",gtfs)

GTFS_FILE = "output/gtfs-bus2.zip"

def union_table(table,column):
	cols = list(table[0].keys())
	print(cols)
	cols.remove(column)
	table_copy = [tuple([row[col] for col in cols]) for row in table]
	row_set = list(set(table_copy))
	row_dict = {key:index for (index,key) in enumerate(row_set)} 
	print(len(row_set))
	lut = {}
	for row in table:
		row_tuple = tuple([row[col] for col in cols])
		index = row_dict[row_tuple]
		lut[row[column]]=index
	
	new_table = DictTable(cols+[column])
	for (col_val,row) in enumerate(row_set):
		newcol = {key:row[i] for (i,key) in enumerate(cols) }
		newcol[column] = col_val
		new_table.append(newcol)
	return (new_table,lut)

def update_column_lut(table,column,lut,missing=-1):
	for row in table:
		try:
			row[column] = lut[row[column]]
		except KeyError:
			row[column] = -1
	return table


def union_tables_column(main_table,ref_tables,column):
	mtable = load_gtfs_table(main_table)
	(new_mtable,lut) = union_table(mtable,column)
	save_gtfs_table(main_table,new_mtable)
	del mtable
	del new_mtable
	
	for ref_table in ref_tables:
		rtable = load_gtfs_table(ref_table)
		update_column_lut(rtable,column,lut)
		save_gtfs_table(ref_table,rtable)

def union_calendar(calendar_file,caldates_file,trips_file):
	cal = load_gtfs_table(calendar_file)
	caldates = load_gtfs_table(caldates_file)
	trips = load_gtfs_table(trips_file)

def delete_columns(table_file,columns):
	table = load_gtfs_table(table_file)
	for col in columns:
		table.delete_column(col)
	save_gtfs_table(table_file,table)		
	
	
delete_columns("output/stop_times.txt",["p_kod1","p_kod2","p_kod3","spoj"])
union_tables_column("output/agency.txt",["output/routes.txt"],"agency_id")
union_tables_column("output/stops.txt",["output/stop_times.txt"],"stop_id")
