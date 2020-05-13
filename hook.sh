#!/usr/bin/env bash

env PYTHONPATH=. PYTHONUNBUFFERED=1 python3 philips_hue_hooks/hue_hooks.py "$@"