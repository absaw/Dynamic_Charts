# Dynamic_Charts Project

## Introduction

In this project, I got the chance to demonstrate my proficiency in Python, building a simple web-based dashboard to visualize real-time process data originating from one of the bioreactors.

The data is taken from Bioreactors. These bioreactors are purpose-built for cultivated meat, with a mission to 100x the industry’s capacity by 2035. The Data Systems team in these bioreactors is generally responsible for everything from production, model-based control software to web-based data monitoring applications. This project is to demonstrate my abilities in this domain


## Screenshots

<img src="https://github.com/absaw/Dynamic_Charts/blob/main/absaw_charts/screenshots/ss2.png">
<img src="https://github.com/absaw/Dynamic_Charts/blob/main/absaw_charts/screenshots/ss3.png">
<img src="https://github.com/absaw/Dynamic_Charts/blob/main/absaw_charts/screenshots/ss4.png">
<img src="https://github.com/absaw/Dynamic_Charts/blob/main/absaw_charts/screenshots/ss5.png">
<img src="https://github.com/absaw/Dynamic_Charts/blob/main/absaw_charts/screenshots/ss6.png">
<img src="https://github.com/absaw/Dynamic_Charts/blob/main/absaw_charts/screenshots/ss7.png">

## Technical Details

In this directory, you'll find a `Dockerfile` that defines the image your code will be copied into and installed in. Specifically, your source code will be installed into a Python 3.10 virtual environment as a package via pip, along with any dependencies you've specified in a `requirements.txt` file.

You'll also find a `compose.yaml` file that defines the container that'll be used to run your code. Specifically, to serve your web-based dashboard in a local browser at http://localhost:8888/, Docker is configured to start the container by executing `run-app`, the expected [entrypoint](https://setuptools.pypa.io/en/latest/userguide/entry_point.html) for your application.

### The database

The data I will be visualizing is in a Postgres database, also configured in `compose.yaml`. Credentials to access this database are confidential at the moment. But the file can be used to use another database and configure it.

- `POSTGRES_HOST` provides the host
- `POSTGRES_PORT` provides the port
- `POSTGRES_USER` provides the user
- `POSTGRES_PASSWORD` provides the password
- `POSTGRES_DB` provides the database

An example can be found in `local.env`. Note that these will be subject to change, so make sure not to hard code these.

### The data

The tables in the database:

```
brx1=# \dt
                      List of relations
 Schema |           Name           | Type  |      Owner   
--------+--------------------------+-------+------------------
 public | CM_HAM_DO_AI1/Temp_value | table | process_trending
 public | CM_HAM_PH_AI1/pH_value   | table | process_trending
 public | CM_PID_DO/Process_DO     | table | process_trending
 public | CM_PRESSURE/Output       | table | process_trending
```

Each table has the same schema, like so:

```
brx1=# \d public."CM_HAM_DO_AI1/Temp_value"
                Table "public.CM_HAM_DO_AI1/Temp_value"
 Column |            Type             | Collation | Nullable | Default 
--------+-----------------------------+-----------+----------+---------
 time   | timestamp without time zone |           |          | 
 value  | double precision            |           |          | 
```

Each table contains the following data:

| Table                    | Name             | Units   |
| ------------------------ | ---------------- | ------- |
| CM_HAM_DO_AI1/Temp_value | Temperature      | Celsius |
| CM_HAM_PH_AI1/pH_value   | pH               | n/a     |
| CM_PID_DO/Process_DO     | Distilled Oxygen | %       |
| CM_PRESSURE/Output       | Pressure         | psi     |

### How to test the code

Run `docker compose up` and navigate your browser to http://localhost:8888/. That's it!

## Conclusion

The dashboard allows the user to plot each of these four series (Temperature, pH, Distilled Oxygen, and Pressure) over time.

### Checkpoints

- Package installs successfully
- Dashboard can be viewed at http://localhost:8888/. It looks good
- Code is high quality, e.g. It follows PEP8. It is it fully type annotated,and there are comments

### Bonus features

- User can select the time window
- Added a button to refresh the data without refreshing the page, or auto-refresh the page for the user
- Added a "Download as csv" button for the specific time period
