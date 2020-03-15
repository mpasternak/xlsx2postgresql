from setuptools import setup

setup(
    name="xlsx2postgresql",
    version="0.1",
    package_dir={"": "src"},
    packages=["xlsx2postgresql"],
    install_requires=["Click", "xlrd"],
    entry_points="""
        [console_scripts]
        xlsx2postgresql=xlsx2postgresql.core:xlsx2postgresql
    """,
)
