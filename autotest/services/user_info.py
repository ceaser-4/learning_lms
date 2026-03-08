import redis
from students.models import Student

redis_client = redis.Redis(host='localhost', port=6379)

def get_user_profile(student_id):
    try:
        # 先去Redis找
        data = redis_client.get(f"user:{student_id}")
        if data:
            return data
    except redis.ConnectionError:
        # 如果 Redis 挂了，记录日志，并降级去查数据库 (这叫缓存容灾兜底)
        print("🚨 Redis 挂了！触发降级，正在查询数据库...")

    # 去数据里找
    return Student.objects.get(id=student_id)