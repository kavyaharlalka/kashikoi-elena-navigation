from flask import render_template

def home():
    return render_template("index.html")

def help():
    return render_template("help.html")

def findRoute():
    pass