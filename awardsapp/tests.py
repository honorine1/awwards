from django.test import TestCase
from .models import Projects,Profile

# Create your tests here.
class ProfileTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.james= Profile(profile_pic = 'default.png', bio ='likes nature', contact ='+250784478113')

    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.james,Profile))

        # Testing Save Method
    def test_save_method(self):
        self.james.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)