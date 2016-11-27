import os
from exp10it import ModulePath
os.system("rm %sconfig.ini" % ModulePath)
os.system("rm -r %slog" % ModulePath)
os.system("pip3 uninstall exp10it")
modulePath = os.path.abspath(__file__)[:-len(__file__.split("/")[-1])]
os.chdir("/root/")
os.system("rm -r %s" % modulePath) 
