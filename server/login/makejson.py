playerinfo = {"bang": ["1234", "Jun"], "jeong": ["pqrs", "Eun"]}

import json

with open("data.json", "w") as f:
    json.dump(playerinfo, f)