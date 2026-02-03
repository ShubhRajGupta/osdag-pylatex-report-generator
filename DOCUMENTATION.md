# Documentation: Beam Analysis Report Generator

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Usage Guide](#usage-guide)
5. [Script Architecture](#script-architecture)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [API Reference](#api-reference)

---

## Introduction

The Beam Analysis Report Generator is a Python application that automates the creation of professional engineering reports for structural beam analysis. It bridges the gap between raw numerical data and presentation-ready documentation by:

- Reading beam force data from Excel spreadsheets
- Generating LaTeX documents with embedded vector graphics
- Compiling to high-quality PDF reports

### Key Features

| Feature | Description |
|---------|-------------|
| **Vector Graphics** | SFD and BMD rendered using TikZ/pgfplots (infinite zoom, no pixelation) |
| **Selectable Tables** | Data tables are native LaTeX (copy-paste friendly) |
| **Professional Layout** | Title page, TOC, headers, footers, and hyperlinks |
| **Modular Design** | Easy to extend or modify individual sections |
| **Automated Compilation** | Runs pdflatex automatically with proper passes |

---

## System Requirements

### Software Requirements

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8+ | 3.10+ |
| LaTeX Distribution | MiKTeX 21.0 / TeX Live 2021 | Latest |
| pandas | 1.3+ | 2.0+ |
| openpyxl | 3.0+ | 3.1+ |

### Required LaTeX Packages

The following packages are used and must be available:

```latex
\usepackage{geometry}      % Page layout
\usepackage{graphicx}      % Image embedding
\usepackage{booktabs}      % Professional tables
\usepackage{array}         % Enhanced arrays
\usepackage{float}         % Float placement
\usepackage{xcolor}        % Color definitions
\usepackage{colortbl}      % Colored table rows
\usepackage{tikz}          % Vector graphics
\usepackage{pgfplots}      % Plot generation
\usepackage{hyperref}      % Hyperlinks
\usepackage{fancyhdr}      % Headers/footers
\usepackage{titlesec}      % Title formatting
\usepackage{tocloft}       % TOC customization
```

---

## Installation

### Step 1: Install Python Dependencies

```powershell
pip install pandas openpyxl
```

### Step 2: Verify LaTeX Installation

```powershell
pdflatex --version
```

If not installed, download MiKTeX from: https://miktex.org/download

### Step 3: Prepare Input Files

Ensure the following files are in the project directory:

1. `Force Table.xlsx` - Your beam analysis data
2. `simply_supported_beam.png` - Beam diagram image

---

## Usage Guide

### Basic Usage

```powershell
cd X:\Participations\FOSSEE\Latex2
python code.py
```

### Expected Output

```
============================================================
BEAM ANALYSIS REPORT GENERATOR
============================================================
[INFO] Loading data from Excel file...
[INFO] Loaded 11 data points
[INFO] Beam length: 15.0 m
[INFO] Generating LaTeX document...
[INFO] Writing LaTeX file: ...\Beam_Analysis_Report.tex
[INFO] Compiling LaTeX to PDF...
[INFO] pdflatex run 1/2...
[INFO] pdflatex run 2/2...
============================================================
[SUCCESS] PDF generated: ...\Beam_Analysis_Report.pdf
============================================================
```

### Custom Usage (Programmatic)

```python
from code import BeamReportGenerator

generator = BeamReportGenerator(
    excel_path="path/to/data.xlsx",
    beam_image_path="path/to/beam.png",
    output_name="Custom_Report"
)

pdf_path = generator.generate_report()
```

---

## Script Architecture

### Class Diagram

```
BeamReportGenerator
├── __init__(excel_path, beam_image_path, output_name)
├── load_data() -> None
├── generate_report() -> str
│
├── Private Methods (LaTeX Generation)
│   ├── _create_preamble() -> str
│   ├── _create_title_page() -> str
│   ├── _create_toc() -> str
│   ├── _create_introduction() -> str
│   ├── _create_data_table() -> str
│   ├── _create_sfd_diagram() -> str
│   ├── _create_bmd_diagram() -> str
│   ├── _create_conclusion() -> str
│   └── _cleanup_aux_files(output_dir) -> None
│
└── Attributes
    ├── excel_path: str
    ├── beam_image_path: str
    ├── output_name: str
    ├── data: pd.DataFrame
    └── beam_length: float
```

### Data Flow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Force Table    │────▶│  BeamReport      │────▶│  .tex file      │
│  (.xlsx)        │     │  Generator       │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐                              ┌────────▼────────┐
│  Beam Image     │─────────────────────────────▶│  pdflatex       │
│  (.png)         │                              │                 │
└─────────────────┘                              └────────┬────────┘
                                                          │
                                                 ┌────────▼────────┐
                                                 │  .pdf file      │
                                                 │  (Final Report) │
                                                 └─────────────────┘
```

---

## Customization

### Changing Colors

Edit the color definitions in `_create_preamble()`:

```python
\definecolor{shearpositive}{RGB}{70, 130, 180}    % Steel Blue
\definecolor{shearnegative}{RGB}{220, 20, 60}     % Crimson Red
\definecolor{momentpositive}{RGB}{34, 139, 34}    % Forest Green
\definecolor{titleblue}{RGB}{0, 51, 102}          % Dark Blue
```

### Adding New Sections

1. Create a new method: `_create_your_section() -> str`
2. Call it in `generate_report()` before `_create_conclusion()`

### Modifying Chart Appearance

Edit the pgfplots options in `_create_sfd_diagram()` or `_create_bmd_diagram()`:

```python
width=0.95\textwidth,    # Chart width
height=8cm,              # Chart height
bar width=8pt,           # Bar thickness
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `pdflatex not found` | LaTeX not in PATH | Add MiKTeX/bin to system PATH |
| `Package not found` | Missing LaTeX package | Run MiKTeX Package Manager |
| `Excel read error` | Missing openpyxl | `pip install openpyxl` |
| `Image not found` | Wrong path | Use absolute path or check filename |

### LaTeX Compilation Warnings

Some warnings are normal and don't affect output:

- `headheight is too small` - Cosmetic warning, can be ignored
- `Overfull \hbox` - Text slightly exceeds margin, usually OK

---

## API Reference

### BeamReportGenerator

#### Constructor

```python
BeamReportGenerator(
    excel_path: str,
    beam_image_path: str,
    output_name: str = "Beam_Analysis_Report"
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `excel_path` | str | Path to Excel file with force data |
| `beam_image_path` | str | Path to beam diagram image |
| `output_name` | str | Output filename (without extension) |

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `load_data()` | None | Loads and validates Excel data |
| `generate_report()` | str | Generates PDF, returns path |

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `data` | DataFrame | Loaded force/moment data |
| `beam_length` | float | Calculated beam length (m) |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Initial release |

---

*Documentation generated for FOSSEE Project - February 2026*
