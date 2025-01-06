import json
from datetime import datetime
from uuid import UUID


class DTEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is datetime object
        # convert it to a string
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.__str__()
            # return obj.hex

        if isinstance(obj, datetime):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
