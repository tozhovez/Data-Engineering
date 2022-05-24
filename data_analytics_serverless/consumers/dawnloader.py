

import json
import datetime
import boto3
import os
from botocore.exceptions import ClientError


import pathlib
import yaml




SERVICE_CONF = pathlib.Path(__file__).parent / os.getenv(
    "CONFIGS_FILE", "configs-dev-etl.yml"
)


def load_config_from_yaml(filename):
    """load configuration from yaml file"""
    with open(filename, "r", encoding="utf-8") as fd_reader:
        return yaml.full_load(fd_reader)
    



def main_handler(event, context):
    config = load_config_from_yaml(SERVICE_CONF)
    
    current_time = datetime.datetime.now().time()
    message = f"Process start {str(current_time)}"
    record = json.loads(event['Records'][0]["body"])
    receipt_handle = event['Records'][0]["messageAttributes"]["receipt_handle"]
    src = record["url_src"]
    dest = record["url_dest"]
    
    try:
        data = "\n".join(map(lambda row: json.dumps(raw),  load_data(url_src)))
        response = save_data_to_s3(dest, data)
        queue_url = queue_url(config["sqs_queue_name"])
        delete_message_from_queue(queue_url, receipt_handle)
        queue_attributes = receive_queue_attributes(queue_url)
        if queue_attributes["ApproximateNumberOfMessages"] == "0" \
            and queue_attributes["ApproximateNumberOfMessagesNotVisible"] == "0" \
            and queue_attributes["ApproximateNumberOfMessagesDelayed"] == "0":
            # queue is empty
            start_data_processing_process()   
    except ClientError as ex:
        return ex
    
    else:  
        return
    
