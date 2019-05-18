from setuptools import find_packages
from setuptools import setup

setup(
    name="ledger-base",
    version="0.0.1",
    description="Ledger API base models and utilities.",
    author="Roeland van Nieuwkerk",
    author_email="roeland.frans@gmail.com",
    license="Proprietary",
    url="ledgerapi.io",
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
        "django-jsonfield",
        "django==2.2.1",
        "pycountry",
        "pyotp",
    ],
    tests_require=["django-setuptest"],
    test_suite="setuptest.setuptest.SetupTestSuite",
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
