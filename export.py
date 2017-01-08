#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import sys
import zipfile
import time
import os
import psycopg2
import psycopg2.extras
from functools import partial,reduce
from gtfs import GTFSTable,GTFSStreamTable,GTFSCalendar 
from datetime import timedelta, date

outdir = 'output'

def url_filter(row):
	if row["agency_url"]:
		row["agency_url"]="http://"+row["agency_url"]
	else:
		row["agency_url"]="http://example.com"
	return row

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)+1):
		yield start_date + timedelta(n)

def ymd_to_date(ymd):
	return date(int(ymd[0:4]),int(ymd[4:6]),int(ymd[6:8]))

def remove_keys_filter(row,keys):
	""" Remove given keys from the row """
	for key in keys:
		row.pop(key,None)
	return row

def long_name_filter(row):
	if str(row["route_short_name"]) == str(row["route_long_name"]):
		row["route_long_name"]=""
	return row

def date_swap_filter(row,field):
	adate = row[field]
	if adate:
		row[field]=adate[4:]+adate[2:4]+adate[0:2]
	return row

def add_days_filter(row):
	row["monday"] = 0 
	row["tuesday"] = 0 
	row["wednesday"] = 0 
	row["thursday"] = 0
	row["friday"] = 0 
	row["saturday"] = 0 
	row["sunday"] = 0 
	return row

def work_days_filter(row,sym):
	kod_fields = [row["p_kod1"],row["p_kod2"],row["p_kod3"],row["p_kod4"],row["p_kod5"],row["p_kod6"],row["p_kod7"],row["p_kod8"],row["p_kod9"]]
	if sym in kod_fields:
		row["monday"] = 1
		row["tuesday"] = 1
		row["wednesday"] = 1
		row["thursday"] = 1
		row["friday"] = 1 
	return row

def weekend_filter(row,sym):
	kod_fields = [row["p_kod1"],row["p_kod2"],row["p_kod3"],row["p_kod4"],row["p_kod5"],row["p_kod6"],row["p_kod7"],row["p_kod8"],row["p_kod9"]]
	if sym in kod_fields:
		row["saturday"] = 1
		row["sunday"] = 1 
	return row

def day_filter(row,sym,day):
	kod_fields = [row["p_kod1"],row["p_kod2"],row["p_kod3"],row["p_kod4"],row["p_kod5"],row["p_kod6"],row["p_kod7"],row["p_kod8"],row["p_kod9"]]
	if sym in kod_fields:
		row[day] = 1
	return row

def vehicle_filter(row):
	vehicles = {"A":3,"E":0,"T":3,"L":7,"M":1,"P":4}
	row["route_type"] = vehicles[row["route_type"]]
	return row

def pickup_filter(row):
	kod_fields = [row["p_kod1"],row["p_kod2"],row["p_kod3"]]
	if "(" in kod_fields:
		row["pickup_type"]=1
	return row

def drop_off_filter(row):
	kod_fields = [row["p_kod1"],row["p_kod2"],row["p_kod3"]]
	if ")" in kod_fields:
		row["drop_off_type"]=1
	return row

def arrival_filter(row):
	""" Copy arrival time from arrival if missing """
	if not row["arrival_time"] and row["departure_time"]:
		row["arrival_time"] = row["departure_time"]
	return row
def departure_filter(row):
	""" Copy departure time from arrival if missing """
	if not row["departure_time"] and row["arrival_time"]:
		row["departure_time"] = row["arrival_time"]
	return row

def seq_order_filter(row):
	if int(row["spoj"])%2 == 0:
		row["stop_sequence"] = 100000-int(row["stop_sequence"])
	return row

def time_filter(row,field):
	atime = row[field]
	row[field] = atime[:2]+":"+atime[2:4]+":00"
	return row

class Midnight_filter(object):
	def __init__(self):
		self.id = None
		self.hours = 0
		self.days = 0
		self.asc = True
	def __call__(self,row,field):
		if self.id == row["trip_id"]:
			ahours = int(row[field][:2])
			if ahours < self.hours:
				self.days += 1
			self.hours = ahours
			row[field] = "{:02d}".format(self.hours+24*self.days)+row[field][2:]
		else:
			self.id = row["trip_id"]
			self.days = 0
			self.hours = int(row[field][:2])
			self.asc = True if row["stop_sequence"] > 10000 else False
		return row




def cal_exceptions_filter(table):
	newtable = []
	for row in table:
		# jede
		if row["exception_type"] == "1":
			start=ymd_to_date(row["datum_od"])
			if row["datum_do"]:
				end=ymd_to_date(row["datum_do"])
			else:
				end=start
			for day in daterange(start,end):
				newrow = {}
				newrow["exception_type"] = 1
				newrow["service_id"] = row["service_id"]
				newrow["date"] = day.strftime("%Y%m%d")
				newtable.append(newrow)
				
		# jede take
		elif row["exception_type"] == "2":
			newrow = {}
			newrow["exception_type"] = 1
			newrow["service_id"] = row["service_id"]
			newrow["date"] = row["datum_od"] 
			newtable.append(newrow)
		# jede jen
		elif row["exception_type"] == "3":
			newrow = {}
			newrow["exception_type"] = 1
			newrow["service_id"] = row["service_id"]
			newrow["date"] = row["datum_od"] 
			newtable.append(newrow)
		# nejede
		elif row["exception_type"] == "4":
			start=ymd_to_date(row["datum_od"])
			if row["datum_do"]:
				end=ymd_to_date(row["datum_do"])
			else:
				end=start
			for day in daterange(start,end):
				newrow = {}
				newrow["exception_type"] = 2
				newrow["service_id"] = row["service_id"]
				newrow["date"] = day.strftime("%Y%m%d")
				newtable.append(newrow)
			
		# jede jen v lichych tydnech
		elif row["exception_type"] == "5":
			start=ymd_to_date(row["datum_od"])
			if row["datum_do"]:
				end=ymd_to_date(row["datum_do"])
			else:
				end=start
			for day in daterange(start,end):
				if day.isoweekday()[1]%2 == 1:
					continue
				newrow = {}
				newrow["exception_type"] = 2
				newrow["service_id"] = row["service_id"]
				newrow["date"] = day.strftime("%Y%m%d")
				newtable.append(newrow)

		# jede jen v sudych tydnech
		elif row["exception_type"] == "6":
			start=ymd_to_date(row["datum_od"])
			if row["datum_do"]:
				end=ymd_to_date(row["datum_do"])
			else:
				end=start
			for day in daterange(start,end):
				if day.isoweekday()[1]%2 == 0:
					continue
				newrow = {}
				newrow["exception_type"] = 2
				newrow["service_id"] = row["service_id"]
				newrow["date"] = day.strftime("%Y%m%d")
				newtable.append(newrow)

		# jede jen v lichych tydnech od ... do ...
		elif row["exception_type"] == "7":
			pass
		# jede jen v sudych tydnech od ... do ...
		elif row["exception_type"] == "8":
			pass
	return newtable

def default_filter(row,field,default):
	if not row[field]:
		row[field] = default
	return row
	



agency_query="SELECT agency_id,agency_name,agency_url,agency_timezone,agency_phone FROM agency;"
routes_query="SELECT route_id,agency_id,route_short_name,route_long_name,route_type FROM routes;"
stops_query="SELECT stop_id,stop_name,stop_lat,stop_lon FROM stops;"
stop_times_query="SELECT trip_id,arrival_time,departure_time,stop_id,stop_sequence,shape_dist_traveled,\
	p_kod1,p_kod2,p_kod3,spoj,0 AS drop_off_type, 0 AS pickup_type \
	FROM stop_times ORDER BY (trip_id,stop_sequence);"
trips_query="SELECT route_id,service_id,trip_id FROM trips;"

calendar_query="SELECT service_id,start_date,end_date,p_kod1,p_kod2,p_kod3,p_kod4,p_kod5,p_kod6,p_kod7,p_kod8,p_kod9 FROM calendar;"
calendar_dates_query="SELECT '' AS date,service_id,datum_od,datum_do,exception_type FROM calendar_dates;"


agency = GTFSTable("agency",agency_query)
routes = GTFSTable("routes",routes_query)
stops = GTFSTable("stops",stops_query)
stop_times = GTFSStreamTable("stop_times",stop_times_query)
trips = GTFSTable("trips",trips_query)

calendar = GTFSTable("calendar",calendar_query)
calendar_dates = GTFSTable("calendar_dates",calendar_dates_query) 
 
# Connect to the database
try:
	conn = psycopg2.connect('dbname=jdf')
except:
	print("Unable to connect to database \"jdf\"")
	sys.exit(1)
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

print("Agency...")
stime = time.time()
agency.fetch_from_db(cur)
agency.add_filter(url_filter)
agency.apply_filters()
agency.export_to_file()
del agency.table
print("{:.3f} s".format(time.time()-stime))

print("Routes...")
stime = time.time()
routes.fetch_from_db(cur)
routes.add_filter(vehicle_filter)
routes.add_filter(long_name_filter)
routes.apply_filters()
routes.export_to_file()
del routes.table
print("{:.3f} s".format(time.time()-stime))

print("Stops...")
stime = time.time()
stops.fetch_from_db(cur)
stops.add_filter(partial(default_filter,field="stop_lon",default=0.0))
stops.add_filter(partial(default_filter,field="stop_lat",default=0.0))
stops.apply_filters()
stops.export_to_file()
del stops.table
print("{:.3f} s".format(time.time()-stime))

print("Stop times...")
stime = time.time()
stop_times.add_filter(departure_filter)
stop_times.add_filter(arrival_filter)
stop_times.add_filter(partial(Midnight_filter(),field="arrival_time"))
stop_times.add_filter(partial(Midnight_filter(),field="departure_time"))
stop_times.add_filter(partial(time_filter,field="arrival_time"))
stop_times.add_filter(partial(time_filter,field="departure_time"))
stop_times.add_filter(pickup_filter)
stop_times.add_filter(drop_off_filter)
#stop_times.add_filter(seq_order_filter)
stop_times.add_filter(partial(remove_keys_filter,keys=["p_kod1","p_kod2","p_kod3","spoj"]))
stop_times.process(cur)
print("{:.3f} s".format(time.time()-stime))

print("Trips...")
stime = time.time()
trips.fetch_from_db(cur)
trips.apply_filters()
trips.export_to_file()
print("{:.3f} s".format(time.time()-stime))

print("Calendar...")
stime = time.time()
calendar.fetch_from_db(cur)
calendar.add_filter(partial(date_swap_filter,field="start_date"))
calendar.add_filter(partial(date_swap_filter,field="end_date"))
calendar.add_filter(add_days_filter)
calendar.add_filter(partial(work_days_filter,sym="X"))
calendar.add_filter(partial(weekend_filter,sym="+"))
calendar.add_filter(partial(day_filter,sym="1",day="monday"))
calendar.add_filter(partial(day_filter,sym="2",day="tuesday"))
calendar.add_filter(partial(day_filter,sym="3",day="wednesday"))
calendar.add_filter(partial(day_filter,sym="4",day="thursday"))
calendar.add_filter(partial(day_filter,sym="5",day="friday"))
calendar.add_filter(partial(day_filter,sym="6",day="saturday"))
calendar.add_filter(partial(day_filter,sym="7",day="sunday"))
calendar.add_filter(partial(remove_keys_filter,keys=["p_kod1","p_kod2","p_kod3","p_kod4","p_kod5","p_kod6","p_kod7","p_kod8","p_kod9"]))
calendar.apply_filters()
calendar.export_to_file()
del calendar.table
print("{:.3f} s".format(time.time()-stime))

print("Calendar dates...")
stime = time.time()
calendar_dates.fetch_from_db(cur)
calendar_dates.add_filter(partial(date_swap_filter,field="datum_od"))
calendar_dates.add_filter(partial(date_swap_filter,field="datum_do"))
calendar_dates.add_filter(cal_exceptions_filter,False)
calendar_dates.apply_filters()
calendar_dates.export_to_file()
del calendar_dates.table
print("{:.3f} s".format(time.time()-stime))


with zipfile.ZipFile(os.path.join(outdir,"gtfs-bus.zip"),"w") as gtfszip:
#	for table in [agency,routes,stops,stop_times,trips,calendar_dates]:
	for table in [agency,routes,stops,stop_times,trips,calendar,calendar_dates]:
		gtfszip.write(os.path.join(table.outdir,table.name+".txt"),arcname=table.name+".txt")
