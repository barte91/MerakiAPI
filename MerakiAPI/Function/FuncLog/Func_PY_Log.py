import os
import queue
import logging

REDIS_URL = os.environ.get("REDIS_URL")  # presente solo in Docker

if REDIS_URL:
    # ── MODALITÀ DOCKER → Redis ──────────────────────────────
    import redis
    _redis = redis.from_url(REDIS_URL)
    CHANNEL = "meraki_logs"
    USE_REDIS = True

    def publish(message: str):
        _redis.publish(CHANNEL, message)

    def subscribe():
        pubsub = _redis.pubsub()
        pubsub.subscribe(CHANNEL)
        return pubsub

else:
    # ── MODALITÀ LOCALE → Queue in memoria ───────────────────
    USE_REDIS = False
    log_queue = queue.Queue()

    def publish(message: str):
        log_queue.put(message)

    def subscribe():
        return None  # non usato in locale