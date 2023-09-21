from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__,static_url_path='/templates', static_folder='templates',template_folder='templates')

# Routes
@app.get('/')
def home():
    return send_from_directory("templates",'home.html')

if __name__ == '__main__':
    app.run(debug=True,port=80)
