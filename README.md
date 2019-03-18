[![Build Status](https://travis-ci.org/Ross-Alexandra/SENG-371-Project-2.svg?branch=master)](https://travis-ci.org/Ross-Alexandra/SENG-371-Project-2)
[![codecov](https://codecov.io/gh/Ross-Alexandra/SENG-371-Project-2/branch/master/graph/badge.svg)](https://codecov.io/gh/Ross-Alexandra/SENG-371-Project-2)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)



# SENG-371-Project-2
Live use case for BYOA cloud compute framework (ccf).

# Running the project
On your first run you may need to start a Docker daemon. This
can be done with
``` commandline
sudo dockerd
```

Once you have the Docker daemon, simply using
``` commandline
sudo docker-compose up
```

# Development Setup

## Devtools installation
First, a virtual environment should be created.
This can be done with
``` commandline
python -m virtualenv env
```

Once the virtualenv has installed and created itself,
activate it with

``` commandline
source env/bin/activate
```

Finally, once your environment has been activated,
simply run
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Devtools setup.
Thanks to the magic of pre-commit, most of this
has been automated. However, you must first run
``` commandline
pre-commit install
```

This will install and setup the pre-commit tool,
which will ensure the other tools are run when
you create a commit.

## Running the tests.
This project uses pytest as its test-runner. In order to run the tests,
you must run
``` commandline
pytest ccf
```
if you're in the root dir, or
``` commandline
pytest
```
if you're in the ccf directory.

## Docker setup
### Installation
To install the docker components of this project,
please run
``` commandline
sudo apt-get install docker.io
sudo apt-get install docker-compose
```

Once these have sucessfully been installed, you
have all of the docker components needed.

## Production Environment
Deployment is automatically handled by Travis-ci and Heroku. Due to the nature of this project up-time is *not* guaranteed as the server may be spun-down by the owner when it is not needed.
Should you need to see something in prod when it is down, please contact the owner of this github repository so that it can be turned back on. 
The prod website can be found [here](https://seng371p2.herokuapp.com)
