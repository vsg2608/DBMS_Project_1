from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "<b>Hello World</b> <br> How are you???"
   

if __name__ == '__main__':
   app.run()