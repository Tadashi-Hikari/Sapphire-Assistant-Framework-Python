# Python based *NIX Assistant

## About

This project contains a customizable personal assistant program, mostly written in Python, designed with the Unix philosophy in mind. Its design is modular for replacements and upgrades using custom components, and it is meant to be fitted to an individual rather than a generic assistant for everybody. 

## Features & Goals 

Primary features of this are that it is designed to work offline without registration with any services, can be networked with other instances of the assistant, designed for each mobile, desktop, and server useage, and to be customized on device.

Please read the project [Wiki](https://gitlab.com/Hikari_Tadashi/assistant/-/wikis/home) for more information for how it works.


## Normal Setup:
Following this setup guide will install the assistant, and create a system service that will start upon user login. To send messages to the assistant, use the udp-client.py with <code>python3 udp-client.py "your message here"</code>. It can also be useful to make an alias for this command, such as <code>alias msg=python3 /your/assistant/directory/udp-client.py</code> and put it in your .profile script

To start the setup, just follow the guide below

### Copy the git repository

<code>git clone https://gitlab.com/Hikari_Tadashi/assistant.git</code>

### Enter the assistant directory

<code>cd assistant</code>

### Install poetry 

This step varies depending on your package manager. For more information, go to [poetrys website](https://python-poetry.org/docs/#installation)

Example: <code>pacman -S python-poetry</code>

### Setup the poetry environment

<code>poetry install</code>

### Setup the Systemd service

<code>sed "s,{ASST_BASE_PLACEHOLDER},$(pwd)/assistant/g" assistant/assistant.service >> ${HOME}/.config/systemd/user/assistant.service</code>

### Enable the Systemd service

<code>systemctl --user enable assistant</code>

### Start the assistant

<code>systemctl --user start assistant</code>

Once all these steps are complete, the Assistant will run on user login
