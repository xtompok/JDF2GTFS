#!/usr/bin/python3

import sys
from gtfs import load_gtfs,save_gtfs,load_gtfs_table,save_gtfs_table
from dicttable import DictTable

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

	
	
def union_agencies():
	agencies = load_gtfs_table(GTFS_FILE,"agency")
	(new_agencies,lut) = union_table(agencies,"agency_id")
	save_gtfs_table(GTFS_FILE,new_agencies,"agency")
	
	routes = load_gtfs_table(GTFS_FILE,"routes")
	update_column_lut(routes,"agency_id",lut)
	save_gtfs_table(GTFS_FILE,routes,"routes")

def union_stops():
	stops = load_gtfs_table(GTFS_FILE,"stops")
	(new_stops,lut) = union_table(stops,"stop_id")
	save_gtfs_table(GTFS_FILE,new_stops,"stops")

	del stops
	del new_stops
	print("Fixing stop_times")

	stop_times = load_gtfs_table(GTFS_FILE,"stop_times")
	update_column_lut(stop_times,"stop_id",lut)
	save_gtfs_table(GTFS_FILE,stop_times,"stop_times")
	pass



	

union_agencies()
union_stops()
