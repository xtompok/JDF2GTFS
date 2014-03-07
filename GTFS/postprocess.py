#!/usr/bin/python
# -*- coding: utf-8 -*- 

import csv

def formatTime(time):
	return time[:2]+":"+time[2:4]+":00"

def stop_times():
	with open("dump/stop_times.txt","r") as rad, open("output/stop_times.txt","w") as out:
		reader = csv.reader(rad,lineterminator="\n")
		names = reader.next()
		reader = csv.DictReader(rad,names,lineterminator="\n")
		writer = csv.writer(out,lineterminator="\n")
		writer.writerow(names[:-1])
		writer = csv.DictWriter(out,names[:-1],lineterminator="\n",extrasaction="ignore")
		for row in reader:
			if row["departure_time"] in ["<","|"]:
				continue
			if row["arrival_time"] == "":
				row["arrival_time"]=row["departure_time"]
			row["arrival_time"]=formatTime(row["arrival_time"])
			row["departure_time"]=formatTime(row["departure_time"])
			writer.writerow(row)
			

def routes():
	with open("dump/routes.txt","r") as routes, open("output/routes.txt","w") as out:
		reader = csv.reader(routes,lineterminator="\n")
		names = reader.next()
		reader = csv.DictReader(routes,names,lineterminator="\n")
		writer = csv.writer(out,lineterminator="\n")
		writer.writerow(names)
		writer = csv.DictWriter(out,names,lineterminator="\n")
		for line in reader:
			line["route_type"]=types[line["route_type"]]
			try:
				writer.writerow(line)
			except TypeError:
				print line

def agency():
	with open("output/agency.txt","a") as ag:
		ag.write('"65535","Neznama","http://kam.mff.cuni.cz","Europe/Prague","dopravce neznamy"')

def stops():
	with open("output/not_in_map.txt","r") as nim, open("output/stops.txt","a") as out:
		reader = csv.reader(nim,lineterminator="\n")
		writer = csv.writer(out,lineterminator="\n")
		try:
			reader.next()
		except StopIteration:
			return
		for line in reader:
			writer.writerow(line+[48.6988086, 20.2582856,"Europe/Prague"])

stop_times()

