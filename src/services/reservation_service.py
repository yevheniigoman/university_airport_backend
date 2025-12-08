from db.redis_client import redis_client


class ReservationService:
    @staticmethod
    def _make_key(flight_id: int, seat_number: str) -> str:
        return f"reservation:{flight_id}:{seat_number}"

    @classmethod
    def reserve_ticket(cls, flight_id: int, seat_number: str, ttl_seconds: int = 300) -> bool:
        key = cls._make_key(flight_id, seat_number)
        reserved = redis_client.setnx(key, "1")

        if reserved:
            redis_client.expire(key, ttl_seconds)

        return reserved

    @classmethod
    def is_reserved(cls, flight_id: int, seat_number: str) -> bool:
        key = cls._make_key(flight_id, seat_number)
        return redis_client.exists(key) == 1

    @classmethod
    def release_ticket(cls, flight_id: int, seat_number: str):
        key = cls._make_key(flight_id, seat_number)
        redis_client.delete(key)
