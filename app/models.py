import os, sys
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
import pg
from app import db, db_name
import json



class dbImages():

	def query_all(self):
		result = None 
		try:	
			result = db.query('SELECT id,about,image_url,addr,ST_X(the_geom) as lon,ST_Y(the_geom) as lat FROM '+  db_name + ";")	
		except Exception as e:
			print e
		return result.dictresult()



	def query_search(self, lat, lon, distance_mi):
		result = None 
		try:	
			print 'SELECT id,about,image_url,addr,ST_X(the_geom) as lon,ST_Y(the_geom) as lat FROM '+ db_name+ \
                                ' WHERE ST_Distance_Sphere(the_geom, ST_MakePoint('+ lon + ', ' + lat + ')) <=' + distance_mi + ' * 1609.34;'
			result = db.query('SELECT id,about,image_url,addr,ST_X(the_geom) as lon,ST_Y(the_geom) as lat FROM '+ db_name+ \
				' WHERE ST_Distance_Sphere(the_geom, ST_MakePoint('+ lon + ', ' + lat + ')) <=' + distance_mi + ' * 1609.34;')
		except Exception as e:
			print e
		return result.dictresult()




	def query(self, request):
		if all (key in request.args for key in ("lat", "lon", "distance_mi")):
			images = self.query_search(request.args['lat'], request.args['lon'], request.args['distance_mi'])	
		else:
			images = self.query_all()

		return images 

