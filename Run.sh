#!/bin/bash

# Start the first process
/usr/local/bin/SmartCurtain/Backend/Backend.py &
  
# Start the second process
npm start --prefix /usr/local/bin/SmartCurtain/Frontend/ &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?