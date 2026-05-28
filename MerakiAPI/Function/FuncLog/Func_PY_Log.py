import redis
import os

_redis = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))
CHANNEL = "meraki_logs"

def publish(message: str):
    """Pubblica un messaggio sul canale log."""
    _redis.publish(CHANNEL, message)

def subscribe():
    """Ritorna un subscriber per leggere i log."""
    pubsub = _redis.pubsub()
    pubsub.subscribe(CHANNEL)
    return pubsub