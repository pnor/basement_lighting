from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('root', __name__, url_prefix='/')

ls = [
    "Rainbow Pulsing", 
    "Gaussian Noise + Flood", 
    "All Black, Like OFF", 
    "Sigmoid", 
    "Fairy", 
    "Snake", 
    "Fire", 
    "Water", 
    "Party", 
    "Strobe Fast", 
    "Rainbow Perlin Noise", 
    "Cloud", 
]

@bp.route("/")
def route_main():
    return render_template("index.html", patterns=ls)
