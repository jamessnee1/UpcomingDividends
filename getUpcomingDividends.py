import os
import sys
import requests
import re
import json

url = "https://www.marketindex.com.au/upcoming-dividends"

response = requests.get(url)

page = response.text

yieldTable = ""

match = re.search("<upcoming-dividend-yield-table :companies=\"(.*?)\"></upcoming-dividend-yield-table>", page);

if match:
    yieldTable = match.group(1)
    
yieldTable = yieldTable.replace("&quot;", "\"")    
    
#print(yieldTable)

json_object = json.loads(yieldTable)

json_object = json.dumps(json_object, indent=4)

with open("upcoming-dividends.json", "w") as outfile:
    outfile.write(json_object)
