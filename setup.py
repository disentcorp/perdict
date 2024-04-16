from setuptools import setup

setup(
    name="perdict",
    version="0.0.1",
    description="""Super simple Persistent dictionary.""",
    author="Batu Davaademberel",
    author_email="batu@disent.com",
    license="Apache Software License",
    url="https://github.com/disentcorp/perdict",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Operating System :: Unix",
    ],
    packages=[
        "perdict",
    ],
    
    include_package_data=True,
    package_data={"perdict": ["tests/*"]},
    license_files=("LICENSE",),
    python_requires=">=3.7",
    zip_safe=False,
)
