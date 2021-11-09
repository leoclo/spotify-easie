# easie-spotify

---

# Introduction
The ``spotify-easie`` is project to serve as an example of how to use [api_easiedata](https://github.com/easiedata/api_easiedata) to create custom databases using data retrieved from spotify on [easiedata](https://www.easiedata.com/login).
It creates 3 tables in easiedata with the objective of generating track recommendations.

## Pre-requisites

### Register User at easiedata

To register as an user in easiedata contact one of the contributors of this repository

### Create a developer application Spotify Developer

To create an spotify application follow this tutorial [spotify-quick-start](https://developer.spotify.com/documentation/web-api/quick-start/)
All you need for this project is Client ID and Client Secret


##  Local Installation
---

Clone the repository or download the .zip file and extract it on the desired directory

Create a virtual environment with the commands

```bash
python -m venv venv
```

Activate the created enviroment

```bash
source venv/bin/activate
```

Install the requirements for the project

```bash
pip install -r requirements.txt
```


## Testing
---
With the activated enviroment set the variables on settings.json file and run the following command

```bash
python tests/test_easie.py settings.json
python tests/test_spotify.py settings.json
```

## Usage
---

Fill the information on the settings.json file on the root directory of this project and run all core functionalities:

```bash
python easiesync settings.json build_all
```
