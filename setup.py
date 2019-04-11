import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyntube",
    version="0.0.1",
    author="Epic",
    author_email="surtla100@gmail.com",
    description="Python streaming service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tag-epic/pyntube",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "flask",
        "requests",
        "opencv_python",
        "numpy",
        "mss",
        "pillow",
        "pyaudio"
    ]
)