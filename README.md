# BlueJeans Download Helper
 A small tool to simplify downloading your BlueJeans recordings.
 Since Verizon decided to sunset BlueJeans, many people might want to save their recordings. Navigating their website
 and downloading everything individually is quite cumbersome and requires lots of clicks.
 This tool does not actually download all the files automatically, but rather provides you with a JSON file containing
 download links for all your recordings. I thought that most people will not want to download all files and they might
 be quite large, so simply providing links seemed like an easier solution.
 
## Installation
Instructions for people who do not use Python or git regularly:
1. Open a terminal
1. Check you have python: `python3 --version` should output something
1. Check you have pip: `python3 -m pip --version` should output something
1. Using the green button with “<>” on github, select to “Download Zip” and unzip it
1. In your terminal, navigate to the downloaded and unzipped folder: `cd Downloads/bjdl` (assuming macOS, adapt as needed - you might be asked for permission to access the Downloads folder)
1. Execute `python3 -m venv .`
2. Execute `. ./bin/activate` - if you want to rerun the script later, you need to repeat this step
1. Execute `python3 -m pip install -r requirements.txt` - this installs one needed package
1. You should now be able to use the script: `python3 main.py`

## Known limitations
### Number of recordings
The script can currently only access 100 recordings; pagination is not implemented. If you believe that you hit this limit,
search in `main.py` for the line containing `{"pageSize": 100}` and change the value to something
larger. The BlueJeans API documentation does not state any upper bound for this value and I have no idea if it will work
with larger values.
### Shared content
If screen sharing was active, you can not see the meeting participants in the downloaded video. This seems to be a limitation imposed by BlueJeans.