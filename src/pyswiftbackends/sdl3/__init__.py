from backend_tools import FilePath
from ..standard_backend import StandardBackend
import pip


class SDL3Backend(StandardBackend):
    
    
    def frameworks(self) -> list[FilePath]:
        sdl_fw = FilePath.ps_support() + "sdl3_frameworks" # type: ignore
        
        return [
            (sdl_fw + "SDL3.xcframework"),
            (sdl_fw + "SDL3_image.xcframework"),
            (sdl_fw + "SDL3_mixer.xcframework"),
            (sdl_fw + "SDL3_ttf.xcframework"),
            (sdl_fw + "libEGL.xcframework"),
            (sdl_fw + "libGLESv2.xcframework")
        ]
        
    
    def target_dependencies(self, target_type: str) -> list[dict[str, object]]:
        return [
            {"framework": "Support/SDL3.xcframework"},
            {"framework": "Support/SDL3_image.xcframework"},
            {"framework": "Support/SDL3_mixer.xcframework"},
            {"framework": "Support/SDL3_ttf.xcframework"},
            {"framework": "Support/libEGL.xcframework"},
            {"framework": "Support/libGLESv2.xcframework"}
        ]
    
    
    def install(self, support: FilePath):
        
        sdl_frameworks = FilePath.ps_support() + "sdl3_frameworks" # type: ignore
        if not sdl_frameworks.exists:
            self.pip_install(
                "kivy_sdl3_angle", 
                "--extra-index-url", "https://pypi.anaconda.org/pyswift/simple",
                "-t", str(sdl_frameworks)
            )
        
        
backend = SDL3Backend()