import requests
from requests.exceptions import RequestException
from django.template import Template, Context


class Action:
    name = 'HTTP Request'

    def execute(self, case, args):
        template = Template(args.get('body', ''))
        context = Context({
            'case': case,
            'args': args
        })

        data = template.render(context)

        try:
            response = requests.post(args['url'], data=data)
            response.raise_for_status()
            case.logs.create(
                event='http_request',
                metadata={
                    'message': f"Sucessfully performed HTTP request to {args['url']}. Response {response.status_code} data: {response.text}"
                }
            )

            return True
        except RequestException as e:
            case.logs.create(
                event='http_request',
                metadata={
                    'message': f'Could not complete request due to exception {e}'
                }
            )

            return False
