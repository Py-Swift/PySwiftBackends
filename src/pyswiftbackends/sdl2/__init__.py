from backend_tools import FilePath
from ..standard_backend import StandardBackend
import pip


class SDL2Backend(StandardBackend):
    
    
    def frameworks(self) -> list[FilePath]:
        sdl2_fw = FilePath.ps_support() + "sdl2_frameworks" # type: ignore
        
        return [
            (sdl2_fw + "SDL2.xcframework"),
            (sdl2_fw + "SDL2_image.xcframework"),
            (sdl2_fw + "SDL2_mixer.xcframework"),
            (sdl2_fw + "SDL2_ttf.xcframework")
        ]
        
    
    def target_dependencies(self, target_type: str) -> list[dict[str, object]]:
        return [
            {"framework": "Support/SDL2.xcframework"},
            {"framework": "Support/SDL2_image.xcframework"},
            {"framework": "Support/SDL2_mixer.xcframework"},
            {"framework": "Support/SDL2_ttf.xcframework"}
        ]
    
    
    def install(self, support: FilePath):
        
        sdl2_frameworks = FilePath.ps_support() + "sdl2_frameworks" # type: ignore
        if not sdl2_frameworks.exists:
            self.pip_install(
                "kivy_sdl2", 
                "--extra-index-url", "https://pypi.anaconda.org/pyswift/simple",
                "-t", str(sdl2_frameworks)
            )
        
        
backend = SDL2Backend()