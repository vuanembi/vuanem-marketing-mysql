import os
from dataclasses import dataclass


@dataclass
class Connection:
    host: str
    user: str
    password: str
    database: str = "vuanem_ecommerce"


magento_connection = Connection(
    os.getenv("M_MYSQL_HOST", ""),
    os.getenv("M_MYSQL_UID", ""),
    os.getenv("M_MYSQL_PWD", ""),
)
laravel_connection = Connection(
    os.getenv("L_MYSQL_HOST", ""),
    os.getenv("L_MYSQL_UID", ""),
    os.getenv("L_MYSQL_PWD", ""),
)
