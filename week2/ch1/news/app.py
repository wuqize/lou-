#coding=utf-8

import os
import json

from flask import Flask, render_template

FILE_DIR_PATH = "/home/shiyanlou/files"

app = Flask(__name__)
app.config.from_pyfile('./config.py')


def file_load(filename, file_type="json"):
	with open(os.path.join(FILE_DIR_PATH, filename), "r") as f:
		if file_type == "json":
			return json.load(f)
@app.route("/")
def index():
	json_file = [ 
		item for item in  os.listdir(FILE_DIR_PATH) 
			if item.endswith(".json")
			]
	print(json_file)
	title_list = []
	for item in json_file:
		title_list.append(file_load(item)["title"])
	return render_template('index.html', title_list=title_list)

@app.route("/files/<filename>")
def file(filename):
	filename = "{}.json".format(filename)
	json_file = [ item for item in  os.listdir("/home/shiyanlou/files") if item.endswith(".json")]
	if filename in json_file:
		file_content = file_load(filename)
		return render_template('file.html', file_content=file_content)
	else:
		slog = "shiyanlou 404"
		return render_template('404.html', slog=slog)

@app.errorhandler(404)
def not_found(error):
	slog = "shiyanlou 404"
	return render_template('404.html', slog=slog), 404

if __name__ == "__main__":
	app.run(port=3000)