from backend_tools import FilePath
from ..sdl2 import SDL2Backend
import pip
from importlib.util import spec_from_file_location



pre_main_swift = """
KivyLauncher.pyswiftImports = [
    {modules}
]
"""

main_swift = """
exit(
    KivyLauncher.SDLmain()
)
"""



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
    
    def copy_to_site_packages(self, site_path: FilePath):
        pips = [
            "ios", "pyobjus"
        ]
        for pip in pips:
            self.pip_install(pip, "--extra-index-url", "https://pypi.anaconda.org/pyswift/simple", "--target", str(site_path))
        
    
    def pre_main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        return pre_main_swift.format(modules=",\n\t".join(modules))
    
    def main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        return main_swift
    
    
    
backend = KivyLauncherBackend()