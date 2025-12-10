from models import Flight, City
from sqlalchemy.orm import Session
from db.neo4j_client import Neo4jClient
from datetime import datetime

neo4j_client = Neo4jClient()

class Route:
    def __init__(self, flights: list[Flight]):
        self.flights = flights
        self.duration = self._get_duration()

    def get_total_price(self):
        return sum(float(f.economy_price) for f in self.flights)

    def _get_duration(self):
        dep = self.flights[0].departure_time
        arr = self.flights[-1].arrival_time
        return (arr - dep).total_seconds()

    def get_waiting_time(self):
        if len(self.flights) < 2:
            return 0
        arr = self.flights[0].arrival_time
        dep = self.flights[1].departure_time
        return (dep - arr).total_seconds() / 3600

class RouteService:
    # Service for synchronizing data from MySQL to Neo4j
    # In Neo4j we maintain an airport graph where each flight is represented
    # as a separate FLIGHT relationship between Airport nodes

    @staticmethod
    def create_airport_node(airport):
        # Creates an Airport node if it does not already exist
        query = """
        MERGE (a:Airport {code: $code})
        SET a.name = $name
        """
        params = {
            "code": airport.code,
            "name": airport.name
        }
        neo4j_client.run_query(query, params)

    @staticmethod
    def add_flight_edge(flight: Flight):
        # Creates a FLIGHT relationship between two Airport nodes with all flight details
        query = """
        MATCH (dep:Airport {code: $dep_code})
        MATCH (arr:Airport {code: $arr_code})

        CREATE (dep)-[:FLIGHT {
            flight_number: $fn,
            departure_time: $dep_time,
            arrival_time: $arr_time,
            economy_price: $ep,
            business_price: $bp,
            aircraft: $aircraft
        }]->(arr)
        """

        params = {
            "dep_code": flight.dep_airport.code,
            "arr_code": flight.arr_airport.code,
            "fn": flight.flight_number,
            "dep_time": flight.departure_time.isoformat(),
            "arr_time": flight.arrival_time.isoformat(),
            "ep": float(flight.economy_price),
            "bp": float(flight.business_price),
            "aircraft": flight.aircraft.tail_number
        }

        neo4j_client.run_query(query, params)

    @classmethod
    def sync_flight_created(cls, flight: Flight):
        # Synchronizes a newly created flight from MySQL to Neo4j by creating airport nodes (if needed)
        # and inserting corresponding FLIGHT relationship
        cls.create_airport_node(flight.dep_airport)
        cls.create_airport_node(flight.arr_airport)

        cls.add_flight_edge(flight)

    @staticmethod
    def delete_flight_edge(dep_code: str, arr_code: str, flight_number: str):
        query = """
        MATCH (dep:Airport {code:$dep})-[r:FLIGHT {flight_number:$fn}]->(arr:Airport {code:$arr})
        DELETE r
        """
        params = {
            "dep": dep_code,
            "arr": arr_code,
            "fn": flight_number
        }
        neo4j_client.run_query(query, params)

    @staticmethod
    def search_routes(session: Session, from_city: City, to_city: City) -> list[list[str]]:
        from_airports = [airport.code for airport in from_city.airports]
        to_airports = [airport.code for airport in to_city.airports]

        query_direct = """
            MATCH (dep:Airport)-[f:FLIGHT]->(arr:Airport)                
            WHERE dep.code IN $from_codes AND arr.code IN $to_codes
            RETURN [f.flight_number] AS flights
        """

        query_1stop = """
            MATCH (dep:Airport)-[f1:FLIGHT]->(mid:Airport)-[f2:FLIGHT]->(arr:Airport)
            WHERE dep.code IN $from_codes AND arr.code IN $to_codes
            RETURN [f1.flight_number, f2.flight_number] AS flights
        """

        params = {
            "from_codes": from_airports,
            "to_codes": to_airports
        }

        routes = []

        direct_results = neo4j_client.run_query(query_direct, params)
        for record in direct_results:
            routes.append(record["flights"])

        stop_results = neo4j_client.run_query(query_1stop, params)
        for record in stop_results:
            routes.append(record["flights"])

        return routes