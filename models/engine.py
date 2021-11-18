import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine


def get_engine(user: str, pwd: str, host: str, db: str = "vuanem_ecommerce") -> Engine:
    return create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username=user,
            password=pwd,
            host=host,
            database=db,
        )
    )


magento_engine = get_engine(
    os.getenv("M_MYSQL_UID", ""),
    os.getenv("M_MYSQL_PWD", ""),
    os.getenv("M_MYSQL_HOST", ""),
)
laravel_engine = get_engine(
    os.getenv("L_MYSQL_UID", ""),
    os.getenv("L_MYSQL_PWD", ""),
    os.getenv("L_MYSQL_HOST", ""),
)
