#!/bin/bash

if [ "$#" -ne 2 ]
    then 
    echo -e "Please specify /dev/<your-device-here> and folder mount point to new device\n";
    exit 1;
else
    echo -e "Starting demo.. \n";
    echo -e "Creating file called tester.txt for.. testing\n";
    touch $2/test.txt
    ls -la
    echo -e "\nWriting 'I hate kernel stuff' to specified file!\n";
    echo -e "I hate kernel stuff" > $2/test.txt
    echo -e "Let's see what's in there..\n";
    cat $2/test.txt
    echo -e "\n... Interesting... \n";
    echo -e "Let's search for it with grep \n";
    grep -a "I hate kernel stuff"; 
    echo -e "\nNothing should have been displayed since its all encrypted!\n";
    echo -e "Double proof, look at what happens when there is a cat on the device \n";
    cat $1
    echo -e "\nNow let's try to look at the actual mount path file system with cat\n";
    cat $2/test.txt
    echo -e "\nThat SHOULD be better\n";
    echo -e "Removing files..\n";
    rm $2/test.txt
    echo -e "Files removed!, I'm done! Bye bye \n";
    exit 0;
fi
	
