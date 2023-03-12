from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='mlmbench',
      version='1.0.3',
      description='MLM MachineLearning Molecular Benchmarch',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/gmrandazzo/mlmbench',
      author='Giuseppe Marco Randazzo',
      author_email='gmrandazzo@gmail.com',
      license='GPLv3',
      include_package_data=True,
      packages=['mlmbench'],
      package_data={'': ['data/*/*.*']},
      python_requires=">=3.0",
      zip_safe=False)
