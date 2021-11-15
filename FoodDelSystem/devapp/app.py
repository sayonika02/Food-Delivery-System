from flask import Flask, render_template
#import psycopg2 #pip install psycopg2 
#import psycopg2.extras

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)

