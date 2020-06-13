import json
import boto3
import requests
from decimal import *

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1') 
    table = dynamodb.Table('Visitors')

    headers = event["headers"]
    ip_address = headers["X-Forwarded-For"]
    ip_array = ip_address.split(',')
    ip_address = ip_array[0]

    req = requests.get(f'http://ip-api.com/json/{ip_address}')
    location_data = req.json()
    
    table.put_item(Item={'IpAddress': ip_address, 'City': location_data["city"], "Lat": Decimal(str(location_data["lat"])), "Lon": Decimal(str(location_data["lon"])),})
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success"
        }),
    }
