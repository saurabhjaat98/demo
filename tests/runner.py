###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Manik Sidana <manik@coredge.io>, Mar 2023                        #
###############################################################################
import os
import sys
import unittest

TestLoader = unittest.defaultTestLoader.discover(os.path.dirname(__file__))
testRunner = unittest.runner.TextTestRunner(verbosity=2)
run = testRunner.run(TestLoader)
sys.exit(not run.wasSuccessful())
