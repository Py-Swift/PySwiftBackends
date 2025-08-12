from backend_tools import FilePath
from ..standard_backend import StandardBackend
from urllib.request import urlretrieve
import tarfile

class PyFrameworkBackend(StandardBackend):
    
    version = "3.11"
    sub_version = "b7"
    
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
        py_fw_tar = support + filename # type: ignore
        
        if not py_fw.exists:
            url = f"https://github.com/beeware/Python-Apple-support/releases/download/{ver}-{sub}/Python-{ver}-iOS-support.{sub}.tar.gz"
            self.download_file(url, str(support))
            self.untar_file(py_fw_tar, str(support))
        
        
backend = PyFrameworkBackend()