import json
import boto3
import random
import re

def sqsEntry(city_name, cuisine, people, time, email):
    
    regionName  = "us-east-1"
    access_key  = ""
    api_key     = ""
    queue_url   = ""

    sqs = boto3.client (
                            service_name            = "sqs",
                            aws_access_key_id       = access_key,
                            aws_secret_access_key   = api_key,
                            region_name             = regionName,
                        )
    print("Message being sent to the SQS Queue...")
    response = sqs.send_message(
        QueueUrl = queue_url,
        DelaySeconds = 10,
        MessageAttributes = {
            'Location': {
                'DataType': 'String',
                'StringValue': city_name
            },
            'Cuisine': {
                'DataType': 'String',
                'StringValue': cuisine
            },
            'People': {
                'DataType': 'Number',
                'StringValue': "{}".format(people)
            },
            'Time': {
                'DataType': 'String',
                'StringValue': time
            },
            'Email': {
                'DataType': 'String',
                'StringValue': "{}".format(email)
            }
        },
        MessageBody=(
            'User values in the attributes field'
        )
    )
    print(response)
    front_response = "We will send you our best recommendation shortly through a text, till then grab a cup of joe!"
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": front_response
            }
        }
    }

def lambda_handler(event, context):
    
    cuisine_list = ['japanese', 'chinese', 'italian']
    cities = ['manhattan', 'brooklyn', 'queens', 'staten island', 'bronx']
    
    intent_name = event.get("currentIntent").get("name")

    if intent_name == "GreetingIntent":
        res = "Hey, what can I help you with?"
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": res
                }
            }
        }

    if intent_name == "ThankYouIntent":

        res = "Hope I was able to assist you!"
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": res
                }
            }
        }

    if intent_name == "DiningSuggestionsIntent":

        cityName        = event.get("currentIntent").get("slots").get("Location")
        time            = event.get("currentIntent").get("slots").get("Time")
        cuisine         = event.get("currentIntent").get("slots").get("Cuisine")
        # phone_number    = event.get("currentIntent").get("slots").get("Number")
        people          = event.get("currentIntent").get("slots").get("People")
        email           = event.get("currentIntent").get("slots").get("Email")

        if cityName is None:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                      "contentType": "PlainText",
                      "content": "Which city do you want the reservation to be in?"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "Location"
                }
            }
        
        elif cityName is not None and cityName.lower() not in cities:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                    "contentType": "PlainText",
                    "content": "Please enter from the following options: Manhattan, Brooklyn, Bronx, Queens and Staten Island?"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "Location"
                }
            }

        elif people is None:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                      "contentType": "PlainText",
                      "content": "How many people should I book it for?"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "People"
                }
            }

        elif people is not None and int(people) > 25:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                      "contentType": "PlainText",
                      "content": "Please enter any amount less than 25"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "People"
                }
            }

        elif time is None:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                      "contentType": "PlainText",
                      "content": "What time would you like your reservation to be at?"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "Time"
                }
            }

        elif cuisine is None:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                      "contentType": "PlainText",
                      "content": "What Cuisine are you in the mood for (Japanese, Chinese or Italian)?"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "Cuisine"
                }
            }
        
        
        elif cuisine is not None and cuisine.lower() not in cuisine_list:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                    "contentType": "PlainText",
                    "content": "Please enter from the following options: Japanese, Chinese, Italian?"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "Cuisine"
                }
            }

        # elif phone_number is None:
        #     return {
        #         "dialogAction": {
        #             "type": "ElicitSlot",
        #             "message": {
        #               "contentType": "PlainText",
        #               "content": "What is your mobile number?"
        #             },
        #         "intentName": "DiningSuggestionsIntent",
        #         "slots": {
        #             "Location": cityName,
        #             "Cuisine": cuisine,
        #             "People": people,
        #             "Time":time,
        #             "Number":phone_number,
        #             "Email":email
        #         },
        #         "slotToElicit" : "Number"
        #         }
        #     }
            
        # elif phone_number is not None:
        #     PHONE_REGEX = re.compile(r'[0-9]{10}')
        #     if not PHONE_REGEX.match(phone_number):
        #         return {
        #             "dialogAction" : {
        #                 "type" : "ElicitSlot",
        #                 "message": {
        #                     "contentType" : "PlainText",
        #                     "content": "You have entered an incorrect phone number. Please enter a 10 digit US phone number: "
        #                 },
        #             "intentName" : "DiningSuggestionsIntent",
        #             "slots" : {
        #                 "Location": cityName,
        #                 "Cuisine": cuisine,
        #                 "People": people,
        #                 "Time":time,
        #                 "Number":phone_number,
        #                 "Email":email
        #             },
        #             "slotToElicit" : "Number"
        #             } 
        #         }
        
        elif email is None:
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                      "contentType": "PlainText",
                      "content": "What is your Email ID?"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "Email"
                }
            }
        
        elif email is not None and not (email.endswith('nyu.edu') or email.endswith('gmail.com')) :
            return {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                    "contentType": "PlainText",
                    "content": "Please use the NYU or gmail address!"
                    },
                "intentName": "DiningSuggestionsIntent",
                "slots": {
                    "Location": cityName,
                    "Cuisine": cuisine,
                    "People": people,
                    "Time":time,
                    # "Number":phone_number,
                    "Email":email
                },
                "slotToElicit" : "Email"
                }
            }
                
        else:
            return sqsEntry(cityName, cuisine, people, time, email)
            
