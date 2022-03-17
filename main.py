#!/usr/bin/env python
from constructs import Construct
from cdktf import App, NamedRemoteWorkspace, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws import AwsProvider, ec2
import configparser
import os


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        config = configparser.ConfigParser()
        config.read('config.ini')
       # self.account = config['environment']['account']
        self.account = os.getenv('TYRELL_ENVIRONMENT')
        self.variables = config['variables_{}'.format(self.account)]
        print(self.variables["instance_size"])
        
        AwsProvider(self, "AWS", region="eu-west-2")

        instance = ec2.Instance(self, "compute",
                                ami=self.variables["ami"],
                                instance_type=self.variables["instance_size"],
                                tags={"Name": "CDKTF-Demo"},
                                )

        TerraformOutput(self, "public_ip",
                        value=instance.public_ip,
                        )


app = App()
stack = MyStack(app, "aws_instance")

app.synth()
