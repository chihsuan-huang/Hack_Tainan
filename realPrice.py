# !/usr/bin/evn python
# -*- coding: utf8 -*-

import re
import  sys
import json
import urllib2

# use arg1 URL to get json data
def getData():
	
	# make sure that we can get data from server
	try:
		response = urllib2.urlopen( sys.argv[1] )
	except URLError, e:
		if hasattr(e, 'reason'):
			print 'we failed to connect server'
			print e.reason
			sys.exit(0)
		elif hasattr(e, 'code'):
			print 'The server could not fulfill the request'
			print  e.code
			sys.exit(0)

	# convert to json format
	data = json.load( response, encoding = ('utf-8') )	
	
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
	# run program
	if len( sys.argv ) == 2:
		print __doc__
		print "Find", sys.argv[1]
		data = getData()
		result = filterByCity(data, "臺南市")
		for datum in result:
			for key in datum:
				print datum[ key ],			
			print
	else:
		print "ERROR len(argv) should be 2"
