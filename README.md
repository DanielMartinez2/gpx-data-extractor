# GPX Data Extractor

Python command-line tool for extracting geographic and elevation data from GPX files into structured TXT output.

The project parses GPX/XML files, extracts waypoint information and converts the data into a tab-separated text format that can be reused in other workflows or data-processing tools.

## Technologies

* Python
* XML
* GPX
* `xml.etree.ElementTree`
* `argparse`
* Regular expressions
* `pathlib`
* Command-line interfaces

No external Python dependencies are required.

## Features

* Process a single GPX file
* Process multiple GPX files from a directory
* Extract waypoint coordinates
* Extract elevation data
* Extract waypoint names and descriptions
* Extract distance and angle information from GPX descriptions
* Automatically detect the GPX XML namespace
* Generate one structured TXT file for each GPX input
* Automatically create the output directory
* Support custom input and output paths
* Preserve UTF-8 text output

## Extracted Data

Each waypoint can generate the following fields:

```text
type
latitude
longitude
altitude (m)
distance (km)
name
desc
angle
```

The output uses tab-separated values, making it easy to inspect or import into other tools.

## Project Structure

```text
gpx-data-extractor/
├── examples/
│   ├── input/
│   │   └── linha_0.gpx
│   └── output/
│       └── linha_0.txt
│
├── .gitignore
├── gpx_extractor.py
└── README.md
```

## Requirements

* Python 3

The project uses only modules from the Python standard library, so no additional packages need to be installed.

## Usage

### Process a directory

To process all `.gpx` files inside a directory:

```bash
python gpx_extractor.py --input examples/input --output examples/output
```

The script searches the specified input directory for GPX files and creates one TXT file for each input file.

For example:

```text
examples/input/linha_0.gpx
```

generates:

```text
examples/output/linha_0.txt
```

### Process a single GPX file

You can also process only one file:

```bash
python gpx_extractor.py \
  --input examples/input/linha_0.gpx \
  --output examples/output
```

## Command-Line Arguments

| Argument   | Required | Description                                          |
| ---------- | -------- | ---------------------------------------------------- |
| `--input`  | Yes      | Path to a GPX file or directory containing GPX files |
| `--output` | No       | Directory where TXT files will be generated          |

If `--output` is omitted, the default directory is:

```text
output/
```

## Example Output

The generated file starts with:

```text
type	latitude	longitude	altitude (m)	distance (km)	name	desc	angle
```

Each GPX waypoint is then written as a new row.

Conceptually:

```text
W	-16.0000	-48.0000	950	0	Point 1	Waypoint description	90
W	-16.0001	-48.0002	955	0.25	Point 2	Waypoint description	110
```

The exact values depend on the contents of the GPX file.

## How It Works

The processing flow is:

```text
GPX file
   │
   ▼
XML parsing
   │
   ├── Detect GPX namespace
   │
   ▼
Find waypoints
   │
   ├── latitude
   ├── longitude
   ├── elevation
   ├── name
   └── description
          │
          ▼
Extract distance and angle
          │
          ▼
Create structured waypoint data
          │
          ▼
Write TXT output
```

## GPX Parsing

The application uses Python's built-in:

```python
xml.etree.ElementTree
```

to parse GPX files.

Instead of depending on a fixed GPX namespace, the script detects the namespace from the XML root element.

This makes the parser less dependent on one specific GPX file structure.

## Distance and Angle Extraction

Some GPX generators store additional information such as distance and angle inside HTML-formatted waypoint descriptions.

The script analyzes `<td>` elements in the description and searches for fields labeled:

```text
Distance
Angle
```

If explicit labels are not found, the script also includes a fallback strategy based on the position of the values in the description.

## File Processing

When the input is a directory:

```bash
python gpx_extractor.py --input routes
```

the application searches for:

```text
*.gpx
```

and processes the files in sorted order.

When the input is a single file, the program validates that it has the `.gpx` extension before processing it.

## Output Naming

Output filenames are automatically derived from the input filename.

For example:

```text
route_01.gpx
```

becomes:

```text
route_01.txt
```

This means the application does not depend on a specific filename convention.

## Error Handling

The application stops with a clear message when:

* the input path does not exist;
* a single input file does not have the `.gpx` extension;
* no GPX files are found in the selected directory.

Examples:

```text
Input path not found: routes
```

```text
The input file must have a .gpx extension.
```

```text
No GPX files found.
```

## Example

The repository includes a sample GPX file:

```text
examples/input/linha_0.gpx
```

and the corresponding generated output:

```text
examples/output/linha_0.txt
```

This allows the extraction workflow to be tested without needing an external dataset.

## What This Project Demonstrates

This project demonstrates practical knowledge of:

* Python scripting
* XML parsing
* GPX file processing
* geospatial data extraction
* command-line interfaces
* file and directory manipulation
* regular expressions
* structured data transformation
* batch file processing
* input validation
* separation of processing responsibilities

## Possible Improvements

Future versions could include:

* CSV output
* JSON output
* support for GPX tracks and routes in addition to waypoints
* command-line selection of output format
* automatic unit conversion
* elevation statistics
* total route distance calculation
* GeoJSON export
* automated tests
* logging
* packaging as an installable Python CLI
* visualization of extracted points on a map

## Author

**Daniel Martínez Alencar Freitas**

GitHub: [DanielMartinez2](https://github.com/DanielMartinez2)
