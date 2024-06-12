#!/bin/bash

ESP32_MAC_ADDR="C8:C9:A3:FB:0A:16"
RFCOMM_PORT="/dev/rfcomm0"

sudo rfcomm connect hci0 $ESP32_MAC_ADDR &

# Wait for a while to allow the device to be created
sleep 2

# Set permissions on the rfcomm device
if [ -e $RFCOMM_PORT ]; then
    sudo chmod 666 $RFCOMM_PORT
    echo "Permissions set to 666 on $RFCOMM_PORT"
else
    echo "Failed to create $RFCOMM_PORT"
fi 


