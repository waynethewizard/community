from community import config
import psycopg2
from sql_queries import copy_table_queries


def copy_tables(cur, conn):
    """
    """
    print("Starting the copying process.")
    for query in copy_table_queries:
        print("Copying tables now...")
        cur.execute(query)
        conn.commit()
        print("Finished query.")


def main():
    """
    """
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(config.HOST, config.DBNAME, config.USER, config.PASSWORD, config.PORT))
    cur = conn.cursor()

    copy_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()