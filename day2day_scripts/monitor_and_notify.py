#!/usr/bin/env python3
"""
Monitor and Notify - A tool for running commands with Slack notifications

This script allows you to run commands and receive notifications about their execution
status via Slack. It can send start and completion/failure notifications, error alerts,
and custom messages.

Features:
- Monitor command execution and report completion status
- Send formatted error alerts from JSON formatted error messages
- Send custom messages to Slack

Usage:
    python monitor_and_notify.py --command [command to run]
    python monitor_and_notify.py --message "Custom message to send"
    python monitor_and_notify.py --error_message [JSON formatted error]

Environment Variables:
    SLACK_TOKEN: Your Slack API token (can also be passed via --webclient_token)

Examples:
    python monitor_and_notify.py --command python my_script.py
    python monitor_and_notify.py --message "Backup completed successfully!"

Author: Open Source Contributor
License: MIT
"""

import argparse
import getpass
import json
import os
import socket
import subprocess
import time

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

DEFAULT_TOKEN = os.environ.get("SLACK_TOKEN", "<YOUR_SLACK_TOKEN>")
SLACK_CHANNEL = "alerts"  # Change to your desired channel
BOT_USERNAME = "mobitor bot"  # Change to your desired bot name
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def send_alert_to_slack(message, webclient_token):
    # The channel ID or name should match the one you set in Slack api
    channel_id = SLACK_CHANNEL
    bot_name = BOT_USERNAME

    try:
        # Use the chat.postMessage method to send a message to the channel
        client = WebClient(token=webclient_token)
        client.chat_postMessage(channel=channel_id, text=message, username=bot_name)
    except Exception as e:
        print(f"Error sending message to Slack : {e}")


def send_error_alert(error_message, webclient_token):
    hostname = socket.gethostname()
    username = getpass.getuser()
    
    try:
        error_dict = json.loads(error_message)
        if error_dict["levelname"] == "ERROR":
            format_message = f"*Error*: {error_dict['message']} in `{error_dict['filename']}` at line {error_dict['lineno']} at `{error_dict['asctime']}` on `{hostname}` by `{username}`"
            send_alert_to_slack(format_message, webclient_token)
    except Exception:
        pass


def run_and_monitor_command(command, webclient_token):
    # Get hostname and username
    hostname = socket.gethostname()
    username = getpass.getuser()
    
    # Send start notification
    start_message = f"*Process Started*: `{' '.join(command)}` at `{time.strftime(DATE_FORMAT)}` on `{hostname}@{username}`"
    send_alert_to_slack(start_message, webclient_token)
    starting_time = time.time()
    
    try:
        # Run the command and capture output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        
        # Send completion notification
        if process.returncode == 0:
            end_message = f"*Process Completed Successfully*: `{' '.join(command)}` at `{time.strftime(DATE_FORMAT)}` on `{hostname}@{username}` in {(time.time() - starting_time)/60:.2f} minutes"
            send_alert_to_slack(end_message, webclient_token)
        else:
            error_message = f"*Process Failed*: `{' '.join(command)}` with exit code {process.returncode} at `{time.strftime(DATE_FORMAT)}` on `{hostname}` by `{username}` in {(time.time() - starting_time)/60:.2f} minutes \n*Error*: ```{stderr}```"
            send_alert_to_slack(error_message, webclient_token)
    except Exception as e:
        error_message = f"*Error Running Process*: `{' '.join(command)}` at `{time.strftime(DATE_FORMAT)}` on `{hostname}@{username}` in {(time.time() - starting_time)/60:.2f} minutes  \n*Exception*: ```{str(e)}```"
        send_alert_to_slack(error_message, webclient_token)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a message to Slack")
    parser.add_argument("--message", type=str, help="Message to send to Slack")
    parser.add_argument("--webclient_token", default=DEFAULT_TOKEN, help="Slack WebClient token")
    parser.add_argument("--error_message", type=str, help="Error message to send to Slack")
    parser.add_argument("--command", type=str, nargs="+", help="Command to run and monitor")
    # Parse known args to handle flags, leaving remaining args for direct command usage
    args, remaining = parser.parse_known_args()

    if args.message:
        send_alert_to_slack(args.message, args.webclient_token)
    elif args.error_message:
        send_error_alert(args.error_message, args.webclient_token)
    elif args.command:
        run_and_monitor_command(args.command, args.webclient_token)
    elif remaining:  # Use remaining args as command if present
        run_and_monitor_command(remaining, args.webclient_token)
    else:
        print("No valid arguments provided. Use --help for more information.")