
import json
import datetime
import boto3
import os
import pathlib
import yaml
from botocore.exceptions import ClientError



SERVICE_CONF = pathlib.Path(__file__).parent / os.getenv(
    "CONFIGS_FILE", "configs-dev-etl.yml"
)


def load_config_from_yaml(filename):
    """load configuration from yaml file"""
    with open(filename, "r", encoding="utf-8") as fd_reader:
        return yaml.full_load(fd_reader)
    

def call_task(function_name, region, invocation_type, params=None):
    """call_task"""
    session = boto3.session.Session()
    lambda_client = session.client(service_name="lambda", region_name=region)
    lambda_client.invoke(
        FunctionName=function_name,
        InvocationType=invocation_type,
        Payload=json.dumps(params),
    )
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": str(
                    f"{str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))} " \
                    "call task function successfully!"
                    ),
              
            }
        ),
    }



def main_handler(event, context):
    current_time = datetime.datetime.now().time()
    message = f"Process start {str(current_time)}"
    config = load_config_from_yaml(SERVICE_CONF)
    
    try: 
        call_task(
            function_name=config["aws_function_producer_vehicles_data"],
            region=config["region"],
            invocation_type="Event"
            )
        call_task(
            function_name=config["aws_function_producer_vehicles_data"],
            region=config["region"],
            invocation_type="Event"
            )

    except ClientError as ex:
        return ex
    
    else: 
    
        return {
            "statusCode": 200,
            "body": json.dumps({"message": message})
        }
    