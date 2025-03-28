from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py-mail-me",
    version="0.1.0",
    author="Jui-Hsuan Lee",
    author_email="juihsuanlee0303@gmail.com",
    description="A simple Python package for sending email notifications after task completion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juihsuanlee0303/py-mail-me",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "python-dotenv>=0.19.0",
    ],
) 