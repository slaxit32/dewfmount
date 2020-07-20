#!/usr/bin/python

import subprocess,re,os,sys

def display_information(souce,destination):

	print("\nImage Information --------------------\n")

	print(subprocess.getoutput("mmls -aB "+souce))

	print("\nLocations --------------------\n")

	print("Souce image : ",souce,"\n")

	print("Mount to : ",destination,"\n")

	print("ewfmount location : ",destination+"/ewfmounting")

	print("\nCommands --------------------\n")

def getting_slot_start_length(source,destination):
	#mmls command
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
	# Create target Directory if don't exist
	#print(location)
	if not os.path.exists(location):
	    os.mkdir(location)
	    #print("Directory " , dirName ,  " Created ")
	# else:    
	#     print("Directory " , dirName ,  " already exists")	    

def ewfmounting(source,destination):
	create_folder(destination+"/ewfmounting")

	command="ewfmount "+source+" "+destination

	os.system(command)

	print(command)

	#os.system(command)

def mount_command(source,destination,slot,start,length):

	destination_folder=destination+"/p"+str(slot)
	create_folder(destination_folder)
	#print(destination_folder)


	command="a"+str(slot)+str(start)+str(length)+str(destination_folder)
	print(command)

if len(sys.argv) != 3:
	print("help")
else:
	source_ewf_img_file_path=sys.argv[1]
	mount_folder_location=sys.argv[2]

	display_information(source_ewf_img_file_path,mount_folder_location)

	ewfmounting(source_ewf_img_file_path,mount_folder_location)

	getting_slot_start_length(source_ewf_img_file_path,mount_folder_location)
