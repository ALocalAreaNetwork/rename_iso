from setuptools import setup, find_packages

setup(
    name="rename_iso",
    version="0.1.1",
    description="A tool to rename ISO files and their directories based on SFV files.",
    author="ALocalAreaNetwork",
    author_email="ALocalAreaNet@proton.me",
    url="https://github.com/ALocalAreaNetwork/rename_iso",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rename_iso=rename_iso.rename_iso:main',
        ],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)