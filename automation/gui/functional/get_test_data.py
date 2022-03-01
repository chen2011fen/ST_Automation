import os
import yaml


class YamlUtil:
    @staticmethod
    def read_test_times():
        current_path = os.path.dirname(__file__)
        with open(f'{current_path}/test_data.yaml', 'r') as f:
            value = yaml.load(f, Loader=yaml.FullLoader)
            value = value[0]

        return int(value['test_times'])

    @staticmethod
    def write_test_times(data):
        current_path = os.path.dirname(__file__)
        with open(f'{current_path}/test_data.yaml', 'w') as f:
            yaml.dump(data=data, stream=f, allow_unicode=True)
