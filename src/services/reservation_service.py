from db.redis_client import redis_client

class ReservationService():
    def _make_key(self, flight_ig: int, seat_number: str) -> str:
        return f"reservation:{flight_ig}:{seat_number}"

    def reserve_ticket(self, flight_id: int, seat_number: str, ttl_seconds: int = 300) -> bool:

        key = self._make_key(flight_id, seat_number)
        reserved = redis_client.setnx(key, "1")

        if reserved:
            redis_client.expire(key, ttl_seconds)

        return reserved

    def is_reserved(self, flight_id: int, seat_number: str) -> bool:
        key = self._make_key(flight_id, seat_number)
        return redis_client.exists(key) == 1

    def release_ticket(self, flight_id: int, seat_number: str):
        key = self._make_key(flight_id, seat_number)
        redis_client.delete(key)



