from memory_fs.path_handlers.Path__Handler              import Path__Handler
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path

class Path__Handler__Latest(Path__Handler):       # Handler that stores files in a 'latest' directory
    name : Safe_Id = Safe_Id("latest")

    def generate_path(self) -> Safe_Str__File__Path:
        return Safe_Str__File__Path(f"latest")