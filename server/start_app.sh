#!/bin/bash

export FLASK_APP=main.py
flask db init
flask db migrate
flask db upgrade
/usr/bin/python3 main.py