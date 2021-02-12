import configuration

class config_test(object):
    def __init__(self):

        aws_config_file = "./configuration/aws.json"
        self.aws_config = configuration.aws_configuration(aws_config_file)

        print(self.aws_config.get_endpoint())

test = config_test()