from django_migration_testcase import MigrationTest


class ForwardCreateCurrentTest(MigrationTest):
    app_name = 'current'
    before = '0001_initial'
    after = '0002_create_current'

    def test_migration(self):
        self.run_migration()

        # there should be exactly one Current
        Current = self.get_model_after('Current')
        self.assertEqual(Current.objects.all().count(), 1)


class BackwardCreateCurrentTest(MigrationTest):
    app_name = 'current'
    before = '0002_create_current'
    after = '0001_initial'

    def test_migration(self):
        # there should be exactly one Current
        Current = self.get_model_before('Current')
        self.assertEqual(Current.objects.all().count(), 1)

        self.run_migration()

        # there should be exactly no Current
        Current = self.get_model_after('Current')
        self.assertEqual(Current.objects.all().count(), 0)
