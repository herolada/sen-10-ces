""" from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/hello')
def hello_world():
   return "Hello World"

if __name__ == '__main__':
   app.run(debug = True) """

def test(input_var):
   if input_var:
      print(input_var)
   else:
      raise Exception