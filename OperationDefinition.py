import requests
import os
import json


class OperationDefinition:

    def __init__(self, operation_definition_json):
        # Gather basic metadata
        self.url = operation_definition_json['url']
        self.code = operation_definition_json['code']
        self.resources = operation_definition_json['resource']

        # Retrieve parameters and split by use
        self.parameters = {'in': [], 'out': []}
        for parameter in operation_definition_json['parameter']:
            if parameter['use'] == 'in':
                self.parameters['in'].append(Parameter(parameter))
            else:
                self.parameters['out'].append(Parameter(parameter))


class Parameter:

    def __init__(self, parameter_json):
        self.name = parameter_json['name']
        self.use = parameter_json['use']
        self.min = parameter_json['min']
        self.max = parameter_json['max']
        # No type information is present if the parameter definition contains part element
        if 'type' in parameter_json:
            self.type = parameter_json['type']


def get_operation_definition_for_url(url):
    od_json = requests.get(url).json()
    return OperationDefinition(od_json)


if __name__ == "__main__":
    with open(os.path.join('resources', 'operation_definition_sources.json')) as url_file:
        # Load operation definition urls
        url_json = json.loads(url_file.read())

        # Test with CodeSystem-lookup
        resource = 'CodeSystem'
        operation = '$lookup'
        od_url = url_json[resource][operation]

        operation_definition = get_operation_definition_for_url(od_url)
        print(f"Detected parameters for operation {operation} of resource {resource}:")
        print(f"in: {', '.join(od_parameter.name for od_parameter in operation_definition.parameters['in'])}")
        print(f"out: {', '.join(od_parameter.name for od_parameter in operation_definition.parameters['out'])}")
