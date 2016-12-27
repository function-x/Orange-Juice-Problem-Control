# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-24 01:54:50
# @Last Modified by:   Michael
# @Last Modified time: 2016-12-27 20:14:25
from flask import Flask, request, jsonify
from flask_script import Manager


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"

manager = Manager(app)


@app.route('/create', method='GET')
def create():
    if request.method == 'GET':
        owner = request.args.get('reponame')
        url = request.args.get('url')
        pass
    else:
        return jsonify(code=7, message="please use GET method.")


@app.route('/update', method='GET')
def update():
    if request.method == 'GET':
        owner = request.args.get('reponame')
        pass
    else:
        return jsonify(code=7, message="please use GET method.")


@app.route('/delete', method='GET')
def delete():
    if request.method == 'GET':
        owner = request.args.get('reponame')
        pass
    else:
        return jsonify(code=7, message="please use GET method.")


if __name__ == '__main__':
    manager.run()
