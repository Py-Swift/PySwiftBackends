from backend_tools import FilePath
from ..standard_backend import StandardBackend
import pip
from importlib.util import spec_from_file_location

class PyCoreBluetoothBackend(StandardBackend):
    
    
    def packages(self) -> dict:
        print("adding PyCoreBluetooth package")
        return {
            "PyCoreBluetooth": {
                "url": "https://github.com/KivySwiftPackages/PyCoreBluetooth",
                "branch": "master"
            }
        }
    
    def target_dependencies(self, target_type: str):
        return [
            {"package": "PyCoreBluetooth", "products": ["PyCoreBluetooth"]}
        ]
    
    def wrapper_imports(self, target_type: str) -> list[dict[str, object]]:
        return [
            {
                "libraries": ["PyCoreBluetooth"],
                "modules": [".py_corebluetooth"]
            }
        ]
        
    def pre_main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        return "launchAdmob()"
        
    
backend = PyCoreBluetoothBackend()