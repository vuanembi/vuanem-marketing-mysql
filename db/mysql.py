from typing import Any, Callable

from sshtunnel import SSHTunnelForwarder
import pymysql.cursors

from marketing import config

LOCALHOST = "localhost"
SSH_PORT = 22
MYSQL_PORT = 3306


def get(
    db_config: config.DBConfig,
    port_fn: Callable[[], int] = lambda: MYSQL_PORT,
    callback: Callable[[], None] = None,
):
    def _get(query: str) -> list[dict[str, Any]]:
        with pymysql.connect(
            host=db_config.host,
            port=port_fn(),
            user=db_config.user,
            password=db_config.pwd,
            database=db_config.db,
            cursorclass=pymysql.cursors.DictCursor,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
        if callback:
            callback()
        return data

    return _get


def _get_ssh_port(tunnel: SSHTunnelForwarder):
    def _get():
        tunnel.start()
        return tunnel.local_bind_port

    return _get


def get_ssh(db_ssh_config: config.DBSSHConfig):
    tunnel = SSHTunnelForwarder(
        (db_ssh_config.host, SSH_PORT),
        ssh_username=db_ssh_config.ssh_user,
        ssh_password=db_ssh_config.ssh_pwd,
        remote_bind_address=(LOCALHOST, MYSQL_PORT),
    )
    return get(
        config.DBConfig(
            LOCALHOST,
            db_ssh_config.user,
            db_ssh_config.pwd,
            db_ssh_config.db,
        ),
        _get_ssh_port(tunnel),
        tunnel.close,
    )
