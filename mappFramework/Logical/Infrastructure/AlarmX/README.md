# mappAlarmExportImport

Export/import B&R mapp AlarmX list files to a single tab-delimited CSV for bulk editing in Excel or other tools.

**What this tool does**
1. Reads `AlarmXCfg.mpalarmxcore` to discover the referenced list IDs.
2. Resolves those IDs to actual `*.mpalarmxlist` files in the same folder.
3. Exports all alarms into one CSV (tab-delimited).
4. Imports the CSV and updates each list, preserving existing properties.

**Features**
- Single CSV
- List routing included via `List File` and `List ID`.
- Fixed columns for common alarm properties (Confirm, Recording, etc.).
- Dynamic `Extra:` columns for any additional properties discovered.
- No-argument mode opens a Tkinter UI.

## Requirements
- Python 3.10+
- Packages from `requirements.txt`

## Install
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### No arguments (Tkinter UI)
```powershell
python AlarmImportExport.py
```
Use the UI to choose:
- Mode: Export or Import
- CSV path
- `*.mpalarmxcore` path

### With arguments
All file paths can be absolute or relative. Examples below use relative paths.

Export:
```powershell
python AlarmImportExport.py -e true -c AlarmTriggers.csv -m AlarmXCfg.mpalarmxcore
```

Import:
```powershell
python AlarmImportExport.py -c AlarmTriggers.csv -m AlarmXCfg.mpalarmxcore
```
#### Arguments
- `-e`, `--export`
  Enable export mode. If not set, the script runs import mode. Default: `false`.
- `-c`, `--csv-file <path>`
  Path to the CSV file (tab-delimited). Default: `AlarmTriggers.csv`. Example: `data/AlarmTriggers.csv`
- `-m`, `--mpalarmxcore <path>`
  Path to the `*.mpalarmxcore` file. Default: `AlarmXCfg.mpalarmxcore`. Example: `... \mappServices\AlarmX\AlarmXCfg.mpalarmxcore`

## CSV Format
- The CSV is **tab-delimited** (Excel compatible). This is important for fields
  like multi-dimension arrays (for example `[x,y]`) that may contain commas.
- Core columns include:
  - `List File`, `List ID`, `Name`, `Message`, `Code`, `Severity`, `Behavior`
  - Common behavior and recording fields (Confirm, Recording, etc.)
  - Monitoring fields (Monitored PV, Delay, Limits, etc.)
- Any additional properties found in the XML are exported as:
  - `Extra:<path>` columns (for example `Extra:Behavior/DataUpdate/Activation/TimeStamp`)

## Notes
- Import merges by `Name` to preserve existing properties not present in the CSV.
- Empty CSV cells do not overwrite existing values.
