"""
Database configuration: reads .env and provides SQLAlchemy engine for MSSQL (SQL Server).
Uses pyodbc for native support of named instances (e.g. SERVER\\SQLEXPRESS).
"""
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Load .env from project root
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)


def get_engine():
    """
    Build SQLAlchemy engine from environment variables.
    Expects: DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD.

    Returns:
        sqlalchemy.Engine: MSSQL engine.
    """
    server = os.getenv("DB_SERVER")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    missing = [
        k
        for k, v in [
            ("DB_SERVER", server),
            ("DB_NAME", name),
            ("DB_USER", user),
            ("DB_PASSWORD", password),
        ]
        if not v
    ]
    if missing:
        raise ValueError(f"Missing required env vars: {', '.join(missing)}")

    # pyodbc supports server\instance format; driver required on Windows
    driver = "ODBC Driver 17 for SQL Server"
    params = quote_plus(f"DRIVER={{{driver}}};SERVER={server};DATABASE={name};UID={user};PWD={password}")
    url = f"mssql+pyodbc://?odbc_connect={params}"

    try:
        engine = create_engine(url, pool_pre_ping=True)
        return engine
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to create database engine: {e}") from e
