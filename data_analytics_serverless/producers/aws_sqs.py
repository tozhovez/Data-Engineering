import boto3

def send_message_to_queue(queue_url, message_body):
    # queue_url = 'SQS_QUEUE_URL'
    # Create SQS client
    sqs = boto3.client('sqs')
    
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body,
        MessageAttributes=message_attrs,
        AttributeNames=['All']
    )
    
    return response['MessageId']


