"""
Extract gold schema views to local data/ folder.
Uses get_engine() to query DB; exports as parquet (fallback: csv).
"""
import sys
from pathlib import Path

import pandas as pd

# Add project root to path
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root))

from src.database_config import get_engine

DATA_DIR = _project_root / "data"
GOLD_VIEWS = ["product_reports", "customer_reports"]
SCHEMA = "gold"
FORMAT = "parquet"  # or "csv"


def extract_view(engine, view: str, fmt: str = FORMAT) -> Path:
    """Query [gold].[view] and save to data/gold.{view}.{ext}."""
    query = f"SELECT * FROM [{SCHEMA}].[{view}]"
    df = pd.read_sql(query, engine)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".parquet" if fmt == "parquet" else ".csv"
    path = DATA_DIR / f"gold.{view}{ext}"

    if fmt == "parquet":
        df.to_parquet(path, index=False)
    else:
        df.to_csv(path, index=False)

    return path


def main():
    try:
        engine = get_engine()
    except (ValueError, RuntimeError) as e:
        print(f"DB config error: {e}")
        sys.exit(1)

    for view in GOLD_VIEWS:
        try:
            path = extract_view(engine, view, FORMAT)
            print(f"Exported: {path}")
        except Exception as e:
            print(f"Error exporting {view}: {e}")
            raise

    print("Extract complete.")


if __name__ == "__main__":
    main()
