#!/usr/bin/env bash

source ./flivenv/bin/activate

./flilib/manage.py runserver --insecure

deactivate
