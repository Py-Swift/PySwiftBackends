from backend_tools import CodeBlock, FilePath
from ..standard_backend import CodePriority
from ..sdl3 import SDL3Backend
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


class Kivy3LauncherBackend(SDL3Backend):
    
    def exclude_dependencies(self) -> list[str]:
        return [
            "kivy"
        ]
    
    def packages(self) -> dict:
        print("adding KivyLauncher packages")
        return {
            "Kivy3Launcher": {
                "url": "https://github.com/KivySwiftPackages/Kivy3Launcher",
                "branch": "master"
            }
        }
    
    def target_dependencies(self, target_type: str):
        deps = super().target_dependencies(target_type)
        deps.append(
            {"package": "Kivy3Launcher", "products": ["KivyLauncher"]}
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
            "kivy==3.0.0.dev0", "ios", "pyobjus"
        ]
        for pip in pips:
            self.pip_install(
                pip,
                "--upgrade",
                "--disable-pip-version-check",
                f"--platform={platform}",
                "--only-binary=:all:",
                "--extra-index-url", "https://pypi.anaconda.org/pyswift/simple", 
                "--extra-index-url", "https://pypi.anaconda.org/beeware/simple",
                "--extra-index-url", "https://pypi.anaconda.org/kivyschool/simple",
                "--python-version=313",
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
    
    
    
backend = Kivy3LauncherBackend()