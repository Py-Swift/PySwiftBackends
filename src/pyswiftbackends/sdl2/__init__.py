from backend_tools import FilePath, PSBackend
import pip


class SDL2Backend(PSBackend):
    
    def __init__(self):
        super().__init__(self)
    
    def url(self) -> str | None:
        return None
    
    def frameworks(self) -> list[FilePath]:
        sdl2_fw = FilePath.ps_support() + "sdl2_frameworks" # type: ignore
        
        return [
            (sdl2_fw + "SDL2.xcframework"),
            (sdl2_fw + "SDL2_image.xcframework"),
            (sdl2_fw + "SDL2_mixer.xcframework"),
            (sdl2_fw + "SDL2_ttf.xcframework")
        ]
        
    def downloads(self) -> list[str]:
        return []
    
    def config(self, root: FilePath):
        pass
    
    def packages(self) -> dict:
        return {}
    
    def target_dependencies(self, target_type: str) -> list[dict[str, object]]:
        return [
            {"framework": "Support/SDL2.xcframework"},
            {"framework": "Support/SDL2_image.xcframework"},
            {"framework": "Support/SDL2_mixer.xcframework"},
            {"framework": "Support/SDL2_ttf.xcframework"}
        ]
    
    
    def install(self, support: FilePath):
        
        sdl2_frameworks = FilePath.ps_support + "sdl2_frameworks" # type: ignore
        pip.main([
            "install", "kivy_sdl2", 
            "--extra-index-url", "https://pypi.anaconda.org/pyswift/simple",
            "-t", str(support + sdl2_frameworks)
            ])
        
    def wrapper_imports(self, target_type: str) -> list[dict[str, object]]:
        return []
        
        
backend = SDL2Backend()