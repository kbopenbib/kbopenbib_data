# KBOpenBib Data

## Overview

This repository contains scripts, examples and instructions for working with the KBOpenBib data snapshot.

## Examples

- [`Working with the KBOpenBib snapshot`](examples/working_with_kbopenbib_data.md)
- [`Working with PostgreSQL`](examples/working_with_postgresql.md)
- [`Working with BigQuery`](examples/working_with_bigquery.md)

## How to export a snapshot

```python
from scripts.export_files import OpenBibDataRelease

openbib_snapshot = OpenBibDataRelease(
    export_directory='openbib_export',
    export_file_name='kbopenbib_release',
    host='host',
    database='database',
    port='port',
    user='user',
    password='password'
)

openbib_snapshot.make_archive(export_format='csv')
```



