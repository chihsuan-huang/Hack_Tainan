# !/usr/bin/evn python
# -*- coding: utf8 -*-

import MySQLdb

class MysqlDB:
	
	# initial object
	def __init__(self, host, db_name, user, passwd, charset):
		self.host = host
		self.db_name = db_name
		self.user = user
		self.passwd = passwd
		self.charset = charset
		self.connectdb()

	# connect to database
	# will create a Cursor object which can execute all the quries you need.
	def connectdb(self):
		try:
			self.db = MySQLdb.connect( host = self.host,
						  db = self.db_name,
						  user = self.user,
						  passwd = self.passwd,
						  charset = self.charset )
			self.cursor = self.db.cursor()
		except MySQLdb.Error:
			print "ERROR: in connectdb"
	# execute sql statment
	def exeSQL(self, sql ):
		try:
			self.cursor.execute( sql )
			self.db.commit()
		except:
			self.db.rollback()

	def basicInfor(self):
		self.cursor.execute( "SELECT VERSION()")
		data = self.cursor.fetchone()
		if data:
			print "Database version", data

	# disconnect database
	def close(self):
		self.cursor.close()
		self.db.close()



