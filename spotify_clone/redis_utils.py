import redis

class RedisUtils:
    def __init__(self):
        self.redis = redis.StrictRedis(host="redis", port=6379, db=0)

    def set_verification_code(self, email: str, code: str, expires: int = 300):
        key = f"reset_pwd_{email}"
        return self.redis.setex(key, expires, code)
        
    def get_verification_code(self, email: str) -> str:
        key = f"reset_pwd_{email}"
        value = self.redis.get(key)
        return value.decode() if value else None
        
    def delete_verification_code(self, email: str):
        key = f"reset_pwd_{email}"
        self.redis.delete(key)