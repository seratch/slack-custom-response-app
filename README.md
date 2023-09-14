# Slack Custom Response App

This app demonstrates how to build something similar to Slack's custom response feature.

Once your app is installed in a Slack workspace, end-users can access the app's Home tab.
They can maintain custom responses there:

<img src="https://user-images.githubusercontent.com/19658/267919329-a9c1c4a5-0e64-477f-a056-b985adf182b2.gif" width=500 />

Invite the app's bot user to the channels where you'd like to enable this app.
Now it's ready!
Whenever an end-user posts a message that contains a registered keyword in the channel, the app replies to it using the registered response text.

<img src="https://user-images.githubusercontent.com/19658/267919397-d177ba9f-9975-46ce-b100-8f22ed6eef5a.gif" width=500 />

## How to run the app

### Create a Slack app

Head to https://api.slack.com/apps and create a new app using app-manifest.yml in this repo.

### Generate SLACK_APP_TOKEN

Go to Settings > Basic Information > App-Level Tokens, and click the "Generate Token and Scopes" button.
You can generate a new token with the `connections:write` scope and save it as the `SLACK_APP_TOKEN` env variable when running your app.

### Install the app into a Slack workspace

Go to Settings > Install App and click "Install to Workspace" button.
Once the installation completes, save the "Bot User OAuth Token" string as the `SLACK_BOT_TOKEN` env variable.

## Run the app on your local machine

Please note that you need Python 3.6 or newer to run this app.
You can follow the steps below to start the app:

```bash
export SLACK_APP_TOKEN=xapp-...
export SLACK_BOT_TOKEN=xoxb-...
pip install -r requirements.txt
python app.py
```

Lastly, please don't forget to invite this app's bot user to the channels where you want to enable this app's responses.

## License

The MIT License
