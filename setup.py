import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Biosim-G03-Anders-Petter", # Replace with your own username
    version="0.0.1",
    author="Anders Høst; Petter Hetland",
    author_email="pehe@nmbu.no",
    description="Exam package for INF200 biosim project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pkhetland/BioSim_G03_Anders_Petter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)