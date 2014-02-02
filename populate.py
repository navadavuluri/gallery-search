import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
import subprocess
from app import app
import pg

db_table = app.config['DB_NAME']

db = pg.connect(db_table, \
     app.config['DB_HOST'], \
     int(app.config['DB_PORT']), \
     None, None, \
     app.config['USERNAME'], \
     app.config['PASSWORD'] )


try:
	db.query("CREATE EXTENSION postgis;")
	db.query("CREATE TABLE "+db_table+" \
        ( \
          id serial NOT NULL, \
		about character varying(256), \
		image_url character varying(256), \
		addr character varying(128), \
		the_geom geometry, \
		CONSTRAINT "+db_table+"_pkey PRIMARY KEY (id), \
		CONSTRAINT enforce_dims_geom CHECK (st_ndims(the_geom) = 2), \
		CONSTRAINT enforce_geotype_geom CHECK (geometrytype(the_geom) = 'POINT'::text OR the_geom IS NULL), \
		CONSTRAINT enforce_srid_geom CHECK (st_srid(the_geom) = 4326) \
		) \
		WITH ( \
		OIDS=FALSE \
		); \
		\
		CREATE INDEX "+db_table+"_geom_gist \
		ON "+db_table+" \
		USING gist \
		(the_geom);")

	print("DB table created")
	print("Adding National Parks to DB...")
    
	db.query("Insert into "+db_table+" (about, image_url, addr, the_geom) VALUES ('Waves!', '../static/images/bigsur.jpg', 'Big Sure, CA 93920' , ST_GeomFromText('POINT(-121.807748 36.269973)', 4326));")
	db.query("Insert into "+db_table+" (about, image_url, addr, the_geom) VALUES ('Venice', '../static/images/burano.jpg', '888 Via S. Martino Sinistro, Venezia, VE 30142, Italy' , ST_GeomFromText('POINT(12.4168222 45.4854212)', 4326));")
	db.query("Insert into "+db_table+" (about, image_url, addr, the_geom) VALUES ('Wind', '../static/images/eastbay.jpg', 'MacDonald Park, Tracy, CA 95376' , ST_GeomFromText('POINT(-121.425877 37.731964)', 4326));")
	db.query("Insert into "+db_table+" (about, image_url, addr, the_geom) VALUES ('Like', '../static/images/fb.jpg', '1 Hacker Way, Menlo Park, 94025' , ST_GeomFromText('POINT(-122.148228 37.484224)', 4326));")

except Exception as e:
	print e
