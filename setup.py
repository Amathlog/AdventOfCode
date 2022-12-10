from distutils.core import setup

setup(name='AdventOfCode',
      version='1.0',
      description='My take on Advent of Code',
      author='Adrien Logut',
      author_email='adrien.logut@gmail.com',
      packages=["aoc"],
      requires=["numpy", "reprint"]
     )