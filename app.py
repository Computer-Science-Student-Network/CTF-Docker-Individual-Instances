

from flask import Flask, request
import subprocess
import os
import time
import json
import random
import docker
import requests
client = docker.from_env()

#read the json config file and interpraet it as a dictionary
with open('config.json') as json_file:
    config = json.load(json_file)
with open('image_map.json') as json_file:
    image_map = json.load(json_file)

with open('log.log', 'a') as f:
    f.write("Loaded Config: " + str(config) + '\nLoaded image map: ' + str(image_map) )

ports = []
running_images = []

panic_count = 0

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, if you are seeing this, you either went to the wrong page or the administrator messed up.\n please contact the administrator if you think this is a mistake. \n https://github.com/Computer-Science-Student-Network/CTF-Docker-Individual-Instances'

@app.route('/launch/<image>', methods=['GET'])
# run a bash command that uses token as the argument
def launch(image):
    #check to see if the image is in the image map
    if image not in image_map:
        #log the error
        with open('log.log', 'a') as f:
            f.write("Image missing from map: " + image )
        return "The spesified image is not in the map. Please report this to the administrator"
    #check to see if the image is in the docker image list
    try:
        client.images.get(image_map[image])
    except:
        #client.images.get(image_map['image'])
        #log the error
        with open('log.log', 'a') as f:
            f.write("Image missing from docker: " + image )
        return "The spesified image is not in the docker image list. Please report this to the administrator"
    #generate a random port for this instance
    port = random.randint(10000, 60000)
    #check to see if the port is already in use
    while port in ports:
        port = random.randint(10000, 60000)
    #add the port to the list of used ports
    ports.append(port)
    running_images.append('d-' + image + str(port))
    
    # run the docker run command to run a built image
    client.containers.run(image_map[image], detach=True, ports={'80':str(port)}, name='d-'+ image + str(port), remove=True)    
    # log the start of the image
    with open('log.log', 'a') as f:
        f.write("Started " + image + str(port) + "at time " + str(time.time()) )
    # wait for the container to start
    #time.sleep(30)
    #redirect to the new container
    #return "Redirecting to your new container", 302, {f'Location': f"http://{config['location']}:" + str(port)}
    return f"Your image will launch at http://{config['location']}:{str(port)}. Please be paitent as it will take a few minuites to start"
@app.route('/clean', methods=['GET'])
def clean():
    if len(running_images) > config['panic_threshold']:
        #log that a panic clean was run
        with open('log.log', 'a') as f:
            f.write("Panic clean at time " + str(time.time()) )
        requests.get(f"http://{config['location']}:{config['port']}/flush/{config['key']}")
        return "Panic clean ran"

    for i in running_images:
        #stop the container if it has been running for more than 30 minutes
        if time.time() - client.containers.get(i).attrs['State']['StartedAt'] > config['live_time']*60:
            client.containers.get(i).stop()
            # log the stop of the image
            with open('log.log', 'a') as f:
                f.write("Stopped " + i + "at time " + str(time.time()) )
            #remove the port from the list of used ports
            ports.remove(int(i[-5:]))
            running_images.remove(i)
        else:
            break

@app.route('/flush/<key>', methods=['GET'])
def flush(key):
    if key == config['key']:
        with open('log.log', 'a') as f:
            f.write("Flushed all containers at time " + str(time.time()) )
    
        for i in running_images.copy():
            client.containers.get(i).stop()
            # log the stop of the image
            with open('log.log', 'a') as f:
                f.write("Stopped " + i + "at time " + str(time.time()) )
            #remove the port from the list of used ports
            ports.remove(int(i[-5:]))
            running_images.remove(i)
        return "Flushed all running containers"
    else:
        return "Incorrect key"

@app.route('/status/<key>', methods=['GET'])
def status(key):
    if key == config['key']:
        return ( f" <html>  <body> <h1>status</h1> <h3>panic count</h3> {str(panic_count)} <h3>running images</h3> Running containers:  {str(running_images)} <h3>ports</h3> {str(ports)} </body> </html> ")
    else:
        return "Incorrect key"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config["port"])
