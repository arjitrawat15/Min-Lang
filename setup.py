from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="minlang-compiler",
    version="0.1.0",
    author="MinLang Team",
    author_email="team@minlang.dev",
    description="Educational compiler for MinLang programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-team/minlang-compiler",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.4.0",
        "colorama>=0.4.6",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "minlang=main:main",
        ],
    },
)
