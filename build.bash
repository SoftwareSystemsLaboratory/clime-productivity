#!/bin/bash

rm -r dist
pip uninstall clime_productivity -y
python -m build
pip install dist/clime_*

echo
echo "Done building"
