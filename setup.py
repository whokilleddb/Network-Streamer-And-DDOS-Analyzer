#!/usr/bin/env python3  
from setuptools import setup, find_packages  
import pathlib  

here = pathlib.Path(__file__).parent.resolve()  

# Get the long description from the README file  
long_description = (here / "README.md").read_text(encoding="utf-8")  

# Get a list of requirements  
requirements = [i.strip() for i in open("requirements.txt").readlines()]  

setup(
      name="network_video_streamer",  
      version="0.0.1",  
      description="Stream videos over a network",  
      long_description=long_description,  
      long_description_content_type="text/markdown",  
      url="https://github.com/whokilleddb",  
      classifiers=[  
            "Programming Language :: Python :: 3",
      ],
      packages=find_packages(exclude="tests"),
      python_requires=">=3.7",
      install_requires=requirements,
)
