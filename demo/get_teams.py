""" """

import os
from vaapi.client import Vaapi

client = Vaapi(
    base_url=os.environ.get("VAT_API_URL"),
    api_key=os.environ.get("VAT_API_TOKEN"),
)
my_list = client.team.list()
if my_list:
    print(my_list)

d = {team.id: team.name for team in my_list}

print()
print(d)
