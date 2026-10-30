#!/usr/bin/env python3
import os, sys, unittest
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, R)
suite = unittest.TestLoader().discover(os.path.join(R, "tests"), pattern="test_*.py")
sys.exit(0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1)
