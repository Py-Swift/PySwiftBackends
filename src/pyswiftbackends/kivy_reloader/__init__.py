from backend_tools import FilePath
from ..standard_backend import StandardBackend
import os
import pip
import tempfile
import shutil

class KivyReloaderBackend(StandardBackend):
            
    def copy_to_site_packages(self, site_path: FilePath):
        tmp = tempfile.TemporaryDirectory()
        pip.main([
            "install", "kivy-reloader",
            "-t", str(tmp)
            ])
        
        # delete what is needed from tmp
        for folder in os.listdir(str(tmp)):
            if folder.lower() in ["kaki", "watchdog", "psutil"]:
                shutil.rmtree(os.path.join(str(tmp), folder))
        # copy rest of tmp to site_path
        for folder in os.listdir(str(tmp)):
            shutil.copytree(str(tmp), str(site_path))
        
backend = KivyReloaderBackend()