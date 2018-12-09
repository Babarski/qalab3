import unittest
from lab2.ApplicationService.ApplicationServiceImpl import ApplicationServiceImpl
from lab2.PhoneRepository.PhoneRepositoryImpl import PhoneRepositoryImpl
from pymongo import MongoClient
import os
import yaml
import coverage


class TestApplicationServiceImpl(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cov = coverage.Coverage()
        self.cov.start()

    @classmethod
    def tearDownClass(self):
        self.cov.stop()
        self.cov.save()
        self.cov.html_report()

    def setUp(self):
        print("Enviroment - "+os.environ.get("MODE"))

    def tearDown(self):
        configfile = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        with open(configfile+"/configs/configs.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile)
            mode = "mongodb_" + os.environ.get("MODE")
            client = MongoClient(cfg[mode]["host"])
            client.drop_database(cfg[mode]["database"])

    def test_get_all_phones(self):

        phone_repository = PhoneRepositoryImpl()
        phone_repository.create_phone(phone_name='iphone', phone_price=2000)
        phone_repository.create_phone(phone_name='iphone', phone_price=100)
        phone_repository.create_phone(phone_name='iphone', phone_price=100)
        phone_repository.create_phone(phone_name='samsung', phone_price=2000)
        phone_repository.create_phone(phone_name='samsung', phone_price=2000)

        application_service = ApplicationServiceImpl()
        phones = application_service.get_phones_with_same_names()

        test = [{'price': 2000, 'name': 'iphone'},
                {'price': 100, 'name': 'samsung'},
                {'price': 1300, 'name': 'samsung'},
                {'price': 100, 'name': 'iphone'},
                {'price': 100, 'name': 'iphone'}]

        self.assertEqual(len(phones), len(test))


    def test_get_phones_with_same_name(self):
        phone_repository = PhoneRepositoryImpl()
        phone_repository.create_phone(phone_name='iphone', phone_price=2000)
        phone_repository.create_phone(phone_name='iphone', phone_price=100)
        phone_repository.create_phone(phone_name='iphone', phone_price=100)
        phone_repository.create_phone(phone_name='samsung', phone_price=2000)
        phone_repository.create_phone(phone_name='samsung', phone_price=2000)
        phone_repository.create_phone(phone_name='meizu', phone_price=2000)
        phone_repository.create_phone(phone_name='nokia', phone_price=2000)


        application_service = ApplicationServiceImpl()
        test = [{'price': '2000', 'name': 'iphone'},
                {'price': '100', 'name': 'samsung'},
                {'price': '1300', 'name': 'samsung'},
                {'price': '100', 'name': 'iphone'},
                {'price': '100', 'name': 'iphone'}]

        phones = application_service.get_phones_with_same_names()


        self.assertEqual(len(phones), len(test))


    def test_empty_array(self):

        application_service = ApplicationServiceImpl()
        self.assertEqual(application_service.get_phones_with_same_names(), [])


    def test_change_symbol(self):
        phone_repository = PhoneRepositoryImpl()
        phone_repository.create_phone(phone_name='iphone', phone_price=2000)
        phone_repository.create_phone(phone_name='samsung', phone_price=100)

        phone = phone_repository.get_phone_by_name('iphone')
        phone_id = phone.get('_id')

        application_service = ApplicationServiceImpl()
        application_service.change_symbol(phone['_id'], symbol='p', symbol_to_change='o')

        self.assertEqual(phone_repository.get_phone(phone['_id'])['name'], 'iphpne')

    def test_empty_symbol(self):
        phone_repository = PhoneRepositoryImpl()
        phone_repository.create_phone(phone_name='iphone', phone_price=2000)
        phone_repository.create_phone(phone_name='samsung', phone_price=100)

        phone = phone_repository.get_phone_by_name('iphone')
        phone_id = phone.get('_id')

        application_service = ApplicationServiceImpl()
        application_service.change_symbol(phone['_id'], symbol='p', symbol_to_change='')

        self.assertEqual(phone_repository.get_phone(phone['_id'])['name'], 'iphone')


    def test_change_unused_symbol(self):
        phone_repository = PhoneRepositoryImpl()
        phone_repository.create_phone(phone_name='iphone', phone_price=2000)
        phone_repository.create_phone(phone_name='samsung', phone_price=100)

        phone = phone_repository.get_phone_by_name('iphone')

        application_service = ApplicationServiceImpl()
        application_service.change_symbol(phone['_id'], symbol='p', symbol_to_change='k')

        self.assertEqual(phone_repository.get_phone(phone['_id'])['name'], 'iphone')

