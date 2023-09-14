import os
from typing import Optional
import logging

from slack_bolt import App, Say, BoltContext, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

logging.basicConfig(level=logging.DEBUG)


#
# Database operations
#

# Please note that this is just a demonstration.
# For your business use cases, please proceed with a production-grade database.
database: dict = {"Hey": "What's up?"}


def save_custom_response(keyword: str, response: str):
    database[keyword] = response


def delete_custom_response(keyword: str):
    del database[keyword]


def find_custom_response(text: str) -> Optional[str]:
    for keyword in database.keys():
        if keyword in text:
            return database.get(keyword)
    return None


#
# Slack app
#

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# The message event subtypes to respond
posted_message_subtypes = [
    None,
    "bot_message",
    "thread_broadcast",
    "file_share",
]


# Respond to a message only when its text matches
@app.event("message")
def handle_message_events(message: dict, say: Say):
    if message.get("subtype") not in posted_message_subtypes:
        # Refer to https://api.slack.com/events/message?filter=Events to learn the full list of subtypes
        return
    custom_response = find_custom_response(message.get("text"))
    if custom_response is None:
        return
    say(text=custom_response, thread_ts=message.get("thread_ts"))


# Configure this app on the Home tab
@app.event("app_home_opened")
def sync_home_tab(context: BoltContext, client: WebClient):
    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Configuration*"},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Click this button to add/edit a response :point_right:",
            },
            "accessory": {
                "action_id": "save",
                "type": "button",
                "text": {"type": "plain_text", "text": "Add/Edit"},
                "style": "primary",
                "value": "save",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Custom Responses*"},
        },
        {"type": "divider"},
    ]
    for keyword, response in database.items():
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Keyword:* {keyword}\n*Response:* {response}",
                },
                "accessory": {
                    "action_id": "delete",
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Delete"},
                    "style": "danger",
                    "value": keyword,
                },
            }
        )
    client.views_publish(
        user_id=context.user_id,
        view={"type": "home", "blocks": blocks},
    )


# Open a modal to receive user inputs
@app.action("save")
def handle_some_action(ack: Ack, body: dict, client: WebClient):
    ack()
    client.views_open(
        trigger_id=body.get("trigger_id"),
        view={
            "type": "modal",
            "callback_id": "saving",
            "title": {"type": "plain_text", "text": "My Custom Response"},
            "submit": {"type": "plain_text", "text": "Save"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "keyword",
                    "label": {"type": "plain_text", "text": "When someone says"},
                    "element": {"type": "plain_text_input", "action_id": "input"},
                },
                {
                    "type": "input",
                    "block_id": "response",
                    "label": {
                        "type": "plain_text",
                        "text": "This app's bot user responds",
                    },
                    "element": {"type": "plain_text_input", "action_id": "input"},
                },
            ],
        },
    )


# Add/edit a custom response in the database
@app.view("saving")
def save_registration(
    view: dict,
    ack: Ack,
    context: BoltContext,
    client: WebClient,
):
    keyword = view["state"]["values"]["keyword"]["input"]["value"]
    response = view["state"]["values"]["response"]["input"]["value"]
    # You can do input validation here if necessary
    if len(keyword) >= 100:
        ack(
            response_action="errors",
            errors={"keyword": "Keyword must be shorter than 100 characters"},
        )
        return
    ack()
    save_custom_response(keyword, response)
    sync_home_tab(context=context, client=client)


# Delete an existing custom response
@app.action("delete")
def handle_some_action(
    ack: Ack,
    payload: dict,
    context: BoltContext,
    client: WebClient,
):
    ack()
    delete_custom_response(payload.get("value"))
    sync_home_tab(context=context, client=client)


# export SLACK_APP_TOKEN=xapp-...
# export SLACK_BOT_TOKEN=xoxb-...
# pip install -r requirements.txt
# python app.py
if __name__ == "__main__":
    # Establish a Socket Mode connection
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
