#!/usr/bin/env python
from distutils.core import *

setup(name='Pomodoro+',
      version='1.0',
      author='Eslam Mostafa',
      author_email='cseslam@gmail.com',
      license='GPL',
      description='Pomodoro+ is a timer that applies that pomodoro technique, designed for gnu/linux, written in python/gtk.',
      packages=['pomodoro'],
      scripts=['pomodoro+',],
      data_files=[('/usr/share/icons/hicolor/scalable/apps', ['data/pomodoro+.png']),
			('/usr/share/applications',['data/pomodoro+.desktop']),
			('/usr/share/pomodoro+',['data/gtk-style.css']),
		],
      )
