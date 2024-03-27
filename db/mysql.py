from io import StringIO

from paramiko import RSAKey
import pymysql
from sshtunnel import SSHTunnelForwarder

from secret_manager import get_secret

LOCALHOST = "127.0.0.1"
SSH_PORT = 22
MYSQL_PORT = 3306

SSH_HOST = "34.87.148.108"
DB_HOST = "10.16.208.8"


def get(query: str):
    ssh_pkey = RSAKey.from_private_key(
        StringIO(get_secret("salescall-ssh-key")),
        get_secret("salescall-ssh-passphrase"),
    )

    tunnel = SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username="bivuanem",
        ssh_pkey=ssh_pkey,
        remote_bind_address=(DB_HOST, MYSQL_PORT),
    )

    tunnel.start()

    with pymysql.connect(
        host=LOCALHOST,
        port=tunnel.local_bind_port,
        user="bi-salecalls",
        database="webhook",
        password=get_secret("salescall-db-password"),
        cursorclass=pymysql.cursors.DictCursor,
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()

    tunnel.close()

    return data
