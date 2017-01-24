from setuptools import setup

setup(name='erpn',
      version='0.1',
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
      keywords="rpn",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console :: Curses',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Utilities',
          'Operating System :: POSIX',
          ],
      )
