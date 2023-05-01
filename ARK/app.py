# import jsonify as jsify
import json
from flask import Flask,render_template,jsonify
import psycopg2
import os
from dotenv import load_dotenv
import datetime as dt
load_dotenv("local.env") 
# load_dotenv() 
app=Flask(__name__)

# @app.route('/')
# def hello():
#     return "hello world"

@app.route('/')
def index():
    connect=psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    cursor=connect.cursor()
    query='SELECT * FROM "CM_HAM_DO_AI1/Temp_value"'
    cursor.execute(query)
    query_data=cursor.fetchall()
    # print("hello")
    # print(type(data))
    # print(data)
    x_values=[]
    y_values=[]
    for x,y in query_data:
        x=x.strftime('%m/%d/%Y %H:%M:%S:%f')
        # print(x) 
        # print(type(x))
        x_values.append(x)
        y_values.append(y) 
        # print(y)
        # print(type(y))
    # cursor.commit()

    # print(x_values)
    # print(y_values)
    
    cursor.close()
    connect.close()
    return render_template('dashboard.html',x_values=x_values,y_values=y_values)

@app.route('/graph/<graph>')
def get_graph_data(graph):
  # get the data for the specified graph
  # this could be a function call that returns the data for the graph
    connect=psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    cursor=connect.cursor()
    print(graph)
    if graph=="1":
        query='SELECT * FROM "CM_HAM_DO_AI1/Temp_value"'
        name="Temperature"
        unit="Celsius"
    elif graph=="2":
        query='SELECT * FROM "CM_HAM_PH_AI1/pH_value"'
        name="pH Value"
        unit=""

    elif graph=="3":
        query='SELECT * FROM "CM_PID_DO/Process_DO"'
        name="Process Dissolved Oxygen"
        unit="%"

    else: 
        query='SELECT * FROM "CM_PRESSURE/Output"'
        name="Pressure Output"
        unit="psi"


    cursor.execute(query)
    query_data=cursor.fetchall()
    
    x_values=[]
    y_values=[]
    metadata=[]
    metadata.append(name)
    metadata.append(unit)
    
    for x,y in query_data:
        x=x.strftime('%m/%d/%Y %H:%M:%S:%f')
        x_values.append(x)
        y_values.append(y) 
       
    cursor.close()
    connect.close()
    
    #Converting x and y variables into a dictionary
    data={'x_values':x_values,'y_values':y_values,'metadata':metadata}
    # print(data)
    jd=json.dumps(data) 
    json_response=json.loads(jd)
    # print(type(json_response))
    # we convert the data dictionary to JSON and then back to a python dictionary so 
    # that we can use the jsonify function to create a Flask response object with the 
    # correct headers and formatting for returning JSON-formatted data.
    return jsonify(json_response)

if __name__=="__main__":
    host="0.0.0.0"
    # host="localhost"
    port=8888 
    debug=True
    app.run(host=host,port=8888,debug=True)
    # app.run(debug=True)
    # print(os.getenv('POSTGRES_HOST'))
    # print(os.getenv('VAR_A'))
