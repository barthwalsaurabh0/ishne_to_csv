from setuptools import setup, find_packages

setup(
    name="ishne-to-csv",
    version="0.1.0",
    description="Convert ISHNE ECG Holter files to timestamped CSV format",
    author="Saurabh Barthwal",
    packages=find_packages(),
    install_requires=["pandas", "tqdm"],
    entry_points={
        'console_scripts': [
            'ishne-to-csv = ishne_to_csv.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
