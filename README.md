# Signal Backup Viewer

A Python-based tool to convert Signal Desktop Backup archives (`.zip`) into a human-readable local interactive webpage.

## Features
- Dual-Mode Operation: Offers both an advanced Command Line Interface (CLI) and a intuitive graphical interface (GUI) via.
- Identity & Metadata Recovery: Automatically extracts and reflects native profile attributes (`givenName` from `main.jsonl`), group titles, custom avatar colors, `pinnedOrder` hierarchy, and disappearing message indicators (`expirationTimerMs`).
- **Composite Mapping Rule**: Employs an exact `(File Size, File Extension)` multi-key validation cache to accurately unpack and align system-obfuscated attachment logs.
- Full Data Preservation: Automatically copies the pristine untouched `main.jsonl` backup dictionary into your target directory for raw archival reliability.

## Directory Structure
```
signal-backup-viewer/
├── .gitignore              # Environment and local backup exclusion rules
├── README.md               # Documentation guide
├── requirements.txt        # Package dependencies (gradio, pyinstaller)
├── run.py                  # CLI command line entry point
├── gui.py                  # Web GUI interface entry point
└── src/                    # Encapsulated module package
    ├── __init__.py
    ├── cache.py            # ZIP inspection and composite asset mapping
    ├── parser.py           # Streamlined JSONL parsing and state management
    └── renderer.py         # Telegram DOM node serialization and HTML composition
```

## Directory Structure of Signal Desktop Backup
```
signal-export-YYYY-MM-DD-hh-mm-ss/
├── metadata.json
├── main.jsonl                  # All messages
└── files/                      # Attachment
    ├── 00/
    │   ├── 000a8...68a4d.jpg
    │   └── ...
    └── ...
```