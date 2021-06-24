from django.test import TestCase
from dfirtrack_main.models import Taskname

class TasknameModelTestCase(TestCase):
    """ taskname model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Taskname.objects.create(taskname_name='taskname_1')

    def test_taskname_string(self):
        """ test string representation """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # compare
        self.assertEqual(str(taskname_1), 'taskname_1')

    def test_taskname_id_attribute_label(self):
        """ test attribute label """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # get label
        field_label = taskname_1._meta.get_field('taskname_id').verbose_name
        # compare
        self.assertEqual(field_label, 'taskname id')

    def test_taskname_name_attribute_label(self):
        """ test attribute label """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # get label
        field_label = taskname_1._meta.get_field('taskname_name').verbose_name
        # compare
        self.assertEqual(field_label, 'taskname name')

    def test_taskname_name_length(self):
        """ test for max length """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # get max length
        max_length = taskname_1._meta.get_field('taskname_name').max_length
        # compare
        self.assertEqual(max_length, 50)
