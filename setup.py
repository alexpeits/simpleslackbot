from setuptools import setup, find_packages

setup(
    name='simpleslackbot',
    version=0.1,
    author='Alex Peitsinis',
    packages=find_packages(),
    install_requires=['slackclient==1.0.5'],
    zip_safe=False
)
