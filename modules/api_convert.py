import json
import re
import auth
import sys, getopt, argparse

def camel_to_caps(camel_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()


def regex_object_to_string(matchobj):
    pair = matchobj.group(0)
    replacekey = matchobj.group(0).split(': ')[1]
    return pair.replace(replacekey, camel_to_caps(replacekey))


def api_to_import(json_data):
    new_data = json.load(json_data)

    if 'container' in new_data:

        if 'usageContext' in new_data['container']:
            if len(new_data['container']['usageContext']) > 0:
                new_data['container']['usageContext'] = camel_to_caps(new_data['container']['usageContext'][0])
            else:
                raise KeyError('Missing container.usageContext')
        else:
            raise KeyError('Missing container.usageContext')

        new_builtins = []
        if 'enabledBuiltInVariable' in new_data['container']:
            for builtin in new_data['container']['enabledBuiltInVariable']:
                new_builtins.append(camel_to_caps(builtin))
            new_data['container']['enabledBuiltInVariable'] = new_builtins

        flatfile = json.dumps(new_data)
        parameter_types = r'template|boolean|list|map|integer|'
        operator_types = r'contains|cssSelector|endsWith|equals|greater|greaterOrEquals|less|lessOrEquals|matchRegex|startsWith|urlMatches|'
        trigger_types = r'ajaxSubmission|always|click|customEvent|domReady|formSubmission|historyChange|jsError|linkClick|pageview|timer|windowLoaded|youTube'
        regex = r'"type": "(' + parameter_types + operator_types + trigger_types + r')"'
        new_data = json.loads(re.sub(regex, regex_object_to_string, flatfile))

        flatfile = json.dumps(new_data)
        regex = r'"tagFiringOption": "([^"]+)"'
        new_data = json.loads(re.sub(regex, regex_object_to_string, flatfile))

        final_version = {
            'exportFormatVersion' : 1.3,
            'containerVersion' : new_data
        }

    return final_version

def main(argv):
    scope = ['https://www.googleapis.com/auth/tagmanager.readonly']
    
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_client_secrets', help='path to your client_secrets file')
    args = parser.parse_args()
    client_secrets_path = args.path_to_client_secrets
    
    service = auth.auth('tagmanager', 'v1', scope, client_secrets_path)

if __name__ == '__main__':
    main(sys.argv[1:])