from setuptools import setup, find_packages
setup(  name="chinese_names",
        version="0.1",
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        author='Robert Östling',
        author_email='robert@ling.su.se',
        license='GPLv3',
        package_data={"": ["*.csv"]},
        include_package_data=True)
