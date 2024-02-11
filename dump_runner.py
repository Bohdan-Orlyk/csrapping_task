import datetime
import schedule
import time

from subprocess import run
from config import db_config


PGUSER = db_config.user
PGPASSWORD = db_config.password
PGDATABASE = db_config.database
PGHOST = db_config.host
PGPORT = db_config.port

BACKUP_DIR = "/app/dumps"
PARSER_DIR = "/app"


def dump_db():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{BACKUP_DIR}/db_backup_{timestamp}.dump"

    cmd = f"pg_dump -U {PGUSER} -h {PGHOST} -p {PGPORT} -d {PGDATABASE} -F c -b -v -f {backup_file}"
    run(cmd, shell=True)


def run_parser():
    cmd = f"python {PARSER_DIR}/main.py"
    run(cmd, shell=True)


schedule.every().day.at("12:00").do(run_parser)
schedule.every().day.at("12:30").do(dump_db)

while True:
    schedule.run_pending()
    time.sleep(1)
