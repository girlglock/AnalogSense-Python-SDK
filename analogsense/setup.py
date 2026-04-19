from setuptools import setup, find_packages

setup(
    name="analogsense",
    version="1.0.0",
    description="Python port of the AnalogSense JavaScript SDK",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=["hid"],
)
