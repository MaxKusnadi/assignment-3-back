from setuptools import setup, find_packages

setup(
    name='a3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_login',
        'flask_oauth',
        'sqlalchemy',
        'MySQL-python',
    ]
)
