from setuptools import setup, find_packages

setup(
    name='supersaas-api-client',
    version='0.10.3',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    description='Online bookings/appointments/calendars using the SuperSaaS scheduling platform  - https://supersaas.com',
    long_description='The SuperSaaS API provides services that can be used to add online booking and scheduling functionality to an existing website or CRM software.',
    author='Travis Dunn',
    author_email='travis@supersaas.com',
    keywords=['online appointment schedule', 'booking calendar', 'appointment book', 'reservation system', 
              'scheduling software', 'online booking system', 'scheduling system'],
    url='https://www.supersaas.com',
    install_requires=[
    ],
    project_urls={
        'Documentation': 'https://www.supersaas.com/info/dev',
        'Source': 'https://github.com/SuperSaaS/supersaas-python-api-client'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Scheduling'
    ],
)
