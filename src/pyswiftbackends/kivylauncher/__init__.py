from backend_tools import FilePath
from ..sdl2 import SDL2Backend
import pip
from importlib.util import spec_from_file_location

class KivyLauncherBackend(SDL2Backend):
    
    def packages(self) -> dict:
        print("adding KivyLauncher packages")
        return {
            "KivyLauncher": {
                "url": "https://github.com/KivySwiftPackages/KivyLauncher",
                "branch": "master"
            }
        }
    
    def target_dependencies(self, target_type: str):
        deps = super().target_dependencies(target_type)
        deps.append(
            {"package": "KivyLauncher", "products": ["KivyLauncher"]}
        )
        
        return deps
    
    def wrapper_imports(self, target_type: str) -> list[dict[str, object]]:
        return [
            {
                "libraries": ["KivyLauncher"],
                "modules": []
            }
        ]
    
    def pre_main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        _modules = ",\n\t".join(modules)
        return f"""KivyLauncher.pyswiftImports = [
            {_modules}
        ]
        """
    
    def main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        return """exit(
            KivyLauncher.SDLmain()
        )
        """
    
    
    
backend = KivyLauncherBackend()