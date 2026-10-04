#!/usr/bin/env python3
"""Compatibility entry point for the current source-bound figure set.

The former indexed annual plot is superseded by actual-count manuscript panels.
Rebuild all four figures and their manifest together to avoid stale provenance.
"""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('84_covid_evidence_figures.py')), run_name='__main__')
