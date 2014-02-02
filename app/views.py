import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
from app import app
from .models import dbImages
import subprocess

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/index.html')
def index_page():
    return render_template('index.html')

@app.route('/photos', methods = ['GET'])
def get_images():
	dbIm = dbImages()
	if request.method == 'GET':
		images = dbIm.query(request)
		return jsonify(collection=images)
	else:
		return 400

"""def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
"""
@app.route('/upload', methods = ['POST'])
def save_image():
	if request.method == 'POST':
		try:
			file = request.files['file']
			if file and allowed_file(file.filename):
            			filename = secure_filename(file.filename)
            			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            			return redirect(url_for('uploaded_file',
            	                        filename=filename))
		except Exception, e:
    			print repr(e)
    	return 
