from backend_tools import FilePath, PSBackend
import pip
from importlib.util import spec_from_file_location

class Admob4KivyBackend(PSBackend):
    
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
            "KivyLauncher": {
                "url": "https://github.com/KivySwiftPackages/a4k_pyswift",
                "branch": "master"
            }
        }
    
    def target_dependencies(self, target_type: str):
        return [
            {"package": "a4k_pyswift", "products": ["a4k_pyswift"]}
        ]
    
backend = Admob4KivyBackend()