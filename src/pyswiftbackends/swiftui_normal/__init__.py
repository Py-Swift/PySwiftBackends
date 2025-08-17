from backend_tools import CodeBlock, FilePath
from ..standard_backend import CodePriority, StandardBackend
import pip



imports_swift = """
import SwiftUI
import PySerializing
import PySwiftWrapper
import PySwiftKit
"""

main_swift = """
@main
struct PySwiftApp: App {
    
    @StateObject var py_engine: PyEngine = .shared
    
    var body: some Scene {
        Text("PySwiftApp")
    }
}
"""



class SwiftUINormalBackend(StandardBackend):
    
    def packages(self) -> dict:
        print("adding PythonLauncher packages")
        return {
            "PythonLauncher": {
                "url": "https://github.com/Py-Swift/PythonLauncher",
                "branch": "master"
            }
        }
    
    def target_dependencies(self, target_type: str):
        deps = super().target_dependencies(target_type)
        deps.append(
            {"package": "PythonLauncher", "products": ["PythonLauncher"]}
        )
        
        return deps
    
    def wrapper_imports(self, target_type: str) -> list[dict[str, object]]:
        return [
            {
                "libraries": ["PythonLauncher"],
                "modules": []
            }
        ]
    
    def will_modify_main_swift(self) -> bool:
        return True
    
    def modify_main_swift(self, libraries: list[str], modules: list[str]) -> list["CodeBlock"]:
        return [
            CodeBlock(
                imports_swift,
                CodePriority.IMPORTS
            ),
            CodeBlock(
                main_swift,
                CodePriority.MAIN
            )
        ]
    
    
    
backend = SwiftUINormalBackend()