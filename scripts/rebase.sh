#! /usr/bin/env bash

set -e
set -x

# Places data from the database into the broker
python app/up_data_for_broker.py

# TODO: Remove data from broker, when that don't exist on database
