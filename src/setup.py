from setuptools import find_packages, setup

setup(
    name='Bank266P',
    version='1.0.0',
    packages=find_packages(),
    incluude_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
