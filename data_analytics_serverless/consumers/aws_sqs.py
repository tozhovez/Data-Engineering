import boto3

def receive_queue_attributes(queue_url): 

    # queue_url = 'SQS_QUEUE_URL'
    # Create SQS client
    sqs = boto3.client('sqs')
    # Receive message from SQS queue
    response = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])
    return response


def delete_message_from_queue(queue_url, receipt_handle): 

    # queue_url = 'SQS_QUEUE_URL'
    # Create SQS client
    sqs = boto3.client('sqs')
    
    # Delete message from queue
    response = sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return response