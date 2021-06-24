from django.test import TestCase
from dfirtrack_main.models import Taskpriority

class TaskpriorityModelTestCase(TestCase):
    """ taskpriority model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Taskpriority.objects.create(taskpriority_name='prio_1')

    def test_taskpriority_string(self):
        """ test string representation """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # compare
        self.assertEqual(str(taskpriority_1), 'prio_1')

    def test_taskpriority_id_attribute_label(self):
        """ test attribute label """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # get label
        field_label = taskpriority_1._meta.get_field('taskpriority_id').verbose_name
        # compare
        self.assertEqual(field_label, 'taskpriority id')

    def test_taskpriority_name_attribute_label(self):
        """ test attribute label """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # get label
        field_label = taskpriority_1._meta.get_field('taskpriority_name').verbose_name
        # compare
        self.assertEqual(field_label, 'taskpriority name')

    def test_taskpriority_name_length(self):
        """ test for max length """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # get max length
        max_length = taskpriority_1._meta.get_field('taskpriority_name').max_length
        # compare
        self.assertEqual(max_length, 50)
