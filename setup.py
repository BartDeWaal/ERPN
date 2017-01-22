from setuptools import setup

setup(name='erpn',
      version='0.1dev',
      description='An RPN Calculator',
      url='http://github.com/BartDeWaal/ERPN',
      author='Bart de Waal',
      author_email='bart@tuduft.nl',
      license='GPLv3',
      packages=['erpn'],
      install_requires=['pyperclip'],
      entry_points={
          'console_scripts': [
              'erpn = erpn.main:main'
              ]
          },
      )
