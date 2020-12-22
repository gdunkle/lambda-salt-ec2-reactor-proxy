# coding: utf-8

from setuptools import setup, find_packages

    
setup(
    name='lambda-salt-ec2-reactor-proxy',
    version='1.0',
    description='This function listens for auto scale events on a configured SNS topic and then forwards the message to a salt master server',
    author='Galen Dunkleberger',
    license='ASL',
    zip_safe=False,
    include_package_data=True,
    package_dir={"": "source"},
    packages=find_packages("source"),
    test_suite='tests'
)
