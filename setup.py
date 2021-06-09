from setuptools import setup


setup(name='cooler',
    version="0.0.1",
    description='todo',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    "pywemo",
    "six"
    ],
    entry_points = {
        'console_scripts': [
            'cooler=main:main',
        ]
    }
)
