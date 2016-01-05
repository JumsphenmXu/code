########################
Author: Xinhui
Email: xuxh13@163.com
########################

*Project structrue
	|--H2               	# the project directory
	   |--client        	# client
	   |  |--client.py  	# client.py
	   |  |--__init__.py
	   |--conf          	# project configurations
	   |  |--conf.py    	# configuration module
	   |  |--__init__.py
	   |--db            	# for data storage
	   |  |--db.pkl     	# data file
	   |--doc           	# project documentation
	   |  |--README.txt
	   |--model         	# data model User, Group(left unused)
	   |  |--model.py   	# data module
	   |  |--__init__.py
	   |--server        	# server
	   |  |--server.py
	   |  |--cache.py   	# cache which used to buffer the messages for each clients
	   |  |--__init__.py
	   |--__init__.py


*System design specifications
	1. Folder [client] contains client.py which is used to start the client part
	2. Folder [conf] specify the configuration details for the system
	3. Folder [db] contains the system's storage file
	4. Folder [doc] is where this file located
	5. Folder [model] defines the data model in the system
	6. Folder [server] defines the server part of this system 


*System usage
	STEP 1. Start the server [python server.py]
	STEP 2. Start the client [python client.py]
	STEP 3. Print the help information [help]
	STEP 4. Register an account [register]
	STEP 5. Sign in the system [login]
	STEP 6. Send message to users [chat]
	STEP 7. Leave the system [logout]
	STEP 8. Exit the platform [exit]

	PS: The system have 4 test users whose accounts are list as following:
	User 1: (username = netease1, password = 123)
	User 2: (username = netease2, password = 123)
	User 3: (username = netease3, password = 123)
	User 4: (username = netease4, password = 123)