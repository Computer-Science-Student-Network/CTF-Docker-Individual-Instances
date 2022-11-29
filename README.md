# CTF-Docker-Individual-Instances
This will eventually be a python flask server to automatically create seprate docker containers for CTF challenges
## Setup
install the following packages: `pip install docker`

## Usage
Modify `config.json` to what is appropriate. Also modify `image_map.json` to align with the format `"alias": "container_name"`

Set up a cron job to visit example.com/clean as often as you want to purge old images

Deploy