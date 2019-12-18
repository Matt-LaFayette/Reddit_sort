import psycopg2

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE DATABASE t
        """,
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """
        COMMIT
        """
        )




try:
    connection = psycopg2.connect(user = "cfrpvqibrmhusu",
                                  password = "8ad129dba1e1b695658d7d37c5b29605e10451e1215e348d5fdfad40794d5e6f",
                                  host = "ec2-184-73-176-11.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "d9lk1hiqr3ehl2")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
