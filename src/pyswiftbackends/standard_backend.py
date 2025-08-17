from backend_tools import FilePath, PSBackend, CodeBlock
import pip
import requests
import tarfile
import zipfile
import toml
import sh
from enum import IntEnum

pip3 = sh.Command("/Users/Shared/psproject/hostpython3/bin/pip3")

class CodePriority(IntEnum):
    IMPORTS = 0
    POST_IMPORTS = 1
    PRE_MAIN = 2
    MAIN = 3
    POST_MAIN = 4
    ON_EXIT = 5
    

class StandardBackend(PSBackend):
    
    def __init__(self):
        # pass self so swift side can access py side of the class
        super().__init__(self) # type: ignore
        
    # Swift Abstract functions being called
    
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
        
    def plist_entries(self, plist: object, target_type):
        pass
    
    
    
    def install(self, support: FilePath):
        pass
        
        
    def wrapper_imports(self, target_type: str) -> list[dict[str, object]]:
        return []
    
    def will_modify_main_swift(self) -> bool:
        return False

    def modify_main_swift(self, libraries: list[str], modules: list[str]) -> list["CodeBlock"]:
        return []
    
    def copy_to_site_packages(self, site_path: FilePath, platform: str):
        pass
    
    def will_modify_pyproject(self) -> bool:
        return False

    def modify_pyproject(self, path: "FilePath"):
        pass
    
    def exclude_dependencies(self) -> list[str]:
        return []
    
    
    # internal usage
    
    def pip_install(self, *args: str):
        print(pip3("install", *args))
    
    def pip_download(self, *args: str):
        print(pip3("download", *args))
    
    def download_file(self, url: str, save_path: str):
        try:
            # Send GET request to the URL
            response = requests.get(url)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Write the content of the response to a local file
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"File downloaded successfully: {save_path}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
            
    def untar_file(self, file: str, destination: str, keep_tar: bool = False):
        with tarfile.open(file) as tar:
            tar.extractall(destination)
            
    def unzip_file(self, file: str, destination: str, keep_zip: bool = False):
        z =  zipfile.ZipFile(file)
        z.extractall(destination)
            
    def load_pyproject_toml(self, path: str) -> dict[str, object]:
        with open(path, "r") as fp:
            return toml.load(fp)
        
    def save_pyproject_toml(self, obj: dict[str, object], path: str):
        with open(path, "w") as fp:
            toml.dump(obj, fp)