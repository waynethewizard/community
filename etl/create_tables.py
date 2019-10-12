from community import config
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """ 
    Drops table if exists.
  
    Parameters: 
    cur: db cursor
    conn: postgre connection   
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ 
    Create table for each queries.
  
    Parameters: 
    cur: db cursor
    conn: postgre connection   
    """
    for query in create_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Issue creating table: " + query)
            print(e)
    print("Tables created successfully.")


def main():

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(config.HOST, config.DBNAME, config.USER, config.PASSWORD, config.PORT))
    cur = conn.cursor()

    drop_tables(cur, conn)
    print("Creating tables now...")
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
