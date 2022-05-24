import asyncio
import os
import base64
import json
import boto3
from set_logging import logger
from botocore.exceptions import ClientError

def get_secret(secret_name, region_name):
    """Create a Secrets Manager client"""
    secret, get_secret_value_response = None, None

    # Create a Secrets Manager client
    session = boto3.session.Session()
    try:
        client = session.client(
            service_name="secretsmanager", region_name=region_name
            )
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
            )
    except ClientError as ex:
        raise ex
    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary,
    # one of these fields will be populated.
    if get_secret_value_response:
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        elif "SecretBinary" in get_secret_value_response:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])
    if isinstance(secret, str):
        secret = json.loads(secret)
    return secret


#
# if __name__ == '__main__':
#     print(get_secret('pk'))
