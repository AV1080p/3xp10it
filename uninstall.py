import os
from exp10it import ModulePath
os.system("pip3 uninstall exp10it")
os.system("rm %sconfig.ini" % ModulePath)
os.system("rm -r %slog" % ModulePath)
modulePath = __file__[:-len(__file__.split("/")[-1])]
os.system("rm -r %s" % modulePath) 
