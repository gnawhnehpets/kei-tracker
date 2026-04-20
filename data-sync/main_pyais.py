import json
from pyais.stream import TCPConnection

ship_list = {"257711000", "230028670", "563612000", "431028748", "230028670"}

def default_serializer(obj):
    if isinstance(obj, bytes):
        return obj.hex()
    # enums, IntEnums, etc.
    if hasattr(obj, 'value'):
        return obj.value
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

for msg in TCPConnection('153.44.253.27', port=5631):
    decoded = msg.decode()
    if decoded.msg_type != 1:
        continue
    print(json.dumps(vars(decoded), default=default_serializer))