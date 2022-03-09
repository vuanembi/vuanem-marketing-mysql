import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    user: str
    pwd: str
    db: str


@dataclass
class DBSSHConfig(DBConfig):
    ssh_user: str
    ssh_pwd: str


laravel_db = DBConfig(
    os.getenv("LARAVEL_HOST", ""),
    os.getenv("LARAVEL_USER", ""),
    os.getenv("LARAVEL_PWD", ""),
    "vuanem_ecommerce",
)

webhook_db = DBSSHConfig(
    os.getenv("WEBHOOK_HOST", ""),
    os.getenv("WEBHOOK_USER", ""),
    os.getenv("WEBHOOK_PWD", ""),
    "webhook",
    os.getenv("WEBHOOK_SSH_USER", ""),
    os.getenv("WEBHOOK_SSH_PWD", ""),
)
