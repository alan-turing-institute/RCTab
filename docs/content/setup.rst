Setup
-----

Azure
+++++

RCTab can be deployed to Azure automatically with our Infrastructure repository.
There are some prerequisites, which are covered in the Infrastructure docs.
Once the deployment has finished, the API and Function Apps will pull their respective images from Docker Hub and immediately start collecting data.

Local
+++++

The simplest setup would comprise the web server, database and one or more function apps running on your local (Linux or MacOS) machine.
The steps to set this up are:

#. Clone the API repo and follow the development instructions in the API docs to set up a database & web server and to register an application with Active Directory.
#. Clone the CLI repo and install the CLI package into a virtual environment, as per the CLI docs.
#. Clone the Function Apps repo and follow the developer installation instructions in the Function Apps docs.
   Note that the function apps rely on several environment variables to be able to communicate with the web server.
   In particular, they need to be given the hostname and port of the web server and each function app needs the private half of a key pair (the public halves are set as environment variables on the web server).
#. As per their documentation, each of the function apps requires a different set of permissions to function correctly.
   When you run the function apps locally, they will try to obtain your credentials from several places, such as Visual Studio Code and the Azure CLI.
   Therefore, you will need to make sure that you have the correct Azure RBAC permissions and that you are logged in to Azure via Visual Studio or the Azure CLI before running the functions locally.
#. Once you are logged in and have the web server started, you can run the Status and Usage functions to collect data.
#. With data in your database, you can do any of the following:

   * View it via the web server frontend (typically on ``0.0.0.0:8000``).
   * Approve some budget for your subscription to spend with the RCTab CLI.
   * Disable and enable subscriptions by running the Controller function app.
