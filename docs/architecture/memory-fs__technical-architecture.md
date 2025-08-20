# Memory_FS Technical Architecture

## Overview

Memory_FS is a flexible file system abstraction that decouples storage backends from path strategies, enabling sophisticated file management patterns with minimal complexity. Each Memory_FS instance represents a specific combination of one storage backend and multiple path handlers, allowing the same file to be saved to multiple locations simultaneously.

## Core Architecture Principles

### 1. Separation of Concerns
- **Storage Layer**: Handles raw I/O operations (read, write, delete)
- **Path Strategy Layer**: Determines where files are stored
- **File Operations Layer**: Manages file lifecycle and metadata
- **Entry Point Layer**: Provides configuration API

### 2. Instance-Based Composition
- One Memory_FS instance = One storage backend + Multiple path handlers
- Multiple Memory_FS instances can share the same storage backend
- Each instance handles a specific use case (cache, logs, metrics)
- No central registry or project configuration needed

### 3. Context Manager Pattern
Configuration uses Python's context manager for clear setup:
```python
with Memory_FS() as _:
    storage = _.set_storage__s3(bucket, prefix)
    handler = _.add_handler__latest()
    handler.prefix_path = Safe_Str__File__Path('models')
    fs = _
```

## Component Layers

### Layer 1: Storage Backends (Storage_FS)

Abstract base class with consistent interface across storage types:

```
Storage_FS (Abstract Base)
    ├── Storage_FS__Memory      # In-memory dictionary
    ├── Storage_FS__Local_Disk   # Local filesystem
    ├── Storage_FS__Sqlite       # SQLite database
    ├── Storage_FS__Zip          # ZIP archive
    └── Storage_FS__S3           # AWS S3 (external)
```

Required methods:
- `file__bytes(path)` - Read raw bytes
- `file__save(path, data)` - Write bytes
- `file__delete(path)` - Remove file
- `file__exists(path)` - Check existence
- `file__json(path)` - Read as JSON
- `file__str(path)` - Read as string

### Layer 2: Path Handlers

Path handlers generate file paths with flexible prefix/suffix support:

```
Path__Handler (Base Class)
├── Properties:
│   ├── prefix_path  # Optional path prefix
│   └── suffix_path  # Optional path suffix
└── Methods:
    ├── generate_path()   # Returns complete path
    └── combine_paths()   # Handles prefix + middle + suffix

Path__Handler__Latest     # Fixed "latest" directory
Path__Handler__Temporal    # Time-based hierarchy
Path__Handler__Versioned   # Version-numbered paths
Path__Handler__Custom      # User-defined paths
```

The base `combine_paths()` method automatically handles:
1. Adding prefix_path if set
2. Adding handler-specific middle segments
3. Adding suffix_path if set

### Layer 3: File Operations (File_FS)

File_FS manages individual files with:
- **Multi-path support**: Same file stored in multiple locations
- **Three-file pattern**:
  - `.config` - Immutable configuration
  - `.json` - Actual content (with .json extension or configured extension)
  - `.metadata` - Hash, size, timestamp
- **Type-aware serialization**: JSON, text, binary, base64

### Layer 4: Memory_FS Entry Point

Main interface that:
- Manages storage configuration (returns storage object for further config)
- Maintains path handler list (returns handlers for modification)
- Creates File_FS instances with proper configuration
- Provides type-specific file creation (json, text, data)

### Layer 5: Pattern Classes

Pre-configured Memory_FS subclasses for common patterns:
```
Memory_FS__Latest           # Single latest path
Memory_FS__Temporal         # Time-based paths only
Memory_FS__Latest_Temporal  # Latest + temporal backup
Memory_FS__Versioned        # Version numbers only
Memory_FS__Versioned_Latest # Versions + latest
```

Pattern classes accept `**kwargs` to pass Path__Handler properties (prefix_path, suffix_path, etc.) to all handlers.

## Data Flow

### Write Operation
```
User Data → Memory_FS.file__json(file_id)
    ↓
Create File_FS with:
  - file_id
  - paths from all handlers
  - storage reference
    ↓
File_FS.create(data)
    ↓
For each path:
  - Serialize based on type
  - Save .config.json
  - Save .{id}.json (content)
  - Save .metadata.json
    ↓
Storage_FS.file__save(path, bytes)
```

### Read Operation
```
Memory_FS.file__json(file_id) → File_FS instance
    ↓
File_FS.content()
    ↓
Check paths in order (first wins):
  - Storage_FS.file__bytes(path)
    ↓
Deserialize based on type → Return data
```

## Path Generation Example

With a Memory_FS configured with both latest and temporal handlers:

```python
with Memory_FS() as _:
    storage = _.set_storage__s3('bucket', 'data')
    
    latest = _.add_handler__latest()
    latest.prefix_path = Safe_Str__File__Path('production')
    latest.suffix_path = Safe_Str__File__Path('current')
    # Generates: production/latest/current/
    
    temporal = _.add_handler__temporal(areas=['models'])
    temporal.prefix_path = Safe_Str__File__Path('production')
    temporal.suffix_path = Safe_Str__File__Path('archive')
    # Generates: production/2024/01/15/10/models/archive/
```

File with id "response_123" would be saved to:
- `production/latest/current/response_123.json`
- `production/latest/current/response_123.config.json`
- `production/latest/current/response_123.metadata.json`
- `production/2024/01/15/10/models/archive/response_123.json`
- `production/2024/01/15/10/models/archive/response_123.config.json`
- `production/2024/01/15/10/models/archive/response_123.metadata.json`

## Usage Patterns

### Pattern 1: Simple Cache
```python
with Memory_FS__Latest() as _:
    _.set_storage__memory()
    cache_fs = _
```

### Pattern 2: Shared Storage, Different Strategies
```python
storage = Storage_FS__S3(bucket="app-data").setup()

# Critical data: latest + temporal backup
with Memory_FS__Latest_Temporal(storage_fs=storage) as _:
    fs_critical = _

# Logs: temporal only with areas
with Memory_FS__Temporal(storage_fs=storage, areas=['logs']) as _:
    fs_logs = _
```

### Pattern 3: Complex Path Customization
```python
with Memory_FS() as _:
    storage = _.set_storage__sqlite(db_path="/data/cache.db")
    
    # Configure versioned handler
    versioned = _.add_handler__versioned()
    versioned.prefix_path = Safe_Str__File__Path('releases')
    versioned.set_version(3)
    
    # Configure latest handler
    latest = _.add_handler__latest()
    latest.latest_folder = Safe_Str__File__Path('stable')
    
    fs = _
```

## Key Design Decisions

### Why Multiple Memory_FS Instances?

Instead of one Memory_FS with named strategies, each instance owns its path configuration because:
- **Simplicity**: No routing logic or strategy registry
- **Flexibility**: Each use case gets exactly what it needs
- **Edge cases**: Complex scenarios (entire filesystems at temporal leaves) handled naturally
- **Clear ownership**: No confusion about which strategy applies

### Why Return Storage/Handler Objects?

The `set_storage__*` and `add_handler__*` methods return the created objects (not self) to allow:
- **Further configuration**: Modify storage or handler properties after creation
- **Direct access**: No need for getter methods
- **Explicit control**: Clear what's being configured

### Why Three-File Pattern?

Separating config, content, and metadata provides:
- **Immutable configuration**: Config can't be modified after creation
- **Efficient updates**: Only content/metadata change
- **Atomic verification**: Can check all parts exist
- **Separate access patterns**: Different read/write patterns for each

### Why Prefix/Suffix in Base Class?

Having prefix_path and suffix_path in Path__Handler base class:
- **Eliminates duplication**: One implementation in combine_paths()
- **Consistent behavior**: All handlers work the same way
- **Maximum flexibility**: Any handler can have any prefix/suffix
- **Clean subclasses**: Handlers only implement their unique logic

## Performance Characteristics

- **Shared storage**: Multiple Memory_FS instances share one connection
- **Lazy loading**: Data only loaded when requested
- **Path priority**: First path checked first (optimize for common case)
- **No caching**: Each operation goes to storage (storage layer can cache)

## Extension Points

1. **Custom storage**: Implement Storage_FS interface
2. **Custom handlers**: Extend Path__Handler base
3. **Custom file types**: Define new Schema__Memory_FS__File__Type
4. **Custom serialization**: Add new Enum__Memory_FS__Serialization
5. **Custom patterns**: Subclass Memory_FS with pre-configured handlers

## Simplified Architecture Summary

The entire system is now just three core concepts:

```
Memory_FS (configuration layer)
    ↓
File_FS (operations layer)
    ↓
Storage_FS (I/O layer)
```

With path handlers as simple strategy objects that generate paths, not complex routing systems. This achieves the original vision of flexible file management while keeping the implementation straightforward and maintainable.