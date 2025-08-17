from backend_tools import FilePath
from ..standard_backend import StandardBackend, CodePriority, CodeBlock
import pip
from importlib.util import spec_from_file_location


pre_main_swift = """
KivyLauncher.Env.A4K_BACKEND = "pyswift"
try launchAdmob()
"""

class Admob4KivyBackend(StandardBackend):
    
    def plist_entries(self, plist: object, target_type):
        if isinstance(plist, dict):
            plist.update({
                "GADApplicationIdentifier": "ca-app-pub-3940256099942544~1458002511",
                "SKAdNetworkItems": [
                    {"SKAdNetworkIdentifier": "cstr6suwn9.skadnetwork"},
                    {"SKAdNetworkIdentifier": "4fzdc2evr5.skadnetwork"},
                    {"SKAdNetworkIdentifier": "2fnua5tdw4.skadnetwork"},
                    {"SKAdNetworkIdentifier": "ydx93a7ass.skadnetwork"},
                    {"SKAdNetworkIdentifier": "p78axxw29g.skadnetwork"},
                    {"SKAdNetworkIdentifier": "v72qych5uu.skadnetwork"},
                    {"SKAdNetworkIdentifier": "ludvb6z3bs.skadnetwork"},
                    {"SKAdNetworkIdentifier": "cp8zw746q7.skadnetwork"},
                    {"SKAdNetworkIdentifier": "3sh42y64q3.skadnetwork"},
                    {"SKAdNetworkIdentifier": "c6k4g5qg8m.skadnetwork"},
                    {"SKAdNetworkIdentifier": "s39g8k73mm.skadnetwork"},
                    {"SKAdNetworkIdentifier": "3qy4746246.skadnetwork"},
                    {"SKAdNetworkIdentifier": "f38h382jlk.skadnetwork"},
                    {"SKAdNetworkIdentifier": "hs6bdukanm.skadnetwork"},
                    {"SKAdNetworkIdentifier": "mlmmfzh3r3.skadnetwork"},
                    {"SKAdNetworkIdentifier": "v4nxqhlyqp.skadnetwork"},
                    {"SKAdNetworkIdentifier": "wzmmz9fp6w.skadnetwork"},
                    {"SKAdNetworkIdentifier": "su67r6k2v3.skadnetwork"},
                    {"SKAdNetworkIdentifier": "yclnxrl5pm.skadnetwork"},
                    {"SKAdNetworkIdentifier": "t38b2kh725.skadnetwork"},
                    {"SKAdNetworkIdentifier": "7ug5zh24hu.skadnetwork"},
                    {"SKAdNetworkIdentifier": "gta9lk7p23.skadnetwork"},
                    {"SKAdNetworkIdentifier": "vutu7akeur.skadnetwork"},
                    {"SKAdNetworkIdentifier": "y5ghdn5j9k.skadnetwork"},
                    {"SKAdNetworkIdentifier": "v9wttpbfk9.skadnetwork"},
                    {"SKAdNetworkIdentifier": "n38lu8286q.skadnetwork"},
                    {"SKAdNetworkIdentifier": "47vhws6wlr.skadnetwork"},
                    {"SKAdNetworkIdentifier": "kbd757ywx3.skadnetwork"},
                    {"SKAdNetworkIdentifier": "9t245vhmpl.skadnetwork"},
                    {"SKAdNetworkIdentifier": "a2p9lx4jpn.skadnetwork"},
                    {"SKAdNetworkIdentifier": "22mmun2rn5.skadnetwork"},
                    {"SKAdNetworkIdentifier": "44jx6755aq.skadnetwork"},
                    {"SKAdNetworkIdentifier": "k674qkevps.skadnetwork"},
                    {"SKAdNetworkIdentifier": "4468km3ulz.skadnetwork"},
                    {"SKAdNetworkIdentifier": "2u9pt9hc89.skadnetwork"},
                    {"SKAdNetworkIdentifier": "8s468mfl3y.skadnetwork"},
                    {"SKAdNetworkIdentifier": "klf5c3l5u5.skadnetwork"},
                    {"SKAdNetworkIdentifier": "ppxm28t8ap.skadnetwork"},
                    {"SKAdNetworkIdentifier": "kbmxgpxpgc.skadnetwork"},
                    {"SKAdNetworkIdentifier": "uw77j35x4d.skadnetwork"},
                    {"SKAdNetworkIdentifier": "578prtvx9j.skadnetwork"},
                    {"SKAdNetworkIdentifier": "4dzt52r2t5.skadnetwork"},
                    {"SKAdNetworkIdentifier": "tl55sbb4fm.skadnetwork"},
                    {"SKAdNetworkIdentifier": "c3frkrj4fj.skadnetwork"},
                    {"SKAdNetworkIdentifier": "e5fvkxwrpn.skadnetwork"},
                    {"SKAdNetworkIdentifier": "8c4e2ghe7u.skadnetwork"},
                    {"SKAdNetworkIdentifier": "3rd42ekr43.skadnetwork"},
                    {"SKAdNetworkIdentifier": "97r2b46745.skadnetwork"},
                    {"SKAdNetworkIdentifier": "3qcr597p9d.skadnetwork"}
                ]
            })
    
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
        
    def will_modify_main_swift(self) -> bool:
        return True
    
    def modify_main_swift(self, libraries: list[str], modules: list[str]) -> list[CodeBlock]:
        return [
            CodeBlock(
                pre_main_swift,
                CodePriority.PRE_MAIN
            )
        ]
        
    def pre_main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        return pre_main_swift
        
    
backend = Admob4KivyBackend()