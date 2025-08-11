from backend_tools import FilePath, PSBackend
import pip


class StandardBackend(PSBackend):
    
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
        return {}
    
    def target_dependencies(self, target_type: str) -> list[dict[str, object]]:
        return []
        
    def plist_entries(self, plist: dict[str, object], target_type: str):
        pass
    
    
    def install(self, support: FilePath):
        pass
        
        
    def wrapper_imports(self, target_type: str) -> list[dict[str, object]]:
        return []
    
    def pre_main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        pass
    
    def main_swift(self, libraries: list[str], modules: list[str]) -> str | None:
        pass