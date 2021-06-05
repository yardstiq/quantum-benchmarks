#!/usr/bin/env python3

from aws_cdk import core

from runner.runner_stack import RunnerStack
import os

app = core.App()


region = os.environ.get("AWS_REGION", "us-west-1")
account_id = os.environ.get("AWS_ACCOUNT_ID","249016812213")
env = core.Environment(region=region, account=account_id)

RunnerStack(app, "runner", env=env)

app.synth()
