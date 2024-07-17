# This file represent a example of testing using unittest

import unittest
import numpy as np
import pandas as pd
from importlib import resources
# import our package here  from our_package import NFW, etc

class TestINSTANCE(unittest.TestCase):  # You can change the name of the Class
    def test_init_default(self):  # This test is only to check if the function works
        # swift = NFW(**kwargs)  # Add args to the main function (i.e., mass, radius, etc.)
        # self.assertEqual(NFW.mass, 64)  # Check if the mass is received on the instance NFW
        # self.assertEqual(NFW.radius, 1e2)  # Check if the radius required is received for the instance NFW
        pass

if __name__ == '__main__':  # Main executable line of code, it will run all the test when used
    unittest.main()
