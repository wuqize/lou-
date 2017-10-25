#coding=utf-8


import os
import json
import datetime

import pymysql
import pymongo

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config.from_pyfile('./config.py')
db = SQLAlchemy(app)

mon = pymongo.MongoClient()
mon_db = "shiyanlou"
tag_col = "tag"
file_col = "file"

"""
文章表 class File(db.Model)

id：文章的ID，主键约束（db.Integer）
title: 文章名称（db.String(80)）
created_time: 文章创建时间（db.DateTime）
category_id: 文章的分类，外键约束（db.Integer, db.ForeignKey(...)）
content: 文章的内容（db.Text）

类别表 class Category(db.Model)

id：类别的ID，主键约束（db.Integer）
name：类别的名称（db.String(80)）

"""

class Category(db.Model):

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

class File(db.Model):

    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category",  backref='files')
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    # 向文章添加标签
    def add_tag(self, tag_name):
        # 为当前文章添加 tag_name 标签存入到 MongoDB
        col = mon[mon_db][file_col]
        added = col.find({"tag_name":tag_name, "file_id":self.id}).count()
        if not added:
            col.insert_one({"tag_name":tag_name, "file_id":self.id})
            return True
        return True

    # 移除标签
    def remove_tag(self, tag_name):
        # 从 MongoDB 中删除当前文章的 tag_name 标签
        col = mon[mon_db][file_col]
        col.remove({"tag_name": tag_name, "file_id": self.id})
        return True

    # 标签列表
    @property
    def tags(self):
        # 读取 mongodb，返回当前文章的标签列表
        col = mon[mon_db][file_col]
        data = col.find({"file_id": self.id})
        tags = []
        for item in data:
            tags.append(item["tag_name"])
        return tags

    def __repr__(self):
        return '<File %r>' % self.title

@app.route('/')
def index():
    # 显示文章名称的列表
    # 页面中需要显示所有文章的标题（title）列表，此外每个标题都需要使用 `<a href=XXX></a>` 链接到对应的文章内容页面
    files = File.query.all()
    return render_template('index.html', files=files)


@app.route('/files/<file_id>')
def file(file_id):
    # file_id 为 File 表中的文章 ID
    # 需要显示 file_id  对应的文章内容、创建时间及类别信息（需要显示类别名称）
    # 如果指定 file_id 的文章不存在，则显示 404 错误页面
    files = File.query.filter_by(id=file_id).limit(1).all()
    if files:
        return render_template('file.html', file=files[0])
    else:
        slog = "shiyanlou 404"
        return render_template('404.html', slog=slog)

@app.errorhandler(404)
def not_found(error):
    slog = "shiyanlou 404"
    return render_template('404.html', slog=slog), 404

if __name__ == "__main__":
    app.run(port=3000)
    # db.create_all()
    # java = Category('Java')
    # python = Category('Python')
    # file1 = File('Hello Java', datetime.datetime.utcnow(),  java, 'File Content - Java is cool!')
    # file2 = File('Hello Python', datetime.datetime.utcnow(), python, 'File Content - Python is cool!')
    # db.session.add(java)
    # db.session.add(python)
    # db.session.add(file1)
    # db.session.add(file2)
    # db.session.commit()
    # # 增加 MongoDB 中的数据
    # file1 = File.query.filter_by(id="1").all()[0]
    # file2 = File.query.filter_by(id="2").all()[0]
    # file1.add_tag('tech')
    # file1.add_tag('java')
    # file1.add_tag('linux')
    # file2.add_tag('tech')
    # file2.add_tag('python')