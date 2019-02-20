# Project Structure

The project consists of two directories: `threat` and `webapp`. The `threat` directory contains the MongoDB files, and the `webapp` contains the  files for the web application.

Once you have cloned the repository go to the web application directory
`cd webapp`
# Restoring Database

> Make sure you have the latest version of MongoDB installed on your computer.
> For more information for installation please follow the tutorials here: https://docs.mongodb.com/manual/installation/

 Once you have installed MongoDB correctly and you have an instance of mongo server running on the default port `27017` , restore the database by running the following command:

`mongorestore -d threat threat`

Now you should have a database called `threat` that contains a collection called `tweets`.

# Running Server
### Requirements

 - Python3
 - Installed dependencies for `webapp` by running:
	 -  `pip3 install -r requirements.txt`
### Run
To run the web application simply run
`python3 main.py`

This will run the web application on port 5000.



**Now follow InstructionsWebApp.pdf**
