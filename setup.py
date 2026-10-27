"""Setup for SuperSaaS API client module."""

from pathlib import Path

from setuptools import find_packages, setup

setup(
    name='supersaas-api-client',
    version='2.0.1',
    license='MIT',
    packages=find_packages(exclude=['test', 'test.*', 'examples', 'examples.*']),
    include_package_data=True,
    description='Online bookings/appointments/calendars using the SuperSaaS scheduling platform - '
                'https://supersaas.com',
    long_description=(Path(__file__).parent / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    author='Kaarle Kulvik',
    author_email='dev@supersaas.com',
    keywords=['online appointment schedule', 'booking calendar', 'appointment book',
              'reservation system', 'scheduling software', 'online booking system',
              'scheduling system', 'supersaas'],
    url='https://www.supersaas.com',
    install_requires=[],
    python_requires='>=3.8',
    project_urls={
        'Homepage': 'https://www.supersaas.com',
        'Issues': 'https://github.com/SuperSaaS/supersaas-python-api-client/issues',
        'Documentation': 'https://www.supersaas.com/info/dev',
        'Source': 'https://github.com/SuperSaaS/supersaas-python-api-client'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
