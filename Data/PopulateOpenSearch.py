import csv
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3
from botocore.vendored import requests

region = 'us-east-1' 
service = 'es' 
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth("#aws_key#", "#aws_secret_key#", region, service)

host = '' #Insert your host values from elastic search instance created                                            #'search-restaurants1-yyu3b45gf5jcj5iva64ghur5s-m.us-east-1.es.amazonaws.com'

es = OpenSearch(
    hosts = [{'host':host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

with open('/Users/shubh/Documents/Fall 22/Cloud/Assignment 2/Data/restaurant_details.csv', newline='') as f:
    reader = csv.reader(f)
    restaurants = list(reader)

try:
    i = 1
    for restaurant in restaurants:
        index_data = {
            'id': restaurant[0],
            'genres': restaurant[5]
        }
 
        es.index(index="restaurants",id=i, body=index_data, refresh=True) 
        i+=1

except Exception as e:
    print(e)
