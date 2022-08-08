from setuptools import find_packages
from setuptools import setup

setup(
    name="django-general-ledger",
    version="0.0.1",
    description="",
    author="",
    license="???",
    url="https://github.com/openwallet/django-general-ledger",
    packages=find_packages(),
    dependency_links=[],
    python_requires=">=3.7",
    install_requires=["django==4.0.6", "django-money==3.0.0",],
    include_package_data=True,
    zip_safe=False,
)
