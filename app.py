import os
import json
import random
from flask import Flask, render_template_string, redirect, url_for
from engine import get_current_missions, fetch_missions_from_ai
from templates import get_ui_template, gen_stars

app = Flask(__name__)

# 1. REGISTER THE SHUFFLE FILTER
# This allows {{ list | shuffle }} to work in your HTML template
def shuffle_filter(l):
    if not l:
        return l
    l_copy = list(l)
    random.shuffle(l_copy)
    return l_copy

app.jinja_env.filters['shuffle'] = shuffle_filter

@app.route('/')
def index():
    missions = get_current_missions()
    # 2. GENERATE THREE LAYERS OF STARS
    # Passing three different densities creates the 3D parallax effect
    return render_template_string(
        get_ui_template(), 
        missions=missions, 
        stars_css=gen_stars(400),    # Small/Distant
        stars_css_md=gen_stars(150), # Medium
        stars_css_lg=gen_stars(50)   # Large/Near
    )

@app.route('/generate')
def generate():
    fetch_missions_from_ai()
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Host 0.0.0.0 is better for Docker; Port 5001 avoids macOS AirPlay conflicts
    app.run(host="0.0.0.0", port=5001, debug=True)
