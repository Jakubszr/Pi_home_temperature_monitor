import pymysql.cursors
import pymysql
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import datetime
from datetime import datetime

# connect to database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='PiTemperature',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# function to get data from DB i specified range of time
def query_to_get_rows(hours, timestamp, value, table):
    # number of rows to get with measurement in timestamp of measurement
    rows = int((hours*60)/timestamp)

    # queries to get data from database
    with connection.cursor() as cursor:
        # get outside temperature from defined number of hours
        sql = (f'SELECT {value} FROM(SELECT * FROM {table} order by\
                id desc limit {rows})Var1 ORDER by id ASC')
        cursor.execute(sql)
        query_result = cursor.fetchall()

    # list to collect data from query
    query_result_list = []
    # add data from query to list
    for i in query_result:
        query_result_list.append(i[value])

    return (query_result_list)


# function to convert list with time to readable string format
# time from query is in the datetime.timedelta format
def datatime_query(hours, timestamp, value, table):
    # get data with time from query
    time_to_convert = query_to_get_rows(hours, timestamp, value, table)
    # list to collect converted data
    readable_time = []
    # convert and add data to list
    for i in time_to_convert:
        time_in_seconds = i.seconds

        hours = int(time_in_seconds/3600)
        hours = str(hours)
        if len(hours)==1:
            hours = f'0{hours}'
        minutes = int((time_in_seconds%3600)/60)
        minutes = str(minutes)

        if len(minutes)==1:
            minutes = f'0{minutes}'

        time = f'{hours}:{minutes}'
        readable_time.append(time)

    return readable_time


# function to draw linear plot
def draw_linear_plot(xdata, ydata, xlabel, ylabel, color):
    plt.plot(xdata, ydata, color=color)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    #plt.grid(True, axis='y')
    plt.grid(True)
    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(24))
    plt.xticks(rotation=70)
    now = datetime.now()
    date_time = now.strftime("%m:%d:%Y")
    plt.savefig(f'FlaskApp/static/charts/{date_time}_{ylabel}.png',dpi=400)
    plt.close('all')

if __name__ == "__main__":

    outside_temperature = (query_to_get_rows(23, 5, 'temperature', 'outside_temperature'))
    inside_temperature = (query_to_get_rows(23, 5, 'temperature', 'inside_temperature'))
    time = datatime_query(23, 5, 'hour', 'outside_temperature')
    humidity = (query_to_get_rows(23, 5, 'humidity', 'inside_humidity'))

    draw_linear_plot(time, humidity, 'time', 'humidity', 'slateblue')
    draw_linear_plot(time, outside_temperature, 'time', 'outside temperature', 'midnightblue')
    draw_linear_plot(time, inside_temperature, 'time', 'inside temperature', 'red')
  