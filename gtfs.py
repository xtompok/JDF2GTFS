import zipfile
import os
import sys
import csv
import datetime
import time
import tempfile
import zipfile
from pprint import pprint
from dicttable import DictTable

class StopTime:
	def __init__(self,astr):
		self.hour = int(astr[:2])
		self.min = int(astr[3:5])
		self.sec = int(astr[6:8])
	
	def __lt__(self,other):
		if not isinstance(other,StopTime):
			return TypeError("Must compare to StopTime")
		if self.hour < other.hour:
			return True
		if self.min < other.min:
			return True
		if self.sec < other.sec:
			return True
	
	def __str__(self):
		return "{:02}:{:02}:{02}".format(self.hour,self.min,self.sec)
	
	def __repr__(self):
		return str(self)

class GTFSCalendar(object):
	""" Class for managing GTFS calendar_dates table"""
	outdir = 'output'
	def __init__(self,query,day,month,year):
		self.gvdstart = datetime.date(day,month,year) 
		self.name = "calendar_dates"
		self.query = query
		self.table = None
	
	def fetch_from_db(cur):
		cur.execute(self.query)
		res = cur.fetchall()
		for row in res:
			self.table.append(dict(row))

	def export_to_file(self):
		with open(os.path.join(self.outdir,self.name+".txt"),"w") as out:	
			colnames = ["service_id","date","exception_type"]
			writer = csv.writer(out)
			writer.writerow(colnames)
			# Special service for "goes every day", which is not specified in the input files
			#everyday = self.bitmap_to_caldates(1,"".join(["1" for i in range(553)]))
			#writer.writerows(everyday)
			# Special service for "goes when needed", for our purposes never
			#whenneed = self.bitmap_to_caldates(0,"".join(["0" for i in range(553)]))
			#writer.writerows(whenneed)
			for row in self.table:
				caldates = self.bitmap_to_caldates(row["service_id"],row["bitmap"])
				writer.writerows(caldates)
		

	def bitmap_to_caldates(self,service_id,bitmap):
		""" Convert bitmap for days to list of GTFS exceptions """
		startord = self.gvdstart.toordinal()
		caldates = []
		first = True
		for d in range(553):
			if int(bitmap[d]) == 1:
				datestr = datetime.date.fromordinal(startord+d).strftime("%Y%m%d")
				caldates.append([service_id,datestr,1])
			elif first:
				datestr = datetime.date.fromordinal(startord+d).strftime("%Y%m%d")
				caldates.append([service_id,datestr,2])
				first=False
				
		return caldates

class GTFSTable(object):
	""" Manage GTFS table (except calendar tables)"""
	outdir = 'output'
	
	def __init__(self,name,query):
		self.query = query
		self.name = name
		self.filters = []
		self.table = None
	def add_filter(self,afilter,is_row=True):
		""" Add row/table filter to apply on table"""
		self.filters.append([afilter,is_row])
	def fetch_from_db(self,cur):
		cur.execute(self.query)
		res = cur.fetchall()
		self.table = []
		for row in res:
			self.table.append(dict(row))

	def apply_filters(self):
		""" Apply all filters added to the table """
		# TODO: nahradit map-em
		for f,is_row in self.filters:
			if is_row:
				self.table = list(map(f,self.table))
			else:
				self.table = f(self.table)
		
	def export_to_file(self):
		with open(os.path.join(self.outdir,self.name+".txt"),"w") as out:	
			colnames = self.table[0].keys()
			writer = csv.DictWriter(out,colnames)
			writer.writeheader()
			# Debug, should be replaced with writerows
			for row in self.table:
				try:
					writer.writerow(row)
				except:
					pprint(row)
	
class GTFSStreamTable(object):
	""" Manage GTFS table  (except calendar tables)
	Does not store whole table in RAM, table filters are not possible"""
	outdir = 'output'
	
	def __init__(self,name,query):
		self.query = query
		self.name = name
		self.filters = []
		self.table = None
	def add_filter(self,afilter,is_row=True):
		""" Add row/table filter to apply on table"""
		self.filters.append([afilter,is_row])

	def process(self,cur):
		out = open(os.path.join(self.outdir,self.name+".txt"),"w")	
		
		cur.execute(self.query)
		row = cur.fetchone()
		colnames = dict(row).keys()
		cur.scroll(0,'absolute')
		writer = csv.DictWriter(out,colnames)
		writer.writeheader()
		
		processed = 0
		print("Processing results ({})".format(time.time()))
		while True:
			res = cur.fetchmany(10000)
			if len(res)==0:
				break
			self.table = []
			for row in res:
				self.table.append(dict(row))

			# TODO: nahradit map-em
			for f,is_row in self.filters:
				if is_row:
					self.table = list(map(f,self.table))
				else:
					print("In streamed table cannot be table filters")
					sys.exit(1)
			# Debug, should be replaced with writerows
			for row in self.table:
				try:
					writer.writerow(row)
				except:
					pprint(row)
			if processed%100000 == 0:
				print("Processed: {} ({})".format(processed,time.time()))
				processed += len(res)
		out.close()
		



def load_gtfs(filename,encoding='utf-8'):
	tables={}
	with zipfile.ZipFile(filename) as gtfs:
		for fname in gtfs.namelist():
			with gtfs.open(fname) as tablefile:
				lines = tablefile.readlines()
				lines = list(map(lambda x: x.strip(),map(lambda x: x.decode(encoding),lines)))
				table = csv.reader(lines)
				name = fname[:-4]
				columns = next(table) 
				tables[name]=DictTable(columns,[line for line in table])
	return tables


def sort_stop_times(st):
	st.col_convert('stop_sequence',int)
	st.col_convert('arrival_time',StopTime)
	st.col_convert('departure_time',StopTime)
	st.key_sort(['trip_id','stop_sequence']) 
	

def save_gtfs(filename,tables):
	with zipfile.ZipFile(filename,"w",compression=zipfile.ZIP_DEFLATED) as zipf:
		for (name,table) in tables.items():
			fieldnames = table[0].keys()
			tablef = tempfile.NamedTemporaryFile(mode="w",encoding="utf-8")
			writer=csv.DictWriter(tablef,fieldnames)
			writer.writeheader()
			writer.writerows(table)
			tablef.flush()
			zipf.write(tablef.name,name+".txt")
			tablef.close()


def load_gtfs_table(filename):
	with open(filename) as tablefile:
		lines = tablefile.readlines()
		lines = list(map(lambda x: x.strip(),lines))
		table = csv.reader(lines)
	columns = next(table)
	return DictTable(columns,[line for line in table])

def save_gtfs_table(filename,table):
	fieldnames = table[0].keys()
	print("Fieldnames: {}".format(fieldnames))
	tablef = open(filename,mode="w",encoding="utf-8")
	writer=csv.DictWriter(tablef,fieldnames)
	writer.writeheader()
	writer.writerows(table)
	tablef.close()
		
