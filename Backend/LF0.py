import json
import boto3

def lambda_handler(event, context):
    input_text = event.get("messages")[0].get("unstructured").get("text")
    
    client = boto3.client('lex-runtime')
    response = client.post_text (
        botName     = "DiningConcierge",
        botAlias    = "DiningChatbot",
        userId      = "id",
        inputText   = input_text
        )
        
    return {
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'messages': [ 
            {
                'type': "unstructured", 
                'unstructured': 
                {
                    'text': response.get("message")
                }
            } 
        ]
    }
