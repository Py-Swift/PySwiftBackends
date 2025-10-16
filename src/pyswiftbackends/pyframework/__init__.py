from backend_tools import FilePath
from ..standard_backend import StandardBackend
import os

class PyFrameworkBackend(StandardBackend):
    
    version = "3.13"
    sub_version = "b11"
    
    def frameworks(self) -> list[FilePath]:
        #py_fw = FilePath.ps_support() + "Python.framework" # type: ignore
        
        return [
        ]
        
    
    def target_dependencies(self, target_type: str) -> list[dict[str, object]]:
        return [
        ]
    
    
    def install(self, support: FilePath):
        ver = self.version
        sub = self.sub_version
        support = FilePath.ps_support()
        py_fw  = support + "Python.xcframework" # type: ignore
        filename = f"Python-{ver}-iOS-support.{sub}.tar.gz"
        py_fw_tar = str(support + filename) # type: ignore
        
        if not py_fw.exists:
            url = f"https://github.com/beeware/Python-Apple-support/releases/download/{ver}-{sub}/Python-{ver}-iOS-support.{sub}.tar.gz"
            self.download_file(url, py_fw_tar)
            self.untar_file(py_fw_tar, str(support))
            os.remove(py_fw_tar)
        
backend = PyFrameworkBackend()