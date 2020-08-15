#!/usr/bin/python

import subprocess,re,os,sys

def display_information(souce,destination):

	print("\n -------------------- Image Information --------------------\n")

	# display ewf file information
	print(subprocess.getoutput('ewfinfo "'+souce+'"'))

	# get mmls output
	print(subprocess.getoutput('mmls -aB "'+souce+'"'))

	print("\n-------------------- Locations --------------------\n")

	print("Souce image : ",os.path.abspath(souce),"\n")

	print("Mount to : ",os.path.abspath(destination),"\n")

	print("ewfmount location : ",destination+"ewfmounting")

	print("\n-------------------- Commands --------------------\n")

def getting_slot_start_length(source,destination):
	#mmls command
	source='"'+source+'"'
	mmls_output = subprocess.getoutput("mmls -aB "+source)

	filter_output=[]

	for line in mmls_output.splitlines()[5:]:
	    chunks = re.split(' +', line)
	    #print(chunks)
	    slot=int(chunks[1])
	    start=int(chunks[2])
	    length=int(chunks[4])

	    mount_command(source,destination,slot,start,length)

def create_folder(location):
	if not os.path.exists(location):
	    os.mkdir(location)
	    

def ewfmounting(source,destination):
	create_folder(destination+"/ewfmounting")

	command='ewfmount "'+source+'"'+' "'+destination+'ewfmounting"'+" > /dev/null"
	print(command+"\n")
	os.system(command)

	# writing to unmount file
	write_to_file_reverser_order('/tmp/ewf_unmount.sh','umount "'+destination+'ewfmounting"')

def write_to_file_reverser_order(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)	


def mount_command(source,destination,slot,start,length):

	source='"'+source+'"'

	destination_folder=destination+"partition"+str(slot)

	create_folder(destination_folder)

	print("Creating folder at "+destination_folder+"\n")

	#mount -o ro,loop,show_sys_files,stream_interface=windows,offset=$((206848*512)) /mnt/ewf/ewf1 /mnt/windows_mount 

	command="mount -o ro,loop,show_sys_files,stream_interface=windows,offset=$(("+str(start*512)+')),sizelimit=$(('+str(length*512)+')) '+'"'+str(destination)+'ewfmounting/ewf1" "'+destination_folder+'"'
	print(command+"\n")
	os.system(command)

	# writing to unmount file
	write_to_file_reverser_order('/tmp/ewf_unmount.sh','umount "'+destination_folder+'"')


if len(sys.argv) != 3:
	print("""\ndewfmount application can be used as a short method to mount E01 in Linux system. In version 1 it is designed to mount NTFS partitions. 

Requirements : 
---------------

Python3 – Application flow is designed with python 3.x
ewfmount – To mount E01 partitions
ewfinfo – To display details about E01 image

How to run:
---------------

You should have root privileges to execute this script. If have space in file/folder name, use double quotations.

sudo python3[space]<source E01 image file name>[space]<destination mounting location>

Ex. sudo python3 /your/image/location.E01 /destination/folder/to/mount/

Ex. sudo python3 "/your/image/location with spaces/image.E01" /destination/folder/to/mount/

""")

else:

	print("\n\n EWF mount script by")

	print("""
 ____  ____  __    __  __  ___  _   _    __   
(  _ \(_  _)(  )  (  )( ) / __)( )_( )  /__\  
 )(_) )_)(_  )(__  )(__)( \__ \ ) _ (  /(__)\ 
(____/(____)(____)(______)(___/(_) (_)(__)(__)
""")

	source_ewf_img_file_path=sys.argv[1]

	mount_folder_location=sys.argv[2]


	#production testing part start
	# os.system('cls||clear')
	# os.system('chmod +x /tmp/ewf_unmount.sh')
	# os.system('sudo /tmp/ewf_unmount.sh')
	#production testing part end

	# create unmount script file
	f=open("/tmp/ewf_unmount.sh", 'w')
	f.close()


	display_information(source_ewf_img_file_path,mount_folder_location)

	ewfmounting(source_ewf_img_file_path,mount_folder_location)

	getting_slot_start_length(source_ewf_img_file_path,mount_folder_location)

	print ("\n-------------------- Done ! --------------------\n")

	print("Run the ewf_unmount.sh script located in /tmp directory to unmount all partitions.\n")
