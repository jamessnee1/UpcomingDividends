import os
import sys
import requests
import re
import json
import pandas as pd
from pandas import json_normalize

url = "https://www.marketindex.com.au/upcoming-dividends"
jsonFileName = "upcoming-dividends.json"
excelFileName = "upcoming-dividends.xlsx"

#If json file exists, delete it
if os.path.exists(jsonFileName):
    print("Deleting existing " + jsonFileName)
    os.remove(jsonFileName)
    
#If excel file exists, delete it
if os.path.exists(excelFileName):
    print("Deleting existing " + excelFileName)
    os.remove(excelFileName)

#Get MarketIndex page contents
print("Retrieving upcoming dividends table from MarketIndex...")

response = requests.get(url)

page = response.text

#Extract dividends table
yieldTable = ""

match = re.search("<upcoming-dividend-yield-table :companies=\"(.*?)\"></upcoming-dividend-yield-table>", page);

if match:
    yieldTable = match.group(1)
    
yieldTable = yieldTable.replace("&quot;", "\"")    
    
#print(yieldTable)

#Convert to json object

json_object = json.loads(yieldTable)

json_object = json.dumps(json_object, indent = 4)

with open(jsonFileName, "w") as outfile:
    outfile.write(json_object)
    
print("Written output to " + jsonFileName)

#Export json to Excel
df = pd.read_json(json_object, orient = 'list')
#remove timezones from datetimes
df['created_at'] = df['created_at'].dt.tz_localize(None)
df['updated_at'] = df['updated_at'].dt.tz_localize(None)
df.to_excel(excelFileName)

print("Written output to " + excelFileName)