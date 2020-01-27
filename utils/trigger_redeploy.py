# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import logging
import os
import requests
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object
    """

    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--loglevel',
                        default='INFO',
                        choices=['INFO', 'DEBUG', 'WARNING'],
                        help='log level')

    return parser.parse_args()


def get_env_vars():
    vars = ["RANCHER_PROJECT",
            "RANCHER_CLUSTER_PROJECT_ID",
            "RANCHER_BEARER_TOKEN",
            "RANCHER_ENDPOINT"]
    prefix_map = {"develop": "DEV_",
                  "staging": "STG_"}

    # script expects CIRCLE_BRANCH to be in the enviornment variables
    # my_vars = {"environment": os.environ["CIRCLE_BRANCH"]}
    # hardcode branch for testing
    my_vars = {"environment": "develop"}

    try:
        for v in vars:
            my_vars[v] = os.environ[prefix_map[my_vars["environment"]] + v]
    except KeyError as e:
        logging.error("Please set the needed environment variables", e)
        sys.exit(1)
    return my_vars


def raise_error(msg):
    logger.error(msg)
    sys.exit(1)


def redeploy():
    env_vars = get_env_vars()
    req_headers = {"Authorization": "Bearer {0}".format(env_vars["RANCHER_BEARER_TOKEN"]),
                   "content-type": "application/json",
                   "accept": "application/json",
                   "Cache-Control": "no-cache",
                   "Pragma": "no-cache"}
    env_map = {
        "develop": {
            "endpoint": "https://elbecerro.unicef.io/v3",
            "project": "etools-dev",
            "workloads": ["web-dev", "worker-dev", "beater-dev", "worker-vision-dev"],
            "jobs": ["backend-migrations"]
        }
    }
    try:
        env = env_map[env_vars["environment"]]
    except KeyError:
        logger.info("Current branch has no mapping for continuous deployment")
        return

    for workload in env["workloads"]:
        logging.info("Redeploying {}".format(workload))
        url = '{0}/project/{1}/workloads/deployment:{2}:{3}'.format(env["endpoint"],
                                                                    env_vars["RANCHER_CLUSTER_PROJECT_ID"],
                                                                    env["project"],
                                                                    workload)
        logger.debug(url)
        logger.debug(req_headers)

        response = requests.get(url, headers=req_headers)
        logger.debug(response.status_code)
        if response.status_code >= 300 or response.status_code < 200:
            raise_error("Something went wrong getting data from rancher")
        payload = response.json()
        try:
            payload["annotations"]["cattle.io/timestamp"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%zZ')
        except KeyError:
            raise_error("unnexpected response format from rancher")

        response = requests.put(url, headers=req_headers, json=payload)
        if 300 <= response.status_code or response.status_code < 200:
            raise_error("Something went wrong sending data to rancher")

    # TODO: handle jobs like migrations or data loading


def main():
    logger.info('Script starting...')
    in_arg = vars(get_input_args())

    # Set log level
    log_level = in_arg.pop('loglevel')
    logger.setLevel(log_level)

    logger.debug('Arguments are parsed... ')
    logger.debug(in_arg)

    redeploy()
    logger.info("Done!")


if __name__ == "__main__":
    main()
