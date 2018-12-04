from neo4j import GraphDatabase
from manipulator.private_settings import NEO4J_HOST, NEO4J_USER, NEO4J_PASS

_driver = GraphDatabase.driver(NEO4J_HOST, auth=(NEO4J_USER, NEO4J_PASS))

_session = _driver.session()


def get_driver():
    return _driver
