# dewfmount application can be used as a short method to mount E01 in Linux system. In version 1 it is designed to mount NTFS partitions. 

Requirements : 
---------------

Python3 – Application flow is designed with python 3.x

ewfmount – To mount E01 partitions

ewfinfo – To display details about E01 image

How to run:
---------------

You should have root privileges to execute this script. If have spaces in file/folder name, use double quotations.

sudo python3[space][source E01 image file name][space][destination mounting location]

Ex. sudo python3 /your/image/location.E01 /destination/folder/to/mount/

Ex. sudo python3 "/your/image/location with spaces/image.E01" /destination/folder/to/mount/
