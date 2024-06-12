#!/bin/bash

# RFCOMM port to disconnect from
RFCOMM_PORT="/dev/rfcomm0"

sudo rfcomm release $RFCOMM_PORT

if [ $? -eq 0 ]; then
    echo "Successfully disconnected $RFCOMM_PORT"
else
    echo "Failed to disconnect $RFCOMM_PORT"
fi