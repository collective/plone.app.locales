from setuptools import find_packages
from setuptools import setup


version = "6.0.17"


def read(filename):
    with open(filename) as myfile:
        try:
            return myfile.read()
        except UnicodeDecodeError:
            # Happens on one Jenkins node on Python 3.6,
            # so maybe it happens for users too.
            pass
    # Opening and reading as text failed, so retry opening as bytes.
    with open(filename, "rb") as myfile:
        contents = myfile.read()
        return contents.decode("utf-8")


readme = read("README.rst")
changes = read("CHANGES.rst")
long_description = "\n".join([readme, changes])

setup(
    name="plone.app.locales",
    version=version,
    description="Translation files for Plone",
    long_description=long_description,
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="plone i18n locale translation",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/collective/plone.app.locales",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
    ],
)
