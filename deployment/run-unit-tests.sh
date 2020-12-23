#!/bin/bash

template_dir="$PWD"
project_dir="$template_dir/../"

cd $project_dir
pipenv install --dev
python3 setup.py install
pipenv run pytest
