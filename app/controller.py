"""
Final Project For Freshman Seminar (Computational Thoughts)
Authors: Nauman Ahmad & Jeffrey He
"""
from . import app, db
from .models import ZipCodes, HotSpots
from .utils import Distance, generate_map

from flask import render_template, request, redirect, url_for, flash
from geopy.geocoders import Nominatim

import requests

geolocator = Nominatim()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/nearme')
def find_hotspot_nearme():
    # Get users location based on IP address
    res = requests.get('http://freegeoip.net/json').json()

    if res['city'] != "New York":
        flash("Whoops, Looks Like You Are Not In NYC!")
        return redirect(url_for('index'))

    lat = res['latitude']
    lon = res['longitude']

    my_map = generate_map(lat, lon)

    return render_template("result.html", my_map=my_map, nearme=True)


@app.route('/nearzipcode', methods=["POST"])
def find_hotspot_nearzipcode():
    if "zipcode" in request.form:
        # Get zipcode entered by user
        zipcode = request.form['zipcode']

    # Search the database for the zipcode entered by the user
    zipcode_details = ZipCodes.query.filter_by(zipcode=zipcode).first()

    if zipcode_details is not None:
        my_map = generate_map(
            zipcode_details.latitude, zipcode_details.longitude)
    else:
        flash("Invalid Zipcode")
        return redirect(url_for('index'))

    return render_template("result.html", my_map=my_map, zipcode=zipcode)


@app.route('/nearaddress', methods=["POST"])
def hotspot_near_address():
    if "address" in request.form:
        address = request.form["address"]

    try:
        location = geolocator.geocode(address)
        lat = location.latitude
        lon = location.longitude
        # Checks if the address entered by user is in NYC
        assert "NYC" in location.raw['display_name']
    except:
        flash("Invalid Address Entered")
        return redirect(url_for("index"))

    my_map = generate_map(lat, lon)
    return render_template("result.html", my_map=my_map, address=address)


@app.errorhandler(404)
def not_found_error(err):
    return render_template("error_handler.html", err=err)
