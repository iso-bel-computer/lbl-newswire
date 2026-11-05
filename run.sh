#!/bin/bash
# Activate virtual environment
export PYTHONPATH=/mnt/izzycloud/sharedTools:/mnt/izzycloud/Research/PolicyDashboard:$PYTHONPATH

source /mnt/izzycloud/Research/PolicyDashboard/venv/bin/activate

cd /mnt/izzycloud/Research/PolicyDashboard

python3 main.py

# Deactivate venv (optional)
deactivate
