import requests
import os

base_url=os.environ.get("VAT_API_URL"),
api_key=os.environ.get("VAT_API_TOKEN"),

# specify a file you want to upload
files = {'file': open('test-upload.h5', 'rb')} 
headers ={"Authorization":f"Token {api_key[0]}"}

response = requests.post(url=f"{base_url[0]}api/upload/model/",files=files,headers=headers)

print(response.text)