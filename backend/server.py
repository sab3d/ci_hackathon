from flask import Flask
from sqlalchemy import create_engine, text
from flask_cors import CORS, cross_origin

app = Flask(__name__)

host, un, pw, port = 'conservation-intl.clqfooklvyn0.us-east-1.rds.amazonaws.com','postgres','postgres',5432 
dbname = 'vitalsigns_staging'
engine = create_engine('postgresql://{un}:{pw}@{host}:{port}/{dbname}'.format(
        un=un,
        pw=pw,
        host=host,
        port=port,
        dbname=dbname))
        
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

        
rdbname='r_output'
rengine = create_engine('postgresql://{un}:{pw}@{host}:{port}/{dbname}'.format(
        un=un,
        pw=pw,
        host=host,
        port=port,
        dbname=rdbname))

def get_csv(sql_text,engine_to_use=engine):
    sql = text(sql_text)
    result = engine_to_use.execute(sql)
    header = ",".join(result.keys())
    rows = "\n  ".join(",".join(str(v) for v in row) for row in result.fetchall())
    return header+"\n"+rows

@app.route('/fertilizer_use')
@cross_origin()
def fertilizer_use():
    sql_text = 'SELECT * from public."full_fertilizer_data"'
    return get_csv(sql_text)

@app.route('/nutrition_landscape')
@cross_origin()
def nutrition_landscape():
    sql_text = 'SELECT * from public."nutrition_landscape_query"'
    return get_csv(sql_text,rengine)

