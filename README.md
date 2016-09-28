------------------------------------------------------------------------------
Known bugs:
------------------------------------------------------------------------------
* Problem: cx-Oracle gcc: error: unrecognized command line option ‘-mno-cygwin’
* Solution: this is obsolete gcc option. To fix:
env/bin/pip3 download cx-Oracle
tar zxvf cx_Oracle-5.2.1.tar.gz
remove aforementioned gcc option
env/bin/pip3 install -e cx_Oracle-5.2.1

* Problem: numpy/core/src/multiarray/numpyos.c:18:21: fatal error: xlocale.h: No such file or directory
when pip3 install numpy
* Solution: ln -s /usr/include/locale.h /usr/include/xlocale.h

* Problem: file corrupted on Cygwin
* Solution: fork() issue on Cygwin: Force a full rebase: Run rebase-trigger fullrebase, exit all Cygwin programs and run Cygwin setup.

* Problem: problem with tkagg
* Solution: http://stackoverflow.com/questions/5151755/how-to-install-matplotlib-on-cygwin
env/bin/pip3 download matplotlib
Edit setup.cfg. Around line 70 in the file is a commented line, uncomment the line such that you have:
tkagg = False