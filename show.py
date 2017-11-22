import json
import logging
import random

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# import the shared library, now anything in common/ can be referenced as
# `common.something`
import common


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    fact = random.choice(common.all_facts())

    return {
        'statusCode': 200,
        'body': json.dumps({'random_fact': fact})
    }

