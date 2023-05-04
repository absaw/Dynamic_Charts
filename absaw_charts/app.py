import json
from flask import Flask, request, render_template, jsonify
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
#Getting env variables
load_dotenv("local.env")
app = Flask(__name__)

@app.route('/')
def index():
    # Connect to backed postgresql on page load
    connect = psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    cursor = connect.cursor()
    query = 'SELECT * FROM "CM_HAM_DO_AI1/Temp_value"'
    cursor.execute(query)
    #Retrieving all initial rows of temp_value table
    query_data = cursor.fetchall()

    x_values = []
    y_values = []
    for x, y in query_data:
        #Converting datetime to string
        x = x.strftime('%m/%d/%Y %H:%M:%S:%f')
        x_values.append(x)
        y_values.append(y)

    cursor.close()
    connect.close()
    # Returning x and y values to dashboard
    return render_template('dashboard.html', x_values=x_values, y_values=y_values)


@app.route('/graph/', methods=['POST'])
def get_graph_data():
  # get the data for the specified graph
    graph = request.json.get('graph')
    start = request.json.get('start')
    end = request.json.get('end')
    
    connect = psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    cursor = connect.cursor()
    if graph == 1:
        if start == 0 and end == 0:
            #When we just need to load the whole graph
            query = 'SELECT * FROM "CM_HAM_DO_AI1/Temp_value"'
        else:
            #When we need to retrieve specific time period
            date_format = "%m/%d/%Y %H:%M:%S:%f"
            start = datetime.strptime(start, date_format)
            end = datetime.strptime(end, date_format)
            query = f"SELECT * FROM \"CM_HAM_DO_AI1/Temp_value\" WHERE time >= '{start}' AND time <= '{end}'"
        name = "Temperature"
        unit = "Celsius"
    elif graph == 2:
        if start == 0 and end == 0:
            query = 'SELECT * FROM "CM_HAM_PH_AI1/pH_value"'
        else:
            date_format = "%m/%d/%Y %H:%M:%S:%f"
            start = datetime.strptime(start, date_format)
            end = datetime.strptime(end, date_format)
            query = f"SELECT * FROM \"CM_HAM_PH_AI1/pH_value\" WHERE time >= '{start}' AND time <= '{end}'"
        name = "pH Value"
        unit = ""

    elif graph == 3:
        if start == 0 and end == 0:
            query = 'SELECT * FROM "CM_PID_DO/Process_DO"'
        else:
            date_format = "%m/%d/%Y %H:%M:%S:%f"
            start = datetime.strptime(start, date_format)
            end = datetime.strptime(end, date_format)
            query = f"SELECT * FROM \"CM_PID_DO/Process_DO\" WHERE time >= '{start}' AND time <= '{end}'"
        name = "Process Dissolved Oxygen"
        unit = "%"

    else:
        if start == 0 and end == 0:
            query = 'SELECT * FROM "CM_PRESSURE/Output"'
        else:
            date_format = "%m/%d/%Y %H:%M:%S:%f"
            start = datetime.strptime(start, date_format)
            end = datetime.strptime(end, date_format)
            query = f"SELECT * FROM \"CM_PRESSURE/Output\" WHERE time >= '{start}' AND time <= '{end}'"
        name = "Pressure Output"
        unit = "psi"

    cursor.execute(query)
    query_data = cursor.fetchall()

    x_values = []
    y_values = []
    metadata = []
    metadata.append(name)
    metadata.append(unit)

    for x, y in query_data:
        x = x.strftime('%m/%d/%Y %H:%M:%S:%f')
        x_values.append(x)
        y_values.append(y)

    cursor.close()
    connect.close()

    # Converting x and y variables into a dictionary
    data = {'x_values': x_values, 'y_values': y_values, 'metadata': metadata}
    # print(data)
    jd = json.dumps(data)
    json_response = json.loads(jd)
    # we convert the data dictionary to JSON and then back to a python dictionary so
    # that we can use the jsonify function to create a Flask response object with the
    # correct headers and formatting for returning JSON-formatted data.
    return jsonify(json_response)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8888
    debug = False
    app.run(host=host, port=8888, debug=debug)
