# CTF-Docker-Individual-Instances
This will eventually be a python flask server to automatically create seprate docker containers for CTF challenges

## Disclaimer

This software comes with absolutly no warranties. Do not use this in a less controlled enviroment. This was designed for in person competitions where students are not expected to attack the server. If you want to make this better, please give a pull request.

## Setup
install the following packages: `pip install docker`

## Usage
Modify `config.json` to what is appropriate. Also modify `image_map.json` to align with the format `"alias": "container_name"`

Set up a link to http://example.com/launch/ALIAS on each challenge

Set up a cron job to visit example.com/clean as often as you want to purge old images

Visit example.com/flush/SECRETKEY to remove all images it created

Monitor example.com/status/SECRETKEY to view how many are running

Deploy
