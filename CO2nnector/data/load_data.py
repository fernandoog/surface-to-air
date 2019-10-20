# Load the Pandas libraries with alias 'pd' 
import glob, os
import pandas as pd 
import sqlite3
import json
import datetime



# Guardamos DF into sqlite
def set_df_to_sqlite(cursor, df, table_name):
	query_check_table = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';".format(table_name=table_name)

	query = cur.execute(query_check_table)
	df.to_sql(table_name, conn, if_exists='append', index=False)

# Check if table not exists
def check_table_not_exists(cursor, table_name):
	query_check_table = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';".format(table_name=table_name)
	query = cursor.execute(query_check_table)
	results = query.fetchall()

	not_exist = table_name not in [x[0] for x in results]

	return not_exist


# dir_raw_data = 'raw_data/'


conn = sqlite3.connect("database.db")
cur = conn.cursor()


# AirQualtySystem/AirQualitySystem.csv
TABLE_NAME = 'AirQualitySystem'

if check_table_not_exists(cur, TABLE_NAME):

	DIR_DATA = 'raw_data/AirQualtySystem/'
	file = 'AirQualitySystem.csv'
	print ('Cargando tabla {}'.format(TABLE_NAME))

	df = pd.read_csv(DIR_DATA+file)
	set_df_to_sqlite(cur, df, TABLE_NAME)


# Datos AOD_DATA
TABLE_NAME = 'AOD_DATA'

if check_table_not_exists(cur, TABLE_NAME):
	print ('Cargando tabla {}'.format(TABLE_NAME))

	DIR_DATA = 'raw_data/AOD_DATA/'
	# os.chdir(DIR_DATA)
	files =  glob.glob(DIR_DATA+"*[Ll][Oo][Ss]*")
	files = [x.replace(DIR_DATA, '') for x in files]


	# lYYYY, MM, DD, Latitude, Longitude, AOD1, AOD3, STD3
	HEADERS = ['YYYY', 'MM', 'DD', 'Latitude', 'Longitude', 'AOD1', 'AOD3', 'STD3']


	dfs = []
	for file in files:
		df_single = pd.read_csv(DIR_DATA+file, index_col=False, header=None, names=HEADERS)
		dfs.append(df_single)

	df = pd.concat(dfs)

	set_df_to_sqlite(cur, df, TABLE_NAME)


# Datos MERRA2
TABLE_NAME = 'MERRA2'

if check_table_not_exists(cur, TABLE_NAME):
	print ('Cargando tabla {}'.format(TABLE_NAME))

	DIR_DATA = 'raw_data/MERRA2/'
	# os.chdir(DIR_DATA)
	files =  glob.glob(DIR_DATA+"*")
	files = [x.replace(DIR_DATA, '') for x in files]

	dfs = []
	for file in files:
		df_single = pd.read_csv(DIR_DATA+file)
		dfs.append(df_single)

	df = pd.concat(dfs)

	set_df_to_sqlite(cur, df, TABLE_NAME)


# Datos Reference_Monitor_Data
TABLE_NAME = 'Reference_Monitor_Data'

if check_table_not_exists(cur, TABLE_NAME):

	DIR_DATA = 'raw_data/Reference_Monitor_Data/'
	file = 'LosAngeles.csv'
	print ('Cargando tabla {}'.format(TABLE_NAME))

	df = pd.read_csv(DIR_DATA+file)
	set_df_to_sqlite(cur, df, TABLE_NAME)


# Datos Reference_Monitor_Data
TABLE_NAME = 'VisualData'

# if check_table_not_exists(cur, TABLE_NAME):

# Normalizamos datos de nasa para visualizar
if False:
	print ('Cargando tabla {}'.format(TABLE_NAME))


	


	query_str = "SELECT * FROM Reference_Monitor_Data WHERE parameter=='pm25';"
	df_rmd = pd.read_sql_query(query_str, conn)
	# df = df_rmd.loc[:, ['date', 'coordinates' 'value']]

	# '{utc=2017-08-11T00:00:00.000Z, local=2017-08-10T16:00:00-08:00}'
	date = [datetime.datetime.strptime(x[1:-1].split(',')[0][4:], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() for x in df_rmd.date]

	# {latitude=34.136475, longitude=-117.923965}
	latitude =[float(x[1:-1].split(',')[0][9:]) for x in df_rmd.coordinates]
	longitude =[float(x[1:-1].split(',')[1][11:]) for x in df_rmd.coordinates]
	value = df_rmd.value

	columns = ['TIME, LAT, LON, VALUE']
	df = pd.DataFrame()
	df['time'] = date
	df['latitude'] = latitude
	df['longitude'] = longitude
	df['value'] = value


	set_df_to_sqlite(cur, df, TABLE_NAME)
	# save to db


# Creamos tabla de datos de sensor
if False:
	print("Creando tabla sensor")


	df = pd.DataFrame(columns=('time', 'latitude', 'longitude', 'value'))
	set_df_to_sqlite(cur, df, 'VisualData_Sensor')


