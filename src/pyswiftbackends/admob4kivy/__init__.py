from backend_tools import FilePath
from ..standard_backend import StandardBackend 
import pip
from importlib.util import spec_from_file_location

class Admob4KivyBackend(StandardBackend):
    
    def packages(self) -> dict:
        print("adding a4k_pyswift package")
        return {
            "a4k_pyswift": {
                "url": "https://github.com/KivySwiftPackages/a4k_pyswift",
                "branch": "master"
            }
        }
    
    def target_dependencies(self, target_type: str):
        return [
            {"package": "a4k_pyswift", "products": ["a4k_pyswift"]}
        ]
        
    def wrapper_imports(self, target_type: str) -> list[dict[str, object]]:
        return [
            {
                "libraries": ["a4k_pyswift"],
                "modules": [".a4k_pyswift"]
            }
        ]
        
    def pre_main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        pass
    
    def main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        pass
    
backend = Admob4KivyBackend()