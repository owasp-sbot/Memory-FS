from unittest                                                                               import TestCase
from osbot_utils.type_safe.primitives.domains.files.safe_uint.Safe_UInt__FileSize           import Safe_UInt__FileSize
from osbot_utils.utils.Objects                                                              import __
from memory_fs.schemas.Schema__Memory_FS__File__Metadata                                    import Schema__Memory_FS__File__Metadata
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path           import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash    import Safe_Str__Cache_Hash


class test_Schema__Memory_FS__File__Metadata(TestCase):                                # Test file metadata schema

    def test__init__(self):                                                             # Test initialization with defaults
        with Schema__Memory_FS__File__Metadata() as _:
            assert type(_) is Schema__Memory_FS__File__Metadata
            assert _.obj() == __(content__hash         = None       ,
                                 content__size         = 0          ,
                                 data                  = __()       ,
                                 chain_hash            = None       ,
                                 previous_version_path = None       ,
                                 tags                  = []         ,
                                 timestamp             = _.timestamp)

    def test__with_values(self):                                                        # Test initialization with values
        content_hash  = Safe_Str__Cache_Hash('abc1234567')                                    # default value needs to be 10 chars
        content_size  = Safe_UInt__FileSize(1024)
        chain_hash    = Safe_Str__Cache_Hash('def1234567')
        prev_path     = Safe_Str__File__Path('v1/file.json')
        tags          = {Safe_Str__Id('tag1'), Safe_Str__Id('tag2')}

        metadata = Schema__Memory_FS__File__Metadata(content__hash         = content_hash ,
                                                     content__size         = content_size ,
                                                     chain_hash            = chain_hash   ,
                                                     previous_version_path = prev_path    ,
                                                     tags                  = tags         )

        with metadata as _:
            assert _.content__hash         == content_hash
            assert _.content__size         == content_size
            assert _.chain_hash            == chain_hash
            assert _.previous_version_path == prev_path
            assert _.tags                  == tags
            assert _.timestamp             is not None                                  # Auto-generated



