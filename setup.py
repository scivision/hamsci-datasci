#!/usr/bin/env python
install_requires=['numpy','pyhamtools','pyephem']
tests_require=['nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='hamsci-datasci',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      version='0.1.0',
      description='Data Science scripts for HamSci',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3',
      ],
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'plot':['matplotlib','seaborn',],
                       'tests':tests_require},
      python_requires='>=3.6',
	  )

