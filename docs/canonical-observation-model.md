# Canonical Observation Data Model

## Purpose

The DigiTech Smart House Data Pack contains environmental and IoT data from several source systems. These sources use different schemas, column names, timestamp formats and measurement structures.

Smart House Research Toolkit therefore needs a consistent representation for observations once source-specific data has been normalised.

This document defines that target representation. It does not define a complete normalisation implementation. Source-specific loaders should continue to preserve the raw data they load. Future normalisation utilities can convert supported observations into this canonical structure.

## Canonical observation schema

A normalised observation should use the following fields:

| Field         | Type                               | Required | Description                                                                                          |
| ------------- | ---------------------------------- | -------- | ---------------------------------------------------------------------------------------------------- |
| `timestamp`   | pandas datetime-compatible value   | Yes      | The actual time at which the observation was recorded.                                               |
| `source`      | string                             | Yes      | The source system that produced the observation.                                                     |
| `location`    | string or missing                  | No       | The physical or logical location associated with the observation, when known.                        |
| `sensor`      | string or missing                  | No       | The sensor, device or source-provided sensor identifier associated with the observation, when known. |
| `measurement` | string                             | Yes      | The type of quantity being observed, such as temperature, humidity or PM2.5.                         |
| `value`       | numeric or source-compatible value | Yes      | The observed measurement value.                                                                      |
| `unit`        | string or missing                  | No       | The unit associated with the measurement, when known.                                                |

The canonical structure is intended to represent one measurement per row.

For example:

```text
timestamp            source        location   sensor     measurement   value   unit
2025-01-01 12:00     weatherlink   outdoor    sensor_1   temperature   8.4     °C
2025-01-01 12:00     weatherlink   outdoor    sensor_1   humidity      81.0    %
```

These values are synthetic examples and are not copied from the DigiTech Smart House Data Pack.

## Field definitions

### `timestamp`

`timestamp` represents the actual observation time recorded by the source system.

It must not be inferred from the dataset release year, directory name or filename when the source data does not provide sufficient timestamp information.

Where timestamp information can be parsed reliably, the canonical value should use a pandas-compatible datetime representation.

### `source`

`source` identifies the source system from which the observation originated.

Examples may include:

```text
weatherlink
invisible_systems
air_quality
glaze_alarm
sds
moisture_sensors
air_source_heat_pump
```

Canonical source names may be used by the toolkit, but normalisation should not remove the ability to trace an observation back to its original source.

### `location`

`location` describes where the observation was recorded when this information is known.

If the source does not provide enough information to determine the location reliably, the value should remain missing rather than being inferred.

### `sensor`

`sensor` identifies the sensor, device or source-provided sensor label associated with the observation.

Not every source provides an explicit sensor identifier. If no reliable sensor identifier exists, this field should remain missing.

### `measurement`

`measurement` describes the quantity represented by the observation.

Examples include:

```text
temperature
humidity
pm2_5
pm10
co2
voc
```

Future normalisation work may define canonical measurement names, but names should only be changed where the mapping from the source measurement is understood.

### `value`

`value` contains the observed measurement value.

Where appropriate and safely supported by the source data, measurement values may eventually be represented numerically. Normalisation should not invent values or silently reinterpret ambiguous source content.

### `unit`

`unit` contains the measurement unit when it is known.

Examples might include:

```text
°C
%
µg/m³
ppm
```

If the dataset does not provide a reliable unit, the unit should remain missing.
Units should not be guessed from a measurement name alone.

## Required and optional fields

The minimum canonical observation requires:

```text
timestamp
source
measurement
value
```

The following fields are optional because they may not be available for every source:

```text
location
sensor
unit
```

Missing optional metadata should be represented explicitly as missing rather than replaced with invented values.

## Raw data and normalised data

Source-specific loaders are responsible for safely reading data from the DigiTech Smart House Data Pack.

They should preserve the structure and values provided by the source wherever possible.Normalisation is a separate step. For example, a raw source might contain measurements in separate columns:

```text
Timestamp (UTC) | PM2.5 | PM10 | Temperature | Humidity
```

A future normalisation process could represent these as separate canonical observations:

```text
timestamp | source | location | sensor | measurement | value | unit
```

Keeping loading and normalisation separate makes transformations easier to understand, test and reproduce.

## Provenance

Normalisation must not make it impossible to determine where an observation originated.

At minimum, the `source` field should identify the originating source system.

Where additional provenance is required, future implementations may retain metadata such as:

* dataset release;
* original filename;
* original column name;
* source-provided sensor name;
* source-provided system name.

These details should not be discarded merely because the observation has been converted into a common structure.

## Dataset release and observation time

The dataset release or folder year is not the same thing as the observation timestamp.For example, a directory associated with one release may contain observations extending into another calendar year.

The toolkit should therefore distinguish between:

```text
dataset release
```

and:

```text
actual observation timestamp
```

Temporal analysis should use timestamps contained in the observations rather than assuming that the release year describes the full date range of the data.

## Timezone handling

Timezone information should only be assigned when it is supported by the source.

For example, a field explicitly named:

```text
Timestamp (UTC)
```

provides timezone information that should be preserved during normalisation.

A timestamp without an explicit timezone must not automatically be assumed to be UTC.

Where timezone information is unavailable, the timestamp may remain timezone-naive until its interpretation can be established reliably.

## Unknown metadata

The canonical model must allow information to remain unknown.

If the location, sensor identity, measurement meaning or unit cannot be established from the dataset or supporting documentation, the toolkit should represent that information as missing.

It should not guess.

This is important for reproducibility because an explicit unknown value is preferable to metadata that appears authoritative but was inferred without evidence.

## Source schema examples

Different source systems represent observations in different ways.

For example:

### WeatherLink

```text
Date & Time
...
```

### Invisible Systems — earlier schema

```text
Sensor
DateTime
Value
Max
Min
Unit
```

### Invisible Systems — later schema

```text
Date
Time
System Name
Sensor Name
Value
Unit
```

### Air Quality

```text
Timestamp (UTC)
PM1
PM2.5
PM10
NOX
VOC
CO2
Temperature
Humidity
```

A canonical model allows later analysis functions to work with a consistent structure even when the original exports differ substantially.

## Conceptual hierarchy

The toolkit should treat the Smart House data conceptually as:

```text
Smart House Data Pack
└── Source system
    ├── Dataset release/folder
    ├── Actual date coverage
    ├── Location
    ├── Sensor
    ├── Measurements
    └── Missing periods
```

These concepts should remain distinct rather than being inferred from one another.

## Out of scope

This document defines the target representation only.

It does not implement:

* source normalisation;
* measurement-name mapping;
* unit conversion;
* timestamp parsing;
* timestamp resampling;
* missing-data handling;
* statistical analysis;
* visualisation.

Those behaviours should be implemented separately and tested independently.
