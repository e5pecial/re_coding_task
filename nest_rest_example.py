import requests
import json

req_link = "http://0.0.0.0:5000/parse?nest=country&currency&city"

body = json.load(open("input.json", 'r'))
request = requests.post(req_link,
                        json=body,
                        headers={"magicauth": "revolut_is_awesome"})
json_answer = json.loads(request.text)
print(json.dumps(json_answer, indent=2))
