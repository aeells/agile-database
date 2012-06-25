from setuptools import setup, find_packages

setup(name='agile-database',
      version='0.0.1',
      packages=find_packages(),
      scripts=['bin/agile_database.py'],
      requires=["mock", "PyYAML", "MySQLdb"],
      test_suite='tests',
      tests_require='mock',
      )