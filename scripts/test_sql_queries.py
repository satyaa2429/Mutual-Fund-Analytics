from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "bluestock_mf.db"
QUERY_PATH = BASE_DIR / "sql" / "queries.sql"


def remove_sql_comments(sql_text: str) -> str:
    """Remove lines beginning with SQL comment markers."""
    clean_lines = []

    for line in sql_text.splitlines():
        if not line.strip().startswith("--"):
            clean_lines.append(line)

    return "\n".join(clean_lines)


def main() -> None:
    sql_text = QUERY_PATH.read_text(encoding="utf-8")
    sql_text = remove_sql_comments(sql_text)

    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    print(f"Total queries found: {len(queries)}")

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        for number, query in enumerate(queries, start=1):
            print("\n" + "=" * 70)

            try:
                cursor.execute(query)
                rows = cursor.fetchmany(5)

                print(f"QUERY {number}: SUCCESS")

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("Query returned no rows.")

            except sqlite3.Error as error:
                print(f"QUERY {number}: FAILED")
                print(error)


if __name__ == "__main__":
    main()