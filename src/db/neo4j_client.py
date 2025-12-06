from neo4j import GraphDatabase
from config import get_settings

settings = get_settings()


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def run_query(self, query: str, parameters: dict = None):
        with self.driver.session() as session:
            return session.run(query, parameters or {}).data()

