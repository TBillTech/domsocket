#!/usr/bin/env python

from distutils.core import setup

setup(name='domsocket',
      version='1.0',
      description='Fastest Web App Development in the West!',
      author='TBillTech',
      author_email='tbill@TBillTech.com',
      url='https://github.com/TBillTech/domsocket',
      packages=['domsocket', 'domsocket/basic_widgets', 'domsocket/messages'],
      scripts=['scripts/build_cherrypyserver', 'scripts/test_domsocket', 'scripts/todos_app_example'],
      package_data={'domsocket': ['data/*','data/cherrypyserver/*','data/examples/*','data/examples/todos/*','data/examples/todos/widgets/*','data/js/*', 'data/test/*', 'data/test/tester/*', 'data/test/tester/test/*', 'data/test/tester/widgets/*']},
      )
