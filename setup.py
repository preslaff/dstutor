from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ds-tutor",
    version="0.1.0",
    author="DS-Tutor Team",
    author_email="support@dstutor.dev",
    description="AI-powered Data Science learning in Jupyter notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ds-tutor",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: IPython",
        "Framework :: Jupyter",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "advanced": [
            "xgboost>=1.7.0",
            "lightgbm>=4.0.0",
            "tensorflow>=2.13.0",
            "torch>=2.0.0",
            "shap>=0.42.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dstutor=dstutor.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "dstutor": [
            "data/sample_data/*",
            "../lessons/**/*.yaml",
        ],
    },
    zip_safe=False,
)
