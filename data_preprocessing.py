# !/usr/bin/evn python
# -*- coding: utf8 -*-
'''
1. get data source url from a file, 
2. load url data and save them to database
'''

import re
import  sys
import csv
import json
import urllib2

# read data's url from file, return url list
def readURLFile(file_name):
	url_list = []
	with open( file_name ) as inputFile:
		content = inputFile.readlines()
		for line in content:
				url_list.append(line)
	return url_list

# get data by read url
def getData( url ):
	
	# make sure that we can get data from server
	try:
		response = urllib2.urlopen( url )
	except URLError, e:
		if hasattr(e, 'reason'):
			print 'we failed to connect server'
			print e.reason
			sys.exit(0)
		elif hasattr(e, 'code'):
			print 'The server could not fulfill the request'
			print  e.code
			sys.exit(0)
	return response

def JsonReader( raw_data ):

	# convert to json format
	data = json.load( raw_data, encoding = ('utf-8') )	
	return data

def CSVReader( raw_data ):

	# convert to csv format
	data = csv.reader( raw_data )	
	return data

# filter data by city 
def filterByCity(data, city):
	
	# unicode zh-tw string to 'utf-8' for find value in data
	tw_road_area = unicode("土地區段位置或建物區門牌", "utf-8")
	
	# regular expression compile pattern for reuse in following search
	pattern = re.compile( city )

	city_data = []
	# start to match data
	for datum in data:
		# check that data's key is same to our json format
		if tw_road_area in datum:
			if datum[tw_road_area] and\
				pattern.search( datum[tw_road_area].encode("utf8") ):
				city_data.append( datum )
		else: 
			print "Error json format is not match!" 
			sys.exit(0)

	# return city_data
	return city_data

if __name__=='__main__':
	if len( sys.argv ) == 2:
		json_url_list = readURLFile( sys.argv[1] )
		csv_url_list = readURLFile( sys.argv[2] )

		'''
		for url in url_list:
			raw_data = getData( url )
			data = CSVReader( raw_data )		
			for row in data:
				for col in row:
						print col,
				print'''
	else:
		read_price_url_list = readURLFile( "data/real_price_url" )
		json_url_list = readURLFile( "data/json_url" )
		csv_url_list = readURLFile( "data/csv_url" )

		for url in read_price_url_list:
			raw_data = getData( url )
			data = JsonReader( raw_data )
			city_data = filterByCity( data, "臺南市" )
			for row in city_data:
				for col in row:
					print row[col],
				print
