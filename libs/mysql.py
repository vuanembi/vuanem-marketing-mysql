from sqlalchemy.engine import Engine


def get(engine: Engine, query: str) -> list[dict]:
    with engine.connect() as conn:
        results = conn.execute(query)
        return [dict(zip(results.keys(), result)) for result in results.fetchall()]
