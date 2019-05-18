from base.constants import SYSTEM_USERNAME
from base.constants.entity import ENTITY_INDIVIDUAL
from base.constants.entity import ENTITY_PTY
from base.models import Entity
from base.utils import generate_country_province_mapper
from base.utils import get_or_create_profile
from base.utils import get_system_user
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from mock import MagicMock
from mock import patch


class EntityTestCase(TestCase):
    @patch("base.models.datetime")
    @patch("base.models.random")
    @patch("django.db.models.Model")
    @patch("base.models.luhn_sign")
    @patch("base.models.gen_feistel")
    @patch("base.models.connection")
    def test_save(
        self, connection, gen_feistel, luhn_sign, Model, random, datetime
    ):
        # Configure mocks
        cursor_mock = MagicMock(name="cursor")

        connection.cursor.return_value = cursor_mock

        random.randint.return_value = 1000

        date_mock = MagicMock(name="date")
        date_mock.strftime.return_value = "20140101"
        datetime.now.return_value = date_mock

        gen_feistel.return_value = 1000
        luhn_sign.return_value = 1000

        n = int("20140101" + "1000")

        entity = Entity()

        # Test with db vendor == 'sqlite'
        cursor_mock.db.vendor = "sqlite"

        entity.save()

        random.randint.assert_called_with(0, 100000)
        assert datetime.now.called
        date_mock.strftime.assert_called_with("%Y%m%d")
        gen_feistel.assert_called_with(n)
        luhn_sign.assert_called_with(1000)
        self.assertEqual(entity.entity_no, "000001000")

        # Test with db vendor == 'postgres'
        cursor_mock.db.vendor = "postgres"
        cursor_mock.fetchone.return_value = [1000]

        entity.entity_no = None
        entity.save()

        assert connection.cursor.called
        cursor_mock.execute.assert_called_with(
            "SELECT nextval('base_entity_id_seq')"
        )
        assert cursor_mock.fetchone.called
        assert datetime.now.called
        date_mock.strftime.assert_called_with("%Y%m%d")
        gen_feistel.assert_called_with(n)
        luhn_sign.assert_called_with(1000)
        self.assertEqual(entity.entity_no, "000001000")

    def test_permitted_filter(self):
        queryset_mock = MagicMock(name="queryset")

        Entity.permitted_filter(queryset=queryset_mock, user="user")

        queryset_mock.filter.assert_called_with(users="user")


class BaseUserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frank = get_user_model().objects.create_user(
            username="frank", password="test"
        )

        cls.company = Entity.objects.create(
            entity_type=ENTITY_PTY,
            name="company",
            telephone="0124563445",
            fax="01234533234",
            email="info@company.com",
        )
        cls.company.users.add(cls.frank)
        cls.company.save()

        cls.individual = Entity.objects.create(
            entity_type=ENTITY_INDIVIDUAL,
            name="Frank",
            telephone="01245633456",
            fax="01234537789",
            email="frank@company.com",
        )
        cls.individual.users.add(cls.frank)
        cls.individual.save()

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        Entity.objects.all().delete()

    def test_get_entities(self):
        entities = self.frank.get_entities()

        self.assertTrue(self.company in entities)
        self.assertTrue(self.individual in entities)

    def test_get_individual_entity(self):
        entity = self.frank.get_individual_entity()

        self.assertEqual(entity, self.individual)


class BaseUtilsTestCase(TestCase):
    @patch("base.utils.settings")
    @patch("base.utils.models")
    def test_get_or_create_profile(self, models, settings):
        # Test with no exception
        user_mock = MagicMock(name="user")
        user_mock.get_profile.return_value = "profile"

        profile = get_or_create_profile(user_mock)

        assert user_mock.get_profile.called
        self.assertEqual(profile, "profile")

        # Test with ObjectDoesNotExist exception
        get_profile_mock = MagicMock(
            name="get_profile", side_effect=ObjectDoesNotExist
        )
        user_mock.get_profile = get_profile_mock

        settings.AUTH_PROFILE_MODULE = "base.UserProfile"
        model_mock = MagicMock(name="model")
        models.get_model.return_value = model_mock
        model_mock.objects.get_or_create.return_value = ["profile"]

        profile = get_or_create_profile(user_mock)

        assert user_mock.get_profile.called
        models.get_model.assert_called_with("base", "UserProfile")
        model_mock.objects.get_or_create.assert_called_with(user=user_mock)
        self.assertEqual(profile, "profile")

    def test_get_system_user(self):
        # Test with no system user
        system_user = get_system_user()

        self.assertEqual(system_user, False)

        # Test with a system user
        system_user = get_user_model().objects.create_user(
            username=SYSTEM_USERNAME, password="test"
        )

        user = get_system_user()

        self.assertEqual(user, system_user)

    @patch("json.dumps")
    @patch("base.utils.subdivisions")
    def test_generate_country_province_mapper(self, subdivisions, dumps):
        subdiv1 = MagicMock()
        subdiv1.country.alpha2 = "div1"
        subdiv1.code = "code1"
        subdiv1.name = "name1"

        subdiv2 = MagicMock()
        subdiv2.country.alpha2 = "div1"
        subdiv2.code = "code2"
        subdiv2.name = "name2"

        subdivisions.__iter__.return_value = [subdiv1, subdiv2]

        generate_country_province_mapper()

        assert dumps.called
