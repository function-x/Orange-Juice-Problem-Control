# -*- coding: utf-8 -*-
# @Author: Michael
# @Date:   2016-12-28 01:46:49
# @Last Modified by:   Michael
# @Last Modified time: 2017-01-02 15:21:35
from flask import Flask, request, jsonify
from flask_script import Manager


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"

manager = Manager(app)


@app.route('/create', methods=['GET'])
def create():
    if request.method == 'GET':
        owner = request.args.get('reponame')
        url = request.args.get('url')
        return jsonify(code=0, owner=owner, url=url)
    else:
        return jsonify(code=7, message="please use GET method.")


@app.route('/update', methods=['GET'])
def update():
    if request.method == 'GET':
        owner = request.args.get('reponame')
        return jsonify(code=0, owner=owner)
    else:
        return jsonify(code=7, message="please use GET method.")


@app.route('/delete', methods=['GET'])
def delete():
    if request.method == 'GET':
        owner = request.args.get('reponame')
        return jsonify(code=0, owner=owner)
    else:
        return jsonify(code=7, message="please use GET method.")


if __name__ == '__main__':
    manager.run()
