# Known Bugs and Logic Issues

This document captures issues discovered during a quick code review. Line numbers refer to the current main branch.

## Memory_FS__File__Create.create
File: `memory_fs/file/actions/Memory_FS__File__Create.py`

```
26      def create(self):
27          with self.file__data() as _:
28              if _.exists() is False:
29                  return self.file__edit().create__config()
30              return False
```

* The return type is not declared but should be `List[Safe_Str__File__Path]`.
* When the file already exists the method returns `False`, however callers expect an empty list.

## Memory_FS__Delete.delete
File: `memory_fs/actions/Memory_FS__Delete.py`

```
25      def delete(self, file_config : Schema__Memory_FS__File__Config
26                  ) -> Dict[Safe_Id, bool]:
27          files_deleted         = self.memory_fs__edit().delete        (file_config)
28          files_deleted_content = self.memory_fs__edit().delete_content(file_config)
29          return files_deleted + files_deleted_content
```

* The annotation claims a `Dict[Safe_Id, bool]` is returned but the code concatenates two lists of paths.
* Either the return type or implementation should be corrected.

## Memory_FS__File__Name.content
File: `memory_fs/file/actions/Memory_FS__File__Name.py`

```
33      def content(self) -> Safe_Str__File__Path:
34          elements = [self.file__config.file_id]     # BUG: need to handle null values in file_extension
35          if self.file__config.file_type.file_extension:
36              elements.append(str(self.file__config.file_type.file_extension))
37          return self.build(elements)
```

* When `file_extension` is `None` the resulting file name becomes `"<id>.None"`.
* The method should skip adding the extension in that case.

## Metadata size not captured
Several tests highlight that the stored `content__size` value remains `0` even after saving file data.
The `Memory_FS__Edit.save` and `save_content` helpers do not calculate or update this metadata, leading to inconsistent file information.
