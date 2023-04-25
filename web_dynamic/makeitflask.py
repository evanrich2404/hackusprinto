#!/usr/bin/python3
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run(debug=True)
