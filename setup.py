from setuptools import setup, find_packages

setup(
    name='supersaas-api-client',
    version='1.0.0',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    description='Online bookings/appointments/calendars using the SuperSaaS scheduling platform. The SuperSaaS API provides services that can be used to add online booking and scheduling functionality to an existing website or CRM software.',
    author='Travis Dunn',
    author_email='travis@supersaas.com',
    keywords=['online appointment schedule', 'booking calendar', 'appointment book', 'reservation system', 
              'scheduling software', 'online booking system', 'scheduling system'],
    url='github.com/SuperSaaS/supersaas-python-api',
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
