#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.   #
#                                                                            #
#  Licensed under the Amazon Software License (the "License"). You may not   #
#  use this file except in compliance with the License. A copy of the        #
#  License is located at                                                     #
#                                                                            #
#      http://aws.amazon.com/asl/                                            #
#                                                                            #
#  or in the "license" file accompanying this file. This file is distributed #
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,        #
#  express or implied. See the License for the specific language governing   #
#  permissions and limitations under the License.                            #
##############################################################################

import logging
import json
import os
import traceback
import requests
import sys

SALT_MASTER_ENDPOINT = str(os.environ.get('SALT_MASTER_ENDPOINT'))


def lambda_handler(event, context):
    try:
        results = [process_record(r) for r in event["Records"]]
        if len(list(filter(lambda r: r['status_code'] != 200, results))) > 0:
            status_code = 500
        else:
            status_code = 200
        result = {
            'status_code': status_code,
            'body': {'results': results}
        }
        return json.dumps(result)
    except Exception as error:
        logging.error('lambda_handler error: %s' % error)
        logging.error('lambda_handler trace: %s' % traceback.format_exc())
        result = {
            'status_code': 500,
            'body': {'message': 'error'}
        }
        return json.dumps(result)


def process_record(record):
    message = json.loads(record["Sns"]["Message"])
    logging.debug(message)
    r = requests.post(SALT_MASTER_ENDPOINT, data=message)
    return {
        "status_code": r.status_code,
        "text": r.text
    }


def init_logger():
    global log_level
    log_level = str(os.environ.get('LOG_LEVEL')).upper()
    if log_level not in [
        'DEBUG', 'INFO',
        'WARNING', 'ERROR',
        'CRITICAL'
    ]:
        log_level = 'ERROR'
    logging.getLogger().setLevel(log_level)


init_logger()
