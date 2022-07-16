import os

import flask
import requests
import creds
from pathlib import Path

from slack.web.client import WebClient
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from flask import Flask


app = Flask(__name__)
env_path = Path('.') / '.env'  # current dir or .env file
load_dotenv(dotenv_path=env_path)

slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/slack/events", app)


client = WebClient(token=os.environ['SLACK_TOKEN'])  # token from .env file


def build(org_id, projects, build_targets, func_name, api_token):
    channel_name = flask.request.values.__getitem__('channel_name')
    username = flask.request.values.__getitem__('user_name')
    if flask.request.values.__getitem__('text'):
        commit = flask.request.values.__getitem__('text').strip()
    else:
        commit = ''
    auth_base = f"orgs/{org_id}/projects/{projects}/buildtargets/{build_targets}"
    url_base = f"https://build-api.cloud.unity3d.com/api/v1/{auth_base}/{func_name}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic {token}".format(token=api_token),
    }
    body = {
        "clean": False,
        "delay": 0,
        "commit": "{hash}".format(hash=commit),
        "headless": False,
        "label": "",
        "platform": "android"
    }
    response = requests.post(url_base, headers=headers)
    if response.status_code == 202:
        client.chat_postMessage(channel=channel_name, text=f"{username} launched a build *successfully*. \n"
                                                           f"Commit hash: {commit}.")
        return flask.jsonify(build_started=True)
    else:
        client.chat_postMessage(channel=channel_name,
                                text=f"{username} tried to launch a build *unsuccessfully.*\n"
                                     f"JSON response is {response.text},\n")
        return flask.jsonify(build_started=False)


@app.route("/slack/events/build", methods=['POST'])
def execute_build():
    message_data = flask.request.values
    channel_name = message_data.__getitem__('channel_name')
    if channel_name == '':
        return build(creds.ORGID, creds.PROJECTS, creds.BUILD_TARGETS, creds.FUNC_NAME,
                     creds.API_TOKEN)
    elif channel_name == '':
        return build(creds.ORGID, creds.PROJECTS, creds.BUILD_TARGETS, creds.FUNC_NAME,
                     creds.API_TOKEN)


if __name__ == "__main__":
    app.run()
