#cache store logic

from typing import Optional
import os
import logging
import redis
import time

USE_REDIS = False

try:
    REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379/0")
    _client = redis.Redis.from_url(REDIS_URL)
    _client.ping() #checks if redis is available or not. 
    USE_REDIS = True
    logging.info(f"Reddis is available and will be used for caching{REDIS_URL}")

except Exception as e: 
    logging.warning(f"Redis is not available: {e}. Caching will not be used")
    USE_REDIS = False
    _client = {}

logging.info(f"Cache backend: {'Redis' if USE_REDIS else 'inMemory'}")

def _key(key:str) -> str:
    """Generate a cache key"""
    return f"Genai Cache : {key}"

def get(key:str) -> Optional[str]:
    """Get a value from the cache"""
    if USE_REDIS:
        value = _client.get(_key(key))
        return value.decode('utf-8') if value else None
    
    else:
        entry = _client.get(_key(key))      # fetch (value, expiry) tuple from dict
        if entry is None:
            return None
        
        value, expiry = entry               # unpack
        if time.time() < expiry:            # check if still fresh
            return value                    # ✅ not expired, return it
        return None                         # ❌ expired, return nothing
    
def set(key:str, value:str, ttl:int = 3600) -> None:
    """Set a value in the cache with an optional TTL"""
    if USE_REDIS:
        _client.setex(_key(key), ttl, value)  
    else:
        expiry = time.time() + ttl             
        _client[_key(key)] = (value, expiry)   