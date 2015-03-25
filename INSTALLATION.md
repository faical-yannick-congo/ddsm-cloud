## Section 0: Manual installation
    # MongoDB
    To install MongoDB
        $ conda install mongodb
        $ conda install pymongo
        $ pip install mongoengine
        $ pip install flask-mongoengine
        $ sudo mkdir -p /data/db/
        $ sudo chown `id -u` /data/db
        $ sudo mongod --rest

    # Other Requirements

        $ pip install flask
        $ pip install docopt
        $ pip install flask-api

## Section 1: Building docker containers
    After configuring docker based on your platform, do:
    $ git clone https://github.com/materialsinnovation/sumatra-cloud.git
    $ cd sumatra-cloud
    $ git checkout dockerized
    $ cd docker/mongodb
    $ docker build -t sumatra-db .
    $ docker run -d -p 27017:27017 -p 28017:28017 sumatra-db
    $ cd ../..
    $ docker build -t sumatra-cloud .
    $ docker run -i -t -p 5000:5000 sumatra-cloud

## Section 2: Pull from docker registry
    After configuring docker based on your platform, do:
    $ docker pull palingwende/sumatra-db
    $ docker run -d -p 27017:27017 -p 28017:28017 palingwende/sumatra-db
    $ docker pull palingwende/sumatra-db
    $ docker run -i -t -p 5000:5000 palingwende/sumatra-cloud

## Section 3: Going to the cloud service frontend
    # Figure out your docker ip.
        If you are on linux: the ip is 0.0.0.0
        If you are on osx: $ boot2docker ip
    Open the browser got to: http://ip_address:5000/
    You are on the sumatra-cloud frontend at this point.



## Docker installation
[Official installation source][https://docs.docker.com/installation/]
    # Tips
        On osx: 
        [boot2docker][https://github.com/boot2docker/osx-installer/releases/tag/v1.5.0]
        $ boot2docker init
        $ boot2docker start
        EXPORT the values being displayed.
        On linux:
        $ sudo apt-get update
        $ sudo apt-get install docker.io
        $ wget -q0- https://get.docker.com/ | sh