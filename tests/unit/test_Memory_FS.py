from unittest import TestCase
import memory_fs
from osbot_utils.utils.Files import parent_folder


class test_Memory_FS(TestCase):  # Test memory FS utils

    def test_memory_fs_path(self):  # Test that memory_fs.path is set correctly
        assert hasattr(memory_fs, 'path')
        assert memory_fs.path is not None
        assert type(memory_fs.path) is str

        # Verify it points to the memory_fs package directory
        assert memory_fs.path.endswith('memory_fs')

    def test_memory_fs_version(self):  # Test that version is accessible
        from memory_fs.utils.Version import version__memory_fs
        assert version__memory_fs is not None
        assert type(version__memory_fs) is str
        assert version__memory_fs.startswith('v')  # Version format