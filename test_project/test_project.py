import requests
import json
import pandas
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, inspect
from sqlalchemy.schema import CreateSchema
import os


user_name = None
user_password = None
server = 'oracle.cise.ufl.edu'
database = '?service_name=orcl'
port = '1521'

###############################################################################
# Enter username password
###############################################################################

project_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_root, 'credentials.txt')   
if os.path.isfile(config_path):
    with open(config_path,"r") as f:
        for line in f:
            if "user" in line:
                user_name = line.split("=")[-1].strip()
                continue
            if "password" in line:
                user_password = line.split("=")[-1].strip()
if user_name in [None, ""] or user_password in [None, ""]:
    user_name = input("Enter Username: ") 
    user_password = input("Enter Password: ")
    
###############################################################################
# Connect to oracle
###############################################################################

while True:
    try:
        connection_string = f'oracle+cx_oracle://{user_name}:{user_password}@{server}:{port}/{database}'
        engine = create_engine(connection_string)
        engine.connect()
        with open(config_path, "w") as f:
            f.write(f"user={user_name}\n")
            f.write(f"password={user_password}")
        print("Engine successfully created: ", engine)
        break
    except Exception as e:
            print("\nError:", e)
            print("If module not found error refer to readme for instructions. oracle sucks")
            print("\nIf not, try username and password again")
            user_name = input("Enter Username: ") 
            user_password = input("Enter Password: ")
            

###############################################################################
# Get dataframe from wikipedia
###############################################################################

url = 'https://wikimedia.org/'
pageviews_access = 'api/rest_v1/metrics/pageviews/'
endpoint = url + pageviews_access + 'per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/2015100100/2015103100'

headers = {
    'User-Agent' : 'School Project',
    'Accept' : 'application/json',
}

response_API = requests.get(endpoint, headers=headers)
if (response_API.status_code != 200):
    print("No response from API. Return Code: " , response_API.status_code)
else:
    # request sucessful
    data = response_API.json()
    df = pandas.DataFrame(data['items'])
    df = df.rename(columns={"project": "project_", "article": "article_", "timestamp": "timestamp_", "access": "access_", "agent": "agent_"})
    print(df)

###############################################################################
# Insert data into database
###############################################################################

# create loop to insert all values
table_name = 'Einstein'
table = f"CREATE TABLE {table_name} (project_ varchar(33), article_ varchar(33), granularity varchar(33), timestamp_ int, access_ varchar(33), agent_ varchar(33), views int)"
insert = f"insert into Einstein (project_, article_, granularity, timestamp_, access_, agent_, views) values('en.wikipedia','Albert_Einstein', 'daily', '2015100100', 'all-access', 'all-agents', '18860')"


try:
    with engine.connect() as connection:
        if connection.dialect.has_table(connection,table_name=table_name):
            print("Table already exists. Dropping table")
            connection.execute(text(f"drop table {table_name}"))
        connection.execute(text(table))
        connection.execute(text(insert))
        connection.commit()
        print("Data successfully inserted into the database.")
except Exception as e:
    print("Error inserting table into database:\n", e)


