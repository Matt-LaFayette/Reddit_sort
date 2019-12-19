import psycopg2
import urllib.parse
import os



result = urllib.parse.urlparse("postgres://cfrpvqibrmhusu:8ad129dba1e1b695658d7d37c5b29605e10451e1215e348d5fdfad40794d5e6f@ec2-184-73-176-11.compute-1.amazonaws.com:5432/d9lk1hiqr3ehl2")

print(result)
try:
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    print(hostname)
    connection = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname
    )

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
