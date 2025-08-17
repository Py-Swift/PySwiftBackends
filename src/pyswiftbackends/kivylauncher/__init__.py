from backend_tools import CodeBlock, FilePath
from ..standard_backend import CodePriority
from ..sdl2 import SDL2Backend
import pip
from importlib.util import spec_from_file_location



pre_main_swift = """
KivyLauncher.pyswiftImports = [
    {modules}
]
"""

main_swift = """
let exit_status = KivyLauncher.SDLmain()
"""

on_exit = """
exit(exit_status)
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
    
    def copy_to_site_packages(self, site_path: FilePath, platform: str):
        
        pips = [
            "ios", "pyobjus"
        ]
        for pip in pips:
            self.pip_install(
                pip,
                "--disable-pip-version-check",
                f"--platform={platform}",
                "--only-binary=:all:",
                "--extra-index-url", "https://pypi.anaconda.org/pyswift/simple", 
                "--target", str(site_path)
            )
    
    def will_modify_main_swift(self) -> bool:
        return True
    
    def modify_main_swift(self, libraries: list[str], modules: list[str]) -> list["CodeBlock"]:
        return [
            CodeBlock(
                pre_main_swift.format(modules=",\n\t".join(modules)),
                CodePriority.POST_IMPORTS
            ),
            CodeBlock(
                main_swift,
                CodePriority.MAIN
            ),
            CodeBlock(
                on_exit,
                CodePriority.ON_EXIT
            )
        ]
    
    
    
backend = KivyLauncherBackend()