from setuptools import find_packages
from setuptools import setup

setup(
    name="ledger",
    version="0.0.1",
    description="A double entry general accounting ledger.",
    author="Roeland van Nieuwkerk",
    author_email="roeland.frans@gmail.com",
    license="Proprietary",
    url="ledgerapi.io",
    packages=find_packages(),
    dependency_links=[],
    install_requires=["django==2.2.1", "django-money", "py-moneyed"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
