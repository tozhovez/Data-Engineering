
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
    



def main_handler_sensor_data(event, context):
    config = load_config_from_yaml(SERVICE_CONF)
    # get numder rows of data to load
    # send create url requests  to api create where to save data and send this message data to queue in loop 
