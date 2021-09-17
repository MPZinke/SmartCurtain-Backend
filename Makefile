

all:
	# Error display setup
	touch ./Installation/InstallErrors.log

	# Pi setup
	sudo apt-get update
	sudo apt-get upgrade -y

	# DB setup
	sudo apt-get install mariadb-server -y || echo "Failed to install mariadb-server with command: sudo apt-get install mariadb-server -y" > ./Installation/InstallErrors.log
	sudo mariadb -uroot -praspberry < DB/Schema.sql || echo "Failed to setup DB with command: sudo mariadb -uroot -praspberry < DB/Schema.sql" > ./Installation/InstallErrors.log
	sudo mariadb -uroot -praspberry < DB/User_Simple.sql || echo "Failed to setup DB user with command: sudo mariadb -uroot -praspberry < DB/Users_Simple.sql" > ./Installation/InstallErrors.log

	# Local folder setup
	sudo mkdir /usr/SmartCurtain || echo "Failed to make directory /usr/SmartCurtain" > ./Installation/InstallErrors.log
	sudo cp -R ./Python/* /usr/SmartCurtain/ || echo "Failed to copy into directory /usr/SmartCurtain/ with command: sudo cp -R ./Python/* /usr/SmartCurtain/" > ./Installation/InstallErrors.log

	# Python setup
	sudo apt-get install python3-pip -y || echo "Failed to install python3-pip with command: sudo apt-get install python3-pip -y" > ./Installation/InstallErrors.log
	pip3 install adafruit-io || echo "Failed to install adafruit-io with command: pip3 install adafruit-io" > ./Installation/InstallErrors.log
	pip3 install astral==1.10.1 || echo "Failed to install astral with command: pip3 install astral" > ./Installation/InstallErrors.log
	sudo pip3 install flask || echo "Failed to install flask with command: pip3 install flask" > ./Installation/InstallErrors.log
	sudo pip3 install mysql-connector || echo "Failed to install mysql-connector with command: pip3 install mysql-connector" > ./Installation/InstallErrors.log
	pip3 install numpy || echo "Failed to install numpy with command: pip3 install numpy" > ./Installation/InstallErrors.log
	pip3 install RPi.GPIO || echo "Failed to install RPi.GPIO with command: pip3 install RPi.GPIO" > ./Installation/InstallErrors.log
	pip3 install setuptool || echo "Failed to install setuptool with command: pip3 install setuptool" > ./Installation/InstallErrors.log
	pip3 install sklearn || echo "Failed to install sklearn with command: pip3 install sklearn" > ./Installation/InstallErrors.log

	# Service setup
	sudo cp ./Installation/SmartCurtain.service /etc/systemd/system/ || echo "Failed to copy SmartCurtain service with command: sudo cp ./Installation/SmartCurtain.service /etc/systemd/system/" > ./Installation/InstallErrors.log
	sudo systemctl enable SmartCurtain.service || echo "Failed to enable service SmartCurtain.service with command: sudo systemctl enable SmartCurtain.service" > ./Installation/InstallErrors.log

	# Clean up (setdown?)
	echo "Finished"
	cat ./Installation/InstallErrors.log
	rm ./Installation/InstallErrors.log
