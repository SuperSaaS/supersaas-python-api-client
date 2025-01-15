"""Setup for SuperSaas API client module."""

from setuptools import setup, find_packages

setup(
    name='supersaas-api-client',
    version='2.0.1',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    description='Online bookings/appointments/calendars using the SuperSaaS scheduling platform  - '
                'https://supersaas.com',
    long_description='The SuperSaaS API provides services that can be used to add online booking'
                     ' and scheduling functionality to an existing website or CRM software.',
    author='Kaarle Kulvik',
    author_email='dev@supersaas.com',
    keywords=['online appointment schedule', 'booking calendar', 'appointment book',
              'reservation system', 'scheduling software', 'online booking system',
              'scheduling system', 'supersaas'],
    url='https://www.supersaas.com',
    install_requires=[
    ],
    python_requires='>=3.8',
    project_urls={
        'Homepage': 'https://www.supersaas.com',
        'Issues': 'https://github.com/SuperSaaS/supersaas-python-api-client/issues',
        'Documentation': 'https://www.supersaas.com/info/dev',
        'Source': 'https://github.com/SuperSaaS/supersaas-python-api-client'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Office/Business :: Scheduling'
    ],
)
