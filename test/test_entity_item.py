import unittest

from simplejson import JSONDecodeError

from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.datatypes import Item

wbi = WikibaseIntegrator()


class TestEntityItem(unittest.TestCase):

    def test_get(self):
        # Test with complete id
        assert wbi.item.get('Q582').id == 'Q582'
        # Test with numeric id as string
        assert wbi.item.get('582').id == 'Q582'
        # Test with numeric id as int
        assert wbi.item.get(582).id == 'Q582'

        # Test with invalid id
        with self.assertRaises(ValueError):
            wbi.item.get('L5')

        # Test with zero id
        with self.assertRaises(ValueError):
            wbi.item.get(0)

        # Test with negative id
        with self.assertRaises(ValueError):
            wbi.item.get(-1)

    def test_get_json(self):
        assert wbi.item.get('Q582').get_json()['labels']['fr']['value'] == 'Villeurbanne'

    def test_write(self):
        with self.assertRaises(JSONDecodeError):
            wbi.item.get('Q582').write(allow_anonymous=True, mediawiki_api_url='https://httpstat.us/200')

    def test_write_required(self):
        assert not wbi.item.get('Q582').write_required(base_filter={'P1791': ''})

        item = wbi.item.get('Q582')
        item.claims.add(Item(prop_nr='P1791', value='Q42'))
        assert item.write_required(base_filter={'P1791': ''})
