# scripts

## validate_dataset.py

Checks a dataset against the shared schema in `docs/data-schema.md` before it is committed. It
verifies the required columns, the ISO date format, unique job identifiers, empty fields and
suspiciously short descriptions, and it scans every cell for personal data such as email addresses
and telephone numbers.

```bash
python scripts/validate_dataset.py work/task-2/nvidia-nayab-khalid/data/raw/nvidia_postings_raw_20260901.csv
```

It exits with a non-zero code if any check fails. The Data Quality Lead of the week runs it across
all four members' datasets.

Only the Python standard library is required.
