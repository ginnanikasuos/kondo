modprobe ftdi-sio
echo 165C 0008 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
chmod 666 /dev/ttyUSB0
