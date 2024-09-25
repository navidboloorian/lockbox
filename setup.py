from setuptools import setup

setup(
    name="lockbox",
    version="1.0",
    py_modules=["main"],
    entry_points={
        'console_scripts': [
            'lockbox = main:main',
        ],
    },
)
