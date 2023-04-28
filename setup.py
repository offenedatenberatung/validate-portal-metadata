from setuptools import setup, find_packages

setup(
        name="dcat_ap_de_validator",
        version="0.1.2",
        author="Mila Frerichs",
        author_email="mila@offenedatenberatung.de",
        description="",
        url="",
        packages=find_packages(),
        install_requires=[
                "requests==2.30.0",
        ],
        entry_points={
            "console_scripts": [
                        "dcat_ap_de_validator-validate=dcat_ap_de_validator.commands.main:main"
            ]
        },
        classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent",
        ],
        python_requires=">=3.9",
)
