from setuptools import setup, find_packages

setup(name='agile-database',
      version='0.0.1',
      packages=find_packages(),
      scripts=['bin/agile_database.py'],
      install_requires=['PyYaml', 'PyMySQL'],
      package_data={
          '':['*.sql']
      },
      test_suite='tests',
      tests_require='mock',
      )