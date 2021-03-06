#!/usr/bin/env python3
# coding: utf-8

from distutils.core import setup

setup(
    name='justme',
    packages=['justme'],
    version='1.1.2',
    description='Prohibit to run two process/instance at same time.',
    package_dir={'justme': 'justme'},
    package_data={'justme': [
                            'locale/just_me.pot',
                            'locale/*/LC_MESSAGES/just_me.mo'
                            ]},
#   ./justme/locale/ja/LC_MESSAGES/just_me.mo'
  # data_files=[
  #     ('locale', ['justme/locale/just_me.pot']),
  # ],
    author='梅濁酒(umedoblock)',
    author_email='umedoblock@gmail.com',
    url='http://pypi.python.org/pypi/justme/',
    download_url='',
    license='BSD License',
    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
    # see
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    options = {
        'sdist': {                                                                          'formats': ['gztar','zip'],
            'force_manifest': True,                                                     },
    },

    long_description = '''\
| Just me
| -------
| 
| Prohibit to run two process/instance at same time.
| To use a transaction behavior via sqlite3.
''',
     )
