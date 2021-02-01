from setuptools import find_packages
from setuptools import setup

setup(
    name="ledger-api",
    version="0.0.1",
    description="",
    author="",
    license="Proprietary",
    url="ledger-api.com",
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
        "django==2.2.1",
        "django-money==0.14.4",
        "djangorestframework==3.9.4",
        "django-filter==2.1.0",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["ledger = ledger_api.main:main"]},
)
