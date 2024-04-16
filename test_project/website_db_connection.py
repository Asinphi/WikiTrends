from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
import pprint

def print_dict(x):
  for i in x:
    print(f"{i} : {x[i]}")

app = Flask(__name__)
cors = CORS(app)
# con = cx_oracle.connect(user="terry.nelson", password="6G8IWcIQQsswp0Rw7hN1X6qO", dsn="")

try:
  app.config['SQLALCHEMY_DATABASE_URI'] = "oracle+cx_oracle://terry.nelson:6G8IWcIQQsswp0Rw7hN1X6qO@oracle.cise.ufl.edu:1521/orcl"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db = SQLAlchemy(app)
  # db.init_app(app)
except Exception as e:
  print("Error: ", e)

connection_string = "oracle+cx_oracle://terry.nelson:6G8IWcIQQsswp0Rw7hN1X6qO@oracle.cise.ufl.edu:1521/orcl"
# primary_key=True in every column when a table has no primary key: 
# https://docs.sqlalchemy.org/en/13/faq/ormconfiguration.html#how-do-i-map-a-table-that-has-no-primary-key:~:text=Better%20yet%20is%20when%20using%20fully%20declared%20table%20metadata%2C%20use%20the%20primary_key%3DTrue%20flag%20on%20those%20columns%3A
class Article(db.Model): 
  project = db.Column(db.String(33), primary_key=True)
  article = db.Column(db.String(33), primary_key=True)
  granularity = db.Column(db.String(33), primary_key=True)
  timestamp = db.Column(db.Integer, primary_key=True)
  access = db.Column(db.String(33), primary_key=True)
  agent = db.Column(db.String(33), primary_key=True)
  views = db.Column(db.Integer, primary_key=True)

engine = create_engine(connection_string)
try:
  connection = engine.connect()
except Exception as e:
  print("\nError: ", e)
  print("Could be bad username/password")

table_name = "einstein"
with connection:
  try:
    if connection.dialect.has_table(connection,table_name=table_name):
      print("table exists")
      query = connection.execute(text(f"select * from {table_name}"))
      # q = query.__dict___()
      # for i in q:
      #   print(i) 
      print(pprint.pformat(query.__dict__))
  except Exception as e:
    print("Something went wrong: ", e)



@app.route('/api/search')
def search():
  message = {}
  data = {}

 

  


  message['message'] = 'Hello World from Flask!'
  data['status'] = 200
  data['data'] = message
  print("\nrequest received")
  print(f"JSON data {data}")
  return jsonify(data)

if __name__ == '__main__':
  app.run(debug=True)