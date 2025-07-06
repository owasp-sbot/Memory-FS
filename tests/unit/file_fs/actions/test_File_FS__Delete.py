from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from tests.unit.Base_Test__File_FS                      import Base_Test__File_FS


class test_File_FS__Delete(Base_Test__File_FS):

    def setUp(self):                                                        # Initialize test data
        super().setUp()
        self.file_create = self.file.file_fs__create()
        self.file_delete = self.file.file_fs__delete()

    def test_delete(self):                                                          # todo: research why this test takes so long
        assert self.file.exists       () is False                                   #       this is a good example of some of the areas we should be able to optimise, since all this is happening in memory
        assert self.file_delete.delete() == []
        assert self.file_create.create() == self.file__created_files
        assert self.file.exists       () is True
        assert self.file_delete.delete() == self.file__created_files
        assert self.file_delete.delete() == []
        assert self.file.exists       () is False

    def test_delete__config(self):                                          # Test config file deletion
        with self.file_create as _:
            _.create__config()
            assert _.file_fs__config().exists()      is True
            assert self.file_delete.delete__config() == [f"{self.file.file_id()}.json.config"]
            assert _.file_fs__config().exists()      is False

    def test_delete__content(self):                                         # Test content file deletion
        content = b'test content'

        with self.file_create as _:
            _.create__content(content)
            assert self.storage_fs.file__exists(Safe_Str__File__Path(f'{self.file_config.file_id}.json')) is True
            assert self.file_delete.delete__content()                                                     == [f'{self.file_config.file_id}.json']
            assert self.storage_fs.file__exists(Safe_Str__File__Path(f'{self.file_config.file_id}.json')) is False