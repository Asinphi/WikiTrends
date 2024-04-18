from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
import pprint
import json

def print_dict(x):
  for i in x:
    print(f"{i} : {x[i]}")

app = Flask(__name__)
cors = CORS(app)
connection_string = "oracle+cx_oracle://terry.nelson:6G8IWcIQQsswp0Rw7hN1X6qO@oracle.cise.ufl.edu:1521/orcl"

@app.route('/api/search')
def search():
  message = {}
  data = {}

  query_as_dict = {}
  # enter any table name
  try:
    app.config['SQLALCHEMY_DATABASE_URI'] = "oracle+cx_oracle://terry.nelson:6G8IWcIQQsswp0Rw7hN1X6qO@oracle.cise.ufl.edu:1521/orcl"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    # db.init_app(app)
  except Exception as e:
    print("Error: ", e)

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
        query = connection.execute(text(f"select * from {table_name}")).fetchall()
        query = [tuple(row) for row in query]
        # q = query.__dict___()
        # for i in q:
        #   print(i) 
        print("Changing to JSON")
        print(type(query))
        print(json.dumps(query))
        query_as_dict = json.dumps(query)
        print("Printing JSON")
        print(pprint.pformat(query_as_dict))
        return jsonify(query_as_dict)

    except Exception as e:
      print("Something went wrong: ", e)
  

  # print(pprint.pformat(query_as_dict))
  # return jsonify(query_as_dict)
  message['message'] = 'Hello World from Flask!'
  data['status'] = 200
  data['data'] = message
  print("\nrequest received")
  print(f"JSON data {data}")
  return jsonify(message)

if __name__ == '__main__':
  app.run(debug=True)