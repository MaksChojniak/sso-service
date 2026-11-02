"""Project-level test suite."""

from pathlib import Path


def load_tests(loader, standard_tests, pattern):
	return loader.discover(start_dir=str(Path(__file__).parent), pattern=pattern)