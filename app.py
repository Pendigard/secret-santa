from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import random

app = Flask(__name__)
app.secret_key = 'impact_blabla_secret_key' 


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)