from backend_tools import FilePath
from ..standard_backend import StandardBackend, pip3
import os
from os.path import join
import pip
import tempfile
import shutil


class KivyReloaderBackend(StandardBackend):

    def copy_to_site_packages(self, site_path: FilePath):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = str(tmp)
            self.download_file(
                "https://github.com/kivy-school/kivy-reloader/archive/refs/heads/main.zip",
                join(tmp_path, "main.zip")
            )
            
            self.unzip_file(join(tmp_path, "main.zip"), tmp_path)
            
            reloader_path = join(tmp_path, "kivy-reloader-main")
            pyp_path = join(reloader_path, "pyproject.toml")
            pyproject = self.load_pyproject_toml(pyp_path)
            
            deps: list[str] = pyproject["project"]["dependencies"] # type: ignore
            
            deps_copy = deps[:]
            to_remove = [
                "cython", "buildozer", "kaki", "pip", "psutil", "toml"
            ]
            
            for dep in deps_copy:
                for rm in to_remove:
                    if dep.startswith(rm):
                        deps.remove(dep)
                        continue
            
            self.save_pyproject_toml(pyproject, pyp_path)
            
            self.pip_install(reloader_path, "-t", str(site_path))
            
            
        
backend = KivyReloaderBackend()