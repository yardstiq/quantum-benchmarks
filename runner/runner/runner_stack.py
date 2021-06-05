from aws_cdk import (
    core,
    aws_ec2 as ec2,
)

instanceName="yardstiqEC2"
instanceType="t2.micro"
amiName="ubuntu-images-us-west-1/ubuntu-hardy-8.04-i386-server-20091130.manifest.xml"


class RunnerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # lookup existing VPC
        vpc = ec2.Vpc(
            self,
            "yardstiqVpc",
        )
       
        # create a new security group
        sec_group = ec2.SecurityGroup(
            self,
            "sec-group-allow-ssh",
            vpc=vpc,
            allow_all_outbound=True,
        )

        # add a new ingress rule to allow port 22 to internal hosts
        sec_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(), #('10.0.0.0/16'),
            description="Allow SSH connection", 
            connection=ec2.Port.tcp(22)
        )

        # Define commands to run on startup
        user_data = ec2.UserData.for_linux()

#        command = """
#        git clone https://github.com/Roger-luo/quantum-benchmarks > /home/ubuntu/yardstiq.log \
#                && cd quantum-benchmarks >> /home/ubuntu/yardstiq.log \
#                && bin/benchmark setup >> /home/ubuntu/yardstiq.log  \
#                && bin/benchmark benchmark >> /home/ubuntu/yardstiq.log 
#        """

        command = """
        echo "Hello World" >> /home/ubuntu/yardstiq.log
        echo "sudo halt" | at now + 1 minutes
        """

        user_data.add_commands(command)

        # define a new ec2 instance
        ec2_instance = ec2.Instance(
            self,
            "ec2-instance",
            key_name="yardstiqPem",
            instance_name=instanceName,
            instance_type=ec2.InstanceType(instanceType),
            machine_image=ec2.GenericLinuxImage({'us-west-1': 'ami-031b673f443c2172c'}),
            vpc=vpc,
            security_group=sec_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=user_data,
            user_data_causes_replacement=True
        )





