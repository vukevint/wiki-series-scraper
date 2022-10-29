#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 20:08:46 2021

Basic definitions and variables used throughout project

@author: kevinvu
"""
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


ROOT_PATH = get_project_root()
root_path = str(ROOT_PATH)
LOG_PATH = ROOT_PATH.joinpath('docs/log')
log_path = str(LOG_PATH)
SCRAPED_PATH = ROOT_PATH.joinpath('data/scraped')
scraped_path = str(SCRAPED_PATH)