# Smart House Research Toolkit

An open-source Python toolkit for working with environmental and IoT sensor data from the DigiTech Smart House Data Pack.

The project aims to make the Smart House dataset easier to explore and analyse by providing reusable, tested Python tools for researchers, students and developers.

> **This project is currently in early development, and contributions are very welcome!**

## About the project

The DigiTech Smart House produces data from a range of environmental and IoT sensors. The available data includes measurements relating to areas such as air quality, indoor and outdoor climate, weather and other smart-building systems.

Working with the Data Pack isn't always straightforward. Data comes from several different sensor platforms, and file formats, measurements and availability can vary between dataset releases.

Smart House Research Toolkit aims to make working with those differences easier by providing a growing collection of reusable Python tools.

The goal is to create functionality that can support lots of different Smart House research projects.

## Project status

🚧 **Early development**

At the moment, the project includes:

* a Python package structure for data processing, analysis and visualisation
* a catalogue describing the high-level data sources available across dataset releases
* an initial loader for WeatherLink CSV exports
* automated tests using pytest
* code quality checks using Ruff
* GitHub Actions for automated testing and linting

There is still plenty to build, so this is also a great time to get involved.

Features such as additional data loaders, data-cleaning utilities, environmental calculations, research workflows and visualisations are planned but should not be considered fully implemented yet.

## The DigiTech Smart House Data Pack

The toolkit is designed around the **DigiTech Smart House Data Pack**, which currently contains dataset releases covering 2022–2025.

The Data Pack includes exports from several systems:

| Source               | 2022 | 2023 | 2024 | 2025 |
| -------------------- | :--: | :--: | :--: | :--: |
| GlazeAlarm           |   ✓  |   ✓  |   *  |   ✓  |
| Invisible Systems    |   ✓  |   ✓  |   ✓  |   ✓  |
| WeatherLink          |   ✓  |   ✓  |   ✓  |   ✓  |
| SDS                  |   —  |   —  |   ✓  |   —  |
| Air Quality Data     |   —  |   —  |   —  |   ✓  |
| Moisture Sensors     |   —  |   —  |   —  |   ✓  |
| Air Source Heat Pump |   —  |   —  |   —  |   ✓  |

* The dataset structure does not always line up neatly with calendar years. For example, GlazeAlarm data published with the 2022 release extends beyond 2022.

One of the principles of this project is therefore **not to assume that a dataset folder year is the same thing as the actual observation period**.

The toolkit will increasingly provide metadata and utilities to make these differences easier to understand.

## Getting started

Smart House Research Toolkit is a Python project and is intended to work across **Windows, macOS and Linux**.

If you want to use or explore the toolkit, you can clone the repository directly.

### Requirements

You'll need:

* Python 3.11 or newer
* Git
* pip

Clone the repository:

```bash
git clone https://github.com/jddrtn/smart-house-research-toolkit.git
cd smart-house-research-toolkit
```

### Create a virtual environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Then activate it using the command for your operating system and terminal.

#### Windows — Command Prompt

```cmd
.venv\Scripts\activate
```

#### Windows — PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### macOS and Linux

```bash
source .venv/bin/activate
```

Once activated, your terminal should normally show `(.venv)` before the command prompt.

### Install the toolkit

Install the project and its development dependencies:

```bash
pip install -e ".[dev]"
```

You can check that the package is available with:

```bash
python -c "import smarthouse; print('Smart House Research Toolkit is installed')"
```

## Getting the dataset

The DigiTech Smart House Data Pack is **not included in this repository**.

You'll need to download it separately from Kaggle:

https://www.kaggle.com/datasets/ssiatuos/smart-house-data-pack

If you use the Kaggle CLI, you can download and extract the dataset into the project's `data/raw` directory:

```bash
kaggle datasets download ssiatuos/smart-house-data-pack -p data/raw --unzip
```

The toolkit expects locally downloaded source data to be stored under:

```text
data/
└── raw/
```

Raw and processed dataset files are ignored by Git and should not be committed to the repository.

The dataset is deliberately kept separate from the source code so that this repository does not redistribute the DigiTech Smart House Data Pack.

## Current usage

The API is still being developed, so expect it to change as the project grows.

The first implemented source loader handles WeatherLink exports:

```python
from smarthouse.data import load_weatherlink

data = load_weatherlink(
    "data/raw/path/to/weatherlink.csv"
)

print(data.head())
```

WeatherLink files contain several metadata rows before their tabular data and use source-specific formatting. The loader handles the basic file structure and validates that the supplied file looks like a supported WeatherLink export.

Cleaning and normalisation functionality will be developed separately so that each transformation remains easy to understand and test.

## Project structure

The package is organised into several areas:

```text
src/smarthouse/
├── data/
├── air_quality/
├── climate/
├── analysis/
├── visualisation/
└── research/
```

### `data`

Dataset catalogues, source-specific loaders, validation and data preparation.

### `air_quality`

Tools relating to particulate matter, indoor air quality and other air-quality measurements.

### `climate`

Weather, temperature, humidity and other environmental calculations.

### `analysis`

Reusable analytical and statistical utilities.

### `visualisation`

Reusable plotting and data-visualisation tools.

### `research`

Higher-level research workflows built from the toolkit's lower-level functionality.

Not every module contains functionality yet. The structure gives contributors clear places to add new features.

## Why source-specific loaders?

One of the first things discovered while exploring the Data Pack was just how different the source systems can be.

For example, WeatherLink exports contain metadata before their tabular data, while Invisible Systems uses different schemas across different releases.

Instead of pretending every CSV follows the same format, the toolkit uses source-specific loaders:

```text
Raw Smart House data
        │
        ├── WeatherLink loader
        ├── GlazeAlarm loader
        ├── Invisible Systems loader
        ├── SDS loader
        └── ...
                 │
                 ▼
       Processing and validation
                 │
                 ▼
       Analysis and visualisation
```

This allows unusual behaviour to be handled explicitly and, importantly for research, tested.

## Roadmap

The project will grow incrementally rather than trying to support every possible analysis from the beginning.

Some areas we'd like to work on include:

* loaders for additional Smart House data sources;
* timestamp parsing and validation;
* missing-data detection;
* measurement and unit normalisation;
* resampling time-series observations;
* air-quality analysis;
* indoor/outdoor environmental comparisons;
* weather and climate utilities;
* reusable visualisations;
* research workflows and statistical tools;
* improved dataset metadata and coverage information;
* documentation and examples.

The roadmap will evolve as we learn more about the dataset and as contributors suggest new ideas.

## Contributing

**Contributions are very welcome!**

You don't need to build a huge new feature to contribute. Small and focused improvements are encouraged and are often easier to review and test.

Potential contributions include:

* implementing a loader for another sensor platform;
* adding a small environmental calculation;
* improving validation;
* writing tests;
* improving documentation;
* adding a useful visualisation;
* investigating an unusual part of the dataset;
* fixing bugs;
* suggesting new research functionality.

Take a look at the repository's GitHub Issues for tasks labelled **`good first issue`** or **`help wanted`**.

### Contributor workflow

If you'd like to contribute code, please **fork the repository first** rather than trying to push directly to the main repository.

The usual workflow is:

1. Fork the repository on GitHub.
2. Clone your fork to your computer.
3. Create a new branch for your change.
4. Make and test your changes.
5. Commit your changes.
6. Push the branch to your fork.
7. Open a pull request back to the main Smart House Research Toolkit repository.

After forking, clone **your fork** by replacing `YOUR-USERNAME` with your GitHub username:

```bash
git clone https://github.com/YOUR-USERNAME/smart-house-research-toolkit.git
cd smart-house-research-toolkit
```

### Set up your development environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it using the appropriate command for your system.

**Windows — Command Prompt:**

```cmd
.venv\Scripts\activate
```

**Windows — PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS and Linux:**

```bash
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
pip install -e ".[dev]"
```

### Create a branch

Create a branch for your contribution:

```bash
git checkout -b feature/my-feature
```

Use a short, descriptive branch name that reflects the work you're doing.

For example:

```bash
git checkout -b feature/glazealarm-loader
```

or:

```bash
git checkout -b fix/weatherlink-validation
```

### Make and test your changes

Make your changes on your branch and run the project's checks before committing:

```bash
pytest
```

Then:

```bash
ruff check src tests
```

### Commit and push

Once your changes are ready:

```bash
git add .
git commit -m "feat: describe your change"
git push -u origin feature/my-feature
```

You can then open a pull request on GitHub from your branch to the `main` branch of the original Smart House Research Toolkit repository.

Before getting started, please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full development setup, testing and contribution guidelines.

By participating in the project, contributors are also expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

If you're considering a larger change, opening an issue first is encouraged so we can discuss the approach before you spend time implementing it.

## Development

The development commands are the same across Windows, macOS and Linux once the virtual environment has been activated.

Run the test suite with:

```bash
pytest
```

Run the lint checks with:

```bash
ruff check src tests
```

Both checks are also run automatically through GitHub Actions when changes are submitted.

## Research and data considerations

This project works with real-world sensor data, so missing observations, changing sensor configurations and inconsistent formats should be expected rather than treated as exceptional.

Where possible, toolkit functionality should:

* preserve information about where data came from;
* avoid silently guessing when data is ambiguous;
* distinguish dataset releases from actual observation periods;
* make assumptions visible to researchers;
* produce reproducible results;
* clearly report limitations.

These principles are particularly important as higher-level research workflows are added.

## Licence

The source code for Smart House Research Toolkit is released under the **MIT License**. See [LICENSE](LICENSE) for details.

The DigiTech Smart House Data Pack is a separate work and is **not distributed with this repository**. It is currently published separately under the **CC BY-NC 4.0** licence.

Users and contributors are responsible for complying with the dataset's own licence when downloading, using or sharing the data.

## Acknowledgements

This project is built around data produced by the **DigiTech Smart House** and made available through the Smart House Data Pack.

Thanks to everyone who contributes code, documentation, testing and improvements to the toolkit.
