

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

def main_queries_executor_handler(event, context):
    config = load_config_from_yaml(SERVICE_CONF)
    # download list of queries from git gub
    
    params = {"params": {"query_files_list": get_query_files_list()}}
    
    return call_task(
            function_name=config["aws_function_next_task"],
            region=config["region"],
            invocation_type="Event",
            params=params
            )

    
def next_queries_executor_handler(event, context):
    """queries executor lambda function"""

    if event["params"]["query_files_list"] and len(event["params"]["query_files_list"]) > 0:
        #result = loop.run_until_complete(queries_execution_in_loop(event))
        return queries_execution_in_loop(event["params"])

    #result = loop.run_until_complete(end_of_queries_execution_loop(event))
    return end_of_queries_execution_loop(event)



def queries_execution_in_loop(params):
    config = load_config_from_yaml(SERVICE_CONF)
    url = params["query_files_list"].pop()
    queries = load_content_query_file(url)
    prepare_execute_queryes_in_athena(queries)
    return call_task(
                function_name=config["aws_function_next_task"],
                region=config["region"],
                invocation_type="Event",
                params=params
                )

def end_of_queries_execution_loop(event):
    # send alert that process etl DONE
    pass
