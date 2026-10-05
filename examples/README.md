# File-handling lessons

These scripts preserve the project's learning progression: text and binary I/O, CSV/JSON, compressed files, file handles, paths, and basic success/error routing. They are demonstrations rather than components of the transaction pipeline.

Run from the repository root, for example `python examples/file_concepts.py`. Each script seeds a temporary working directory from `data`, performs its lesson, and removes generated data on exit. Imports are safe. `pytest_basics.py` is a separate pytest lesson; its duplicate function names were corrected so both exercises can be discovered.

`data/previous_runs` preserves earlier input/output examples for reference; these are not current pipeline expectations. Some old inputs have misspelled filenames, negative amounts, or unknown statuses. Use `../sample_data` for the current pipeline demonstration.
