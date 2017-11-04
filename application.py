from flask import Flask, request, render_template, jsonify
from subprocess import *
import random
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import time
import string
import json

application = Flask(__name__)

AWS_ACCESS_KEY = 'AKIAIJJTG5UK3MOYVRYA'
AWS_SECRET_KEY = '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'
region = 'us-east-1'
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'search-movies-qcuy57xetvnpg7hf3vr3x7uqpm.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

@application.route("/", methods=['GET', 'POST'])
def main_page():
    return render_template("final_test_1.html")


@application.route('/user/<username>')
def main_page_signed_in(username):
    return 'User %s' % username


@application.route('/signinpage', methods=['GET', 'POST'])
def sign_in():
    username = request.form['username']
    password = request.form['password']
    query = ""
    try:
        query = es.get(index=, doc_type=, id=username)
    except:
        return {"status": "notfound"}
    t = Popen(query, shell=True, stdout=PIPE)
    text = t.communicate()[0]
    response_json = eval(text)
    if response_json['_source']['password'] == password:
        return {"status": "true"}
    else:
        return {"status": "false"}

    return render_template("signed_in.html")


@application.route('/signuppage')
def sign_up():
    username = request.form['username']
    password = request.form['password']
    query = es.exists(id=username)
    if not query:
        es.index(index="movies", doc_type="movie", id="102", body={'password': password})
        return {"status": "created"}
    else:
        return {"status": "failed"}
    return render_template("signed_up.html")


if __name__ == "__main__":
    application.run()

