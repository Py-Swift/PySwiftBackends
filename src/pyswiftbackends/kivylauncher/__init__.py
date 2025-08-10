from backend_tools import FilePath
from ..sdl2 import SDL2Backend
import pip
from importlib.util import spec_from_file_location

class KivyLauncherBackend(SDL2Backend):
    
    
    def packages(self) -> dict:
        return {
            "KivyLauncher": {
                "path": "/Volumes/CodeSSD/beeware_env/swift_packages/KivyLauncher",
            }
        }
    
    def target_dependencies(self, target_type: str):
        deps = super().target_dependencies(target_type)
        deps.append(
            {"package": "KivyLauncher", "products": ["KivyLauncher"]}
        )
        
        return deps
    
backend = KivyLauncherBackend()