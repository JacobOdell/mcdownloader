# What do

Downloads mc mods given a list of MC mod links

# Requirements
python
[GeckoDriver](https://github.com/mozilla/geckodriver/releases) (put in same path as script or add to PATH)

# Set up

1. `python -m venv venv`
2. `source venv/bin/activate` for linux or `venv\Scripts\activate` for windows
3. `pip install -r requirements.txt`

# How use

1. Edit MOD_LINKS with your mods
2. Edit MINECRAFT_VERSION with your desired version
3. Edit MODLOADER with your desired modloader
4. `python download.py`

# Known bugs

Does not search past first page of mods for the mods... will fix later idk