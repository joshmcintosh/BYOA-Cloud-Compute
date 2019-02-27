# SENG-371-Project-2
Live use case for BYOA cloud processing framework

# Docker setup

## Installation
To install the docker components of this project,
please run
``` commandline
sudo apt-get install docker.io
sudo apt-get install docker-compose
```

Once these have sucessfully been installed, you
have all of the docker components needed.

## Running the project
First you must start a Docker daemon. This
can be done with
``` commandline
sudo dockerd
```
Note, for anyone using Bash on Ubuntu on Windows
(WSL), please follow the instructions "Running
on Bash on Ubuntu on Windows (WSL)" to
get the docker daemon running.



## Running on Bash on Ubuntu on Windows (WSL)
In order to get the docker daemon running in WSL,
you need to first run the Bash terminal as an administrator
(on the Windows side, right-click Bash and click "run
as administrator".)

Next, in order to get the daemon running, you will need
a cgroup. To do this, first run
``` commandline
sudo apt-get install cgroup-lite
```
Once installed, whenever you want to run the daemon, you
first must run
``` commandline
cgroupfs-mount
sudo dockerd &
```

Once these commands have been run, you will have a docker
daemon running in the background of this shell.
