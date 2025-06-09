# Threat Model for Memory-FS

Memory-FS is an in-memory file system that stores file metadata and content entirely in memory. The library exposes a facade (`Memory_FS`) and a set of action classes to manipulate files. This document outlines potential threats to the system and recommended mitigations.

## Assets
- In-memory file metadata and content
- File configuration schemas and path handlers
- Interface for saving, loading and editing files

## Attack Surfaces
1. **API Usage** – Any consumer can interact with `Memory_FS` and the underlying action classes.
2. **Path Handlers** – Custom path handlers influence how and where files are stored in memory.
3. **File Types** – Serialization and deserialization logic for each file type may process untrusted data.
4. **In-Memory Storage** – The `Memory_FS__File_System` keeps all data in dictionaries within the running process.

## Threats
| ID | Threat | Description |
|----|--------|-------------|
| T1 | Unauthorized Access | If the application exposes `Memory_FS` to untrusted callers, files could be read or modified without permission. |
| T2 | Memory Exhaustion | Attackers might store numerous large files, exhausting available memory and causing denial of service. |
| T3 | Path Collisions | Malicious path handlers could overwrite existing files or bypass expected organization. |
| T4 | Malicious Serialization | File types that rely on unsafe serialization formats (e.g., pickle) could lead to code execution. |
| T5 | Data Leakage | Since data resides only in memory, crashes or debug dumps may expose sensitive content. |
| T6 | Inconsistent State | Unexpected termination (e.g., process crash) can leave callers assuming data is persisted when it is not. |

## Mitigations
- **Access Control**: Ensure that only authorized components create or manipulate `Memory_FS` instances. Limit exposure of internal dictionaries.
- **Input Validation**: Use the existing type-safe models to validate all external input, particularly for file names, path handler parameters and data passed to serialization routines.
- **Resource Limits**: Enforce size limits for individual files and the total number of files stored. Consider periodic cleanup or memory quotas.
- **Safe Serialization**: Avoid unsafe formats like pickle. Prefer formats with strict parsers (JSON, YAML with safe loader, etc.).
- **Crash Handling**: Document that Memory-FS is volatile. If persistence is required, ensure data is saved to a durable backend before shutdown.
- **Testing and Review**: Regularly run the provided unit tests (`pytest`) and perform security reviews of custom path handlers and file types.

## Conclusion
Memory-FS is designed for flexibility and speed, but its in-memory nature introduces unique risks. By applying strict input validation, safe serialization practices, and controlling access to the API, most common threats can be mitigated. Future persistent storage adapters (S3, SQLite, local filesystem) should include similar threat modeling with emphasis on their specific attack surfaces.
