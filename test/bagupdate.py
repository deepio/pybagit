import unittest
import os
import shutil
from pybagit.bagit import BagIt


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.bag = BagIt(os.path.join(os.getcwd(), "test", "testbag"))
        self.invalid_bag = BagIt(os.path.join(os.getcwd(), "test", "invalid_bag"))

    def tearDown(self):
        if os.path.exists(os.path.join(os.getcwd(), "test", "invalid_bag")):
            shutil.rmtree(os.path.join(os.getcwd(), "test", "invalid_bag"))

    def test_full_update(self):
        self.bag.update(full=True)
        self.assertEqual(len(self.bag.bag_errors), 0)

    def test_partial_update(self):
        self.bag.update(full=False)
        self.assertEqual(len(self.bag.bag_errors), 0)

    def test_is_valid(self):
        self.bag.update()
        self.assertEqual(self.bag.is_valid(), True)

    def test_not_valid(self):
        os.remove(self.invalid_bag.manifest_file)
        self.invalid_bag.validate()
        self.assertEqual(self.invalid_bag.is_valid(), False)


def suite():
    test_suite = unittest.makeSuite(UpdateTest, "test")
    return test_suite
