#!/bin/sh
DIR="database-prep/"
python3 sqldatabase.py -v -t utterances -cc "${DIR}utterance-csv"
python3 sqldatabase.py -v -t commands -cc "${DIR}commands-csv"
