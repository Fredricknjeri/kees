from xml.etree import ElementTree
from urllib.parse import urlparse, urljoin
from datetime import datetime
import hashlib

from constance import config
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlencode
import requests

class Action:
    name = 'Mozard koppelverzoek'

    def execute(self, case, args):
        xxd = timezone.now().strftime('%Y%m%d%H%M%S')
        plain_text = f"{args['hash']}\n{args['xxb']}\n{args['hash']}\n{args['xxc']}\n{args['hash']}\n{xxd}\n{args['hash']}\n"

        parsed_url = urlparse(args['url'])
        xxe = hashlib.sha1(plain_text.encode('utf-8')).hexdigest()
        number_of_previous_requests = case.logs.filter(event='mozard_request').count()

        data = render_to_string('mozard/create_case_request.xml', {
            'xxb': args['xxb'],
            'xxc': args['xxc'],
            'xxd': xxd,
            'xxe': xxe,
            'hash': hash,
            'first_notification': (number_of_previous_requests == 0),
            'case': case,
            'assignments': self.get_assignments(case),
            'documents': self.get_documents(case),
            'user': args['user'],
            'organization': {
                'name': config.COMPANY_NAME,
                'address': config.COMPANY_ADDRESS,
                'house_number': config.COMPANY_HOUSE_NUMBER,
                'zip': config.COMPANY_ZIP,
                'city': config.COMPANY_CITY,
            }
        })

        try:
            response = requests.post(args['url'], files={
                'mXml': ('case.xml', data, 'application/xml')
            })
            response.raise_for_status()

            tree = ElementTree.fromstring(response.content)

            case.logs.create(
                event='mozard_request',
                metadata={
                    'success': True,
                    'host': parsed_url.netloc,
                    'mozard_case_id': tree.find('moz_koppelverzoek_zaak').text
                }
            )

            return True
        except (requests.RequestException, ElementTree.ParseError) as e:
            case.logs.create(
                event='mozard_request',
                metadata={
                    'success': False,
                    'host': parsed_url.netloc,
                    'exception': f'{e}'
                }
            )

            return False

    def get_assignments(self, case):
        for key, mapping in self.assignment_mapping.items():
            if isinstance(case.data.get(key), list):
                value = case.data.get(key)[0]
            else:
                value = case.data.get(key)

            if mapping['type'] == 'string':
                yield {'id': mapping['dest_id'], 'value': value}
            elif mapping['type'] == 'date':
                print(value)
                try:
                    parsed_date = datetime.fromisoformat(value)
                except TypeError:
                    parsed_date = ''

                yield {'id': mapping['dest_id'], 'value': parsed_date.strftime('%Y%m%d') if parsed_date else ''}
            elif mapping['type'] == 'boolean':
                yield {'id': mapping['dest_id'], 'value': 'J' if value else 'N'}
            else:
                raise Exception(f"Unsupported type: {mapping['type']}")

    def get_documents(self, case):
        for attachment in case.attachments.all():
            yield {
                'display_name': attachment.display_name,
                'url': urljoin(config.URL, attachment.file.url, f'?s={urlencode(attachment.get_signature())}'),
                'extension': attachment.extension.upper()
            }

    assignment_mapping = {
        'soort_werk': {'dest_id': 1205, 'type': 'string'},
        'vooronderzoek': {'dest_id': 1207, 'type': 'string'},
        'adres': {'dest_id': 443, 'type': 'string'},
        'plaats': {'dest_id': 601, 'type': 'string'},
        'startdatum': {'dest_id': 555, 'type': 'date'},
        'einddatum': {'dest_id': 959, 'type': 'date'},
        'naam_aannemer': {'dest_id': 1097, 'type': 'string'},
        'contactpersoon_aannemer': {'dest_id': 1098, 'type': 'string'},
        'adres_aannemer': {'dest_id': 1099, 'type': 'string'},
        'postcode_aannemer': {'dest_id': 1100, 'type': 'string'},
        'plaats_aannemer': {'dest_id': 1101, 'type': 'string'},
        'telefoonnummer_aannemer': {'dest_id': 1102, 'type': 'string'},
        'kwalibo_erkend_aannemer': {'dest_id': 350, 'type': 'boolean'},
        'aantal_m3_te_ontgraven': {'dest_id': 1208, 'type': 'string'},
    }
