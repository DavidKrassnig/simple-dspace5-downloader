# Simple DSpace5 Downloader

This script takes a CSV list of metadata entries for a DSpace 5.x instance and downloads all of the associated files from the repository (if publically accessible).
This script may or may not work with DSpace versions newer than that, but was developed for my own use case, which happened to be DSpace 5.

## Usage

To use this script, use Python3 from your terminal/console of choice.

**Positional Arguments:**

| Argument   | Effect                                 |
| ---------- | -------------------------------------- |
| csv_file   | Input CSV file path                    |
| base_url   | Input base domain of DSpace repository |