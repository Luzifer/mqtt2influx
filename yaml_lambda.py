import json
import yaml


class YAMLLambda(yaml.YAMLObject):
    yaml_tag = '!lambda'

    def __init__(self, lambda_code):
        self.code = lambda_code

    def run(self, in_value):
        return eval('lambda {}'.format(self.code))(in_value)

    @classmethod
    def from_yaml(cls, loader, node):
        return YAMLLambda(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, data.code)


yaml.SafeLoader.add_constructor('!lambda', YAMLLambda.from_yaml)
yaml.SafeDumper.add_multi_representer(YAMLLambda, YAMLLambda.to_yaml)
