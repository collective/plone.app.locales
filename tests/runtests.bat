@rem NB: Due to some sloppy coding and use of GNU's msgcmp,
@rem     this won't test if all msgid's are present on Windows.

@rem full path to the python interpretor
@set PYTHON="d:\zope2\python\python.exe"

@rem path to ZOPE_HOME/lib/python
@set SOFTWARE_HOME="D:\zope2\Zope\lib\python"

@rem path to your instance. Don't set it if you aren't having  instance
@set INSTANCE_HOME="D:\zope2\Data"

@rem Make sure the gettext tools are on your PATH
@set PATH=%PATH%;D:\zope2\gettext\bin

%PYTHON% runalltests.py