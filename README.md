# Assistant

## About

This project contains a customizable personal assistant program, mostly written in Python, designed with the Unix philosophy in mind. Its design is modular for replacements and upgrades using custom components, and it is meant to be fitted to an individual rather than a generic assistant for everybody. 

## Features & Goals 

Primary features of this are that it is designed to work offline without registration with any services, can be networked with other instances of the assistant, designed for each mobile, desktop, and server useage, and to be customized on device.

Please read the project Wiki for more information for how it works. It can be found at https://gitlab.com/Hikari_Tadashi/assistant/-/wikis/home


Normal Setup:
git clone https://gitlab.com/Hikari_Tadashi/assistant.git
install poetry (I.E. ```pacman -S python-poetry```)
cd assistant
## Setup our poetry env
poetry install
## replace service config file vars with yours and place it in your user services die
sed "s,{ASST_BASE_PLACEHOLDER},$(pwd)/assistant/g" assistant/assistant.service >> ${HOME}/.config/systemd/user/assistant.service
## setup service to be ran with systemd as a user service
systemctl --user enable assistant
## Start the service
systemctl --user start assistant
