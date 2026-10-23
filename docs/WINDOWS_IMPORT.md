# Windows: prepare a shareable firmware research bundle

This workflow inventories two ZIP archives from PanicOpticon's research without modifying the originals.

## Prerequisites
- Windows PowerShell 5.1 or PowerShell 7
- Python 3.11+ (for optional extracted-file hashes and signature scans)
- Sufficient free disk space if you choose to extract the archives

## 1. Clone repository
```powershell
git clone https://github.com/jn90z/nokia5g21.git
cd nokia5g21
```

## 2. Inventory the ZIPs without extracting
```powershell
.\tools\prepare-research.ps1 -Archives "C:\Users\YOU\Downloads\archive1.zip","C:\Users\YOU\Downloads\archive2.zip"
```

Outputs under `reports/panicopticon/`:
- `archives.json`: archive names, byte sizes, SHA-256
- `zip-contents.csv`: member names, uncompressed and compressed sizes

The report is usually much smaller than the archives. Upload these two reports first.

## 3. Optional: extract and hash
```powershell
.\tools\prepare-research.ps1 -Archives "C:\Users\YOU\Downloads\archive1.zip","C:\Users\YOU\Downloads\archive2.zip" -Extract
```

Extracted files are stored under `firmware/panicopticon/<archive-name>/` and excluded from Git. The script refuses path traversal and overwriting files. Extract only if you trust the archive source and have enough space. If the ZIPs are *parts of one split archive* rather than two independent ZIPs, do not use this script to extract them; reassemble with the appropriate archive tool first.

## 4. Optional: scan extracted firmware candidates
```powershell
.\tools\prepare-research.ps1 -Archives "C:\Users\YOU\Downloads\archive1.zip","C:\Users\YOU\Downloads\archive2.zip" -Extract -ScanFirmware
```

Run this only on a fresh destination because extraction refuses overwrites. Scanning matches file extensions, so some embedded images may require manual selection. Signature hits are candidates, not confirmed partitions.

## Privacy and repository safety
Do not commit or upload raw firmware, private keys, IMEI, SIM data, or credentials. Review filenames and report contents before sharing. `reports/` and `firmware/` are ignored by Git.
