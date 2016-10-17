__author__ = 'amit'

import minecraft
import time
import datetime
import requests

from flask import Flask, render_template, request, redirect, url_for, abort, session, make_response, jsonify, Response
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/status', methods=('GET', 'POST'))
def status():

    if request.method == 'POST':
        action = request.form.get("submit").lower()

        if 'start' in action:
            minecraft.start_ec2()
            minecraft.start_minecraft()
            time.sleep(5)
        elif 'stop' in action:
            minecraft.stop_ec2()
        else:
            # just refresh and update
            pass


    df_status = minecraft.get_minecraft_status()
    server_data = df_status.to_html(classes="table table-striped")
    update_date = datetime.datetime.today().strftime("%A %d-%b-%Y %r")
    form = None

    return render_template('status.html', server_data=server_data, form=form, update_date=update_date)


def highlight(val):

    good_color = '#32CD32'
    bad_color = 'red'
    none_color = '#bfbfbf'
    none_color = '#9dd196'
    try:
        if 'running' == val:
            color = good_color
        elif 'stopped' == val:
            color = bad_color
        else:
            color = none_color
    except:
        color = none_color
    return 'background-color: %s' % color



@app.route('/old', methods=('GET', 'POST'))
def status_old():

    if request.method == 'POST':
        print request.form['submit']
        action = request.form.get("submit", "value").lower()
        if 'start' in action:
            minecraft.start_ec2()
            minecraft.start_minecraft()
            time.sleep(5)
        elif 'stop' in action:
            minecraft.stop_ec2()
        else:
            # just refresh and update
            pass

    df_status = minecraft.get_minecraft_status()
    server_data = df_status.style.applymap(highlight).render()

    form = None
    return render_template('status.html', server_data=server_data, form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9000)
