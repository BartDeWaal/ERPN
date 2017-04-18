from setuptools import setup

setup(name='erpn',
      version='1.0',
      description='An RPN Calculator',
      url='http://github.com/BartDeWaal/ERPN',
      author='Bart de Waal',
      author_email='bart@tuduft.nl',
      license='GPLv3',
      packages=['erpn'],
      install_requires=['pyperclip', 'urwid'],
      entry_points={
          'console_scripts': [
              'erpn = erpn.main:main'
              ]
          },
      keywords="rpn",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Utilities',
          'Operating System :: POSIX',
          ],
      )
