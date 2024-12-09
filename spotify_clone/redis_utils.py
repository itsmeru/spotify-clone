import redis

class RedisUtils:
    def __init__(self):
        self.redis = redis.StrictRedis(host="redis", port=6379, db=0)

    def set_verification_code(self, user_id: str, code: str, expires: int = 604800):
        key = f"reset_pwd_{user_id}"
        return self.redis.setex(key, expires, code)
        
    def get_verification_code(self, user_id: str):
        key = f"reset_pwd_{user_id}"
        value = self.redis.get(key)
        return value.decode() if value else None
        
    def delete_verification_code(self, user_id: str):
        key = f"reset_pwd_{user_id}"
        self.redis.delete(key)