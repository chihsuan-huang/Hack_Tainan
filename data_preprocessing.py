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
import traceback
from lib.MysqlDB import *

# read data's url from file, return data_Name to url dictionary
def readURLFile(file_name):
	data_url = {}
	with open( file_name ) as inputFile:
		content = inputFile.readlines()
		for line in content:
			line = line.split(" ")
			print line[1]
			data_url[ line[0] ] = line[1]
	return data_url

# get data by read url
def getData(url):
	
	# make sure that we can get data from server
	try:
		response = urllib2.urlopen( url )
	except urllib2.HTTPError, e:
		print "Cannot retrieve URL: HTTP Error Code", e.code
		sys.exit(0)
	except urllib2.URLError, e:
			print "Cannot retrieve URL: " + e.reason[1]
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

def insertReadPriceData( data_name, datum, db):

	# unicode zh-tw string to 'utf-8' for find value in data
	tw_road_area = unicode("土地區段位置或建物區門牌", "utf-8")
	tw_buy_year = unicode("交易年月", "utf-8")
	tw_rent_year = unicode( "租賃年月", "utf-8" )
	tw_price = unicode("總價元", "utf-8")
	tw_price2 = unicode("總額元", "utf-8")
	tw_area = unicode( "鄉鎮市區", "utf-8" )
	
	sql = "INSERT INTO " + data_name + "( year, road, area, price ) VALUES"
	if tw_area in datum and tw_road_area in datum:
		if tw_buy_year in datum and tw_price in datum:
			sql = sql + "('" + str(datum[tw_buy_year]) + "','" + datum[tw_road_area] + "','" + datum[tw_area] + "','" + str(datum[tw_price]) + "');" 
		if tw_rent_year in datum and tw_price2 in datum:
			sql = sql + "('" + str(datum[tw_rent_year]) + "','" + datum[tw_road_area] + "','" + datum[tw_area] + "','" + str(datum[tw_price2]) + "');"
	else:
		print "Error json format is not match!" 
		sys.exit(0)


	db.exeSQL( sql )	


if __name__=='__main__':
	
	if len( sys.argv ) == 2:
		json_url_list = readURLFile( sys.argv[1] )
		csv_url_list = readURLFile( sys.argv[2] )
	else:
		mydb = MysqlDB( 'localhost', 'mydb', 'root', 'axszdc', 'utf8' )
		rep_data_url = readURLFile( "input_data/real_price_url" )
		#json_data_url = readURLFile( "input_data/json_url" )
		#csv_data_url = readURLFile( "input_data/csv_url" )
		for data_name in rep_data_url:
			#mydb.createTable( data_name )
			raw_data = getData( rep_data_url[ data_name ] )
			data = JsonReader( raw_data )
			city_data = filterByCity( data, "臺南市" )
			for datum in city_data:
				insertReadPriceData( data_name, datum, mydb)
		mydb.close()
