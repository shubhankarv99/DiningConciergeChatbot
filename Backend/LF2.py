

##################################################################################


import json
import boto3
import random
from opensearchpy import OpenSearch, RequestsHttpConnection
from boto3.dynamodb.conditions import Key, Attr
from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
    
    sns = boto3.client("sns")
    sqs = boto3.client("sqs")
    dynamodb = boto3.resource("dynamodb")
    queue_url = ""

    access_key  = ""
    secret_key  = ""
    
    #URL of Elastic search
    host        = “”
    region      = "us-east-1"
    service     = "es"
    

    awsauth = AWS4Auth (
        access_key, 
        secret_key, 
        region, 
        service
    )


    openSearch = OpenSearch(
                                hosts = [
                                    {
                                        'host': host, 
                                        'port': 443
                                    }
                                ],
                                http_auth           = awsauth, 
                                use_ssl             = True,
                                verify_certs        = True, 
                                connection_class    = RequestsHttpConnection
                            )

    resp = sqs.receive_message(
        QueueUrl                = queue_url,
        MaxNumberOfMessages     = 1,
        MessageAttributeNames   = ['All'],
        VisibilityTimeout       = 0,
        WaitTimeSeconds         = 0
    )

 
    message         = resp['Messages'][0]
    messageAttributes = message['MessageAttributes']
    
    print("messageAttributes: ",messageAttributes)
    
    cuisine         = messageAttributes['Cuisine']['StringValue']
    email         = messageAttributes['Email']['StringValue']
    time         = messageAttributes['Time']['StringValue']
    
    #time            = message['MessageAttributes'].get('Time').get('StringValue')
    # date          = message['MessageAttributes'].get('Date').get('StringValue')
    #number          = message['MessageAttributes'].get('Number').get('StringValue')
    #modifiedNumber  = "+1{}".format(number)
    #email           = message['MessageAttributes'].get('Email').get('StringValue')


    result = openSearch.search (
        index   = "restaurants", 
        body    = {
            "query": 
                {
                    "match" : {
                        "genres" : cuisine
                    }
                }
            }
        )
    
  
    candidate_list, ids = [], []
    print(result['hits']['hits'])
    
    ids = result['hits']['hits']
    
    # Create every restaurant indexed from OpenSearch
    for entry in result['hits']['hits']:
      candidate_list.append(entry["_source"])
    
    print("candidate_list: ",candidate_list)
    
    ids_2= list(map(lambda x: x['id'], candidate_list))
    
    print("ids_2: ",ids_2)

    #for entry in result['hits']['hits']:
      #candidate_list.append(entry["_source"])


    #for c in candidate_list:
      #ids.append(c.get("Business ID"))
    


    #restaurantSuggestion = random.choice(ids)


    db_table = dynamodb.Table('yelp-restaurants')
    
    finalMessage    = "Hi! Here are your suggestions \n"
    
    for rest_id in ids_2:
        info = db_table.get_item(
            Key = {
                'id': rest_id
            }
        )
        info_Item = info['Item']
        print("info_Item: ",info_Item)
        Rating          = info_Item["rating"]
        Name            = info_Item["name"]
        RatingCount     = info_Item["review_count"]
        Address         = info_Item["address"]
        Address         = ''.join(list(Address))
        finalMessage += Name + Rating + Address + "\n"
        
        
    #""".format(Name, time, RatingCount, Rating, Address)

    
    

    print("finalMessage: ",finalMessage)
    
    def sendEmail(message):
        # This address must be verified with Amazon SES.
        SENDER = "shreyadesai1202@gmail.com"
        RECIPIENT = email
        AWS_REGION = "us-east-1"
        CUISINE=cuisine
        #PEOPLE=message['people']['stringValue']
        # The subject line for the email.
        SUBJECT = "Restaurant Recommendations for you!"
        #
        #
        #DATE=recommendationRequest['date']['stringValue']
        #TIME=message['time']['stringValue']
        
            
        # The email body for recipients with non-HTML email clients.
        #BODY_TEXT = "Hello! Here are my " + str(CUISINE) + " restaurant suggestions for " + str(PEOPLE) + " people, for " + " at " + str(TIME) + "\n\n" + "1. " + str(restaurants[0][0]) + ", located at " + str(restaurants[0][1]) + "\n\n" + "2. " + str(restaurants[1][0]) + ", located at " + str(restaurants[1][1]) + "\n\n" + "3. " + str(restaurants[2][0]) + ", located at " + str(restaurants[2][1]) + "\n\n" + "Enjoy your meal!"
        CHARSET = "UTF-8"
        # Create a new SES resource and specify a region.
        client = boto3.client('ses',region_name=AWS_REGION)
        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                      
                        'Text': {
                            'Charset': CHARSET,
                            'Data': finalMessage,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
               
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
            
  
  
    # messageSent = sns.publish(
    #     PhoneNumber= modifiedNumber,
    #     Message= finalMessage,
    # )

    # receipt_handle = message['ReceiptHandle']
    # sqs.delete_message(
    #     QueueUrl = queue_url,
    #     ReceiptHandle = receipt_handle
    # )
    
    response =sendEmail(message)
    return {
        'statusCode': 200,
        'body': finalMessage
    }
