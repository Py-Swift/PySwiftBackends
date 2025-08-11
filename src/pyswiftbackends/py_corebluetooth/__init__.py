from backend_tools import FilePath, PSBackend
import pip
from importlib.util import spec_from_file_location

class PyCoreBluetoothBackend(PSBackend):
    
    def __init__(self):
        super().__init__(self)
        
    def url(self) -> str | None:
        return None
    
    def frameworks(self) -> list[FilePath]:
        return []
        
    def downloads(self) -> list[str]:
        return []
    
    def config(self, root: FilePath):
        pass
    
    def packages(self) -> dict:
        print("adding a4k_pyswift package")
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
                "modules": [".pycorebluetooth"]
            }
        ]
    
backend = PyCoreBluetoothBackend()