from setuptools import setup

setup(
    name="windup_ide_tests",
    version="1.0",
    description="Test Framework for Red Hat Application \
        Migration Toolkit IDE plugin",
    license="Eclipse Public License 2.0",
    long_description="README.md",
    long_description_content_type="text/markdown",
    packages=["src", "src/lib", "src/fixtures"],
    install_requires=[
        "rpaframework",
        "rpaframework-recognition",
        "rpaframework[cv]",
        "tesseract",
        "pytest",
    ],
)
