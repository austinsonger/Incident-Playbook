from django.test import TestCase
from dfirtrack_main.models import Taskstatus

class TaskstatusModelTestCase(TestCase):
    """ taskstatus model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Taskstatus.objects.create(taskstatus_name='taskstatus_1')

    def test_taskstatus_string(self):
        """ test string representation """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # compare
        self.assertEqual(str(taskstatus_1), 'taskstatus_1')

    def test_taskstatus_id_attribute_label(self):
        """ test attribute label """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # get label
        field_label = taskstatus_1._meta.get_field('taskstatus_id').verbose_name
        # compare
        self.assertEqual(field_label, 'taskstatus id')

    def test_taskstatus_name_attribute_label(self):
        """ test attribute label """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # get label
        field_label = taskstatus_1._meta.get_field('taskstatus_name').verbose_name
        # compare
        self.assertEqual(field_label, 'taskstatus name')

    def test_taskstatus_name_length(self):
        """ test for max length """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # get max length
        max_length = taskstatus_1._meta.get_field('taskstatus_name').max_length
        # compare
        self.assertEqual(max_length, 50)
