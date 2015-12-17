from django_migration_testcase import MigrationTest

class ForwardCreateHomePageTest(MigrationTest):
    app_name = 'home'
    before = '0001_initial'
    after = '0002_create_homepage'

    def test_migration(self):
        self.run_migration()

        # there should be exactly one HomePage
        HomePage = self.get_model_after('HomePage')
        self.assertEqual(HomePage.objects.all().count(), 1)


class BackwardCreateHomePageTest(MigrationTest):
    app_name = 'home'
    before = '0002_create_homepage'
    after = '0001_initial'

    def test_migration(self):
        # there should be exactly one HomePage
        HomePage = self.get_model_before('HomePage')
        self.assertEqual(HomePage.objects.all().count(), 1)

        self.run_migration()

        # there should be exactly no HomePage
        HomePage = self.get_model_after('HomePage')
        self.assertEqual(HomePage.objects.all().count(), 0)
