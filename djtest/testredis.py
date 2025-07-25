"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='xxxx.com',
    port=17038,
    decode_responses=True,
    username="default",
    password="your-password",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

