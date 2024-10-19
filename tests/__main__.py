import unittest
from coverage import Coverage

test_loader = unittest.TestLoader()
cov = Coverage(source=('fluentflow',))

with cov.collect():

    # Make sure test discovery is in scope of collection
    # Otherwise, coverage.py can't capture all the data
    tests = test_loader.discover('.')

    unittest.TextTestRunner().run(tests)

cov.report()
cov.html_report(directory='htmlcov')


__all__ = [
    'main',
]

