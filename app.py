from cfenv import AppEnv
from flask import Flask,render_template
from dotenv import load_dotenv
import pprint
import os
import json
from sqlalchemy import create_engine,inspect

env = AppEnv()
if env.name==None:
    print("Running locally, fetching .env file for database details")
    load_dotenv()
    local = True

else:
    print("Running on platform, loading local environment variables")
    local = False
envion_var = dict(os.environ)

try:
    services = json.loads(envion_var['VCAP_SERVICES'])
except:
    "Error loading VCAP services environment varable - have you set the correct .env files?"

database = None
try:
    for key,service in services.items():
        for item in service:
         if 'tags' in item.keys():
                if 'mysql' in item.get('tags'):
                    database = item.get('credentials')
                    print("Found database")
                    break
except:
    pass
if database!=None:
    engine = create_engine(database.get('uri').split("?")[0],echo=True)
    schema = []
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
       entry = {"TableName":table_name,"Columns":inspector.get_columns(table_name)}
       schema.append(entry)

app = Flask(__name__)






@app.route('/')
def hello_world():
    return render_template('Overview.html', local=local, width = 1)

@app.route('/env')
def envrionment():
    return pprint.pformat(dict(os.environ), width = 1)

@app.route("/nice_env")
def nice_environment():
    return render_template('FormattedEnv.html', environ=dict(os.environ), width = 1)

@app.route("/database")
def database_page():
    if database == None:
        if local:
            return "No database connected - have you set your local environment variables?"
        else:
            return "No database connected - bind to a mysql service"
    else:
        return render_template("Database.html",schema=schema)




if __name__ == '__main__':
    app.run()
