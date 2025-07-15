from setuptools import setup, find_packages

setup(
    name="validador_cnpj",
    version="1.0.0",
    author="Lilian Kotvan",
    author_email="liliankotvan@gmail.com",
    description="Validação de CNPJ alfanumérico com cálculo de dígito verificador (compatível com Databricks)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pyspark>=3.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    include_package_data=True
)
