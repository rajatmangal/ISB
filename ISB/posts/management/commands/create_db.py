import sys
import logging
#import MySQLdb
import psycopg2

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

rds_host = 'isb-db.cluster-cdl4akxmgbw3.us-east-1.rds.amazonaws.com'
db_name = 'postgres'
user_name = 'postgres'
password = 'password'
port = 5432

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Creates the initial database'

    def handle(self, *args, **options):
        print('Starting db creation')
        try:
            db = psycopg2.connect(host=rds_host, database=db_name, user=user_name,
                                 password=password, port= port,connect_timeout=50)
            c = db.cursor()
            print("connected to db server")
            c.execute("END; CREATE DATABASE isb;")
            db.commit()
            c.execute(
                "GRANT ALL PRIVILEGES ON db_name.* TO 'postgres' IDENTIFIED BY 'Momdad1998';")
            db.commit()
            c.close()
            print("closed db connection")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        # except:
        #     logger.error(
        #         "ERROR: Unexpected error: Could not connect to MySql instance.")
        #     sys.exit()