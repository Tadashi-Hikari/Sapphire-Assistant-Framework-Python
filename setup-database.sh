#!/bin/sh
DIR="prep-csv/"
python3 sqldatabase.py -v -t number -cc "${DIR}number-csv"
python3 sqldatabase.py -v -t timedate_keys -cc "${DIR}timedate-keys-csv"
python3 sqldatabase.py -v -t metadata -cc "${DIR}metadata-csv"
python3 sqldatabase.py -v -t utterances -cc "${DIR}utterance-csv"
python3 sqldatabase.py -v -t time_keys -cc "${DIR}time-key-csv"
python3 sqldatabase.py -v -t commands -cc "${DIR}commands-csv"
python3 sqldatabase.py -v -t command_variables -cc "${DIR}command-variable-csv"



