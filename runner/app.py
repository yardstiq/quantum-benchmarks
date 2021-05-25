#!/usr/bin/env python3

from aws_cdk import core

from runner.runner_stack import RunnerStack


app = core.App()


env = core.Environment(region="us-west-1", account="249016812213")

RunnerStack(app, "runner", env=env)

app.synth()
