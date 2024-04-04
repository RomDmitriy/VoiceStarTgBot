import redis
from os import getenv

host = getenv("REDIS_HOST", "localhost")
port = getenv("REDIS_PORT", 6379)
db = getenv("REDIS_DB_INDEX", 1)

redisServer = redis.Redis(host=host, port=port, db=db, decode_responses=True)
