"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-17038.c341.af-south-1-1.ec2.redns.redis-cloud.com',
    port=17038,
    decode_responses=True,
    username="default",
    password="dy2LDCKKD0z3c0T1FB66RtIN4piEuTqR",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

