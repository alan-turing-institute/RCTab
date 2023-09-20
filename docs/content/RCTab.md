# RCTab Docs

## Overview

RCTab is an Azure subscription management system. It is made up of

- The web server (in this repo).
- The [CLI](https://github.com/alan-turing-institute/rctab-cli), which allows command line interaction with this API and handles authentication.
- Three [Function Apps](https://github.com/alan-turing-institute/rctab-functions), which run background jobs to interact with Azure:
  - Billing: Gets usage data from Azure and posts to this API.
  - Status: Gets information about subscriptions from Azure, such as state and RBAC and posts to this API.
  - Controller: Gets list of subscriptions and their desired state from the API and then enables or disables subscriptions on Azure.
- An [authentication library](https://github.com/alan-turing-institute/fastapimsal), which handles authentication using Microsoft's MSAL library for FastAPI.

In a typical setup:

- The web server and three function apps are deployed to Azure.
- End users can log in to the web server's frontend to check their subscriptions' balances.
- The Billing and Status function apps run on a schedule to collect information about subscriptions and post it to the web server.
- The Controller function app will run on a schedule to check which subscriptions need to be turned off or turned on for.
- The CLI can be installed by admins on their local machines to check or adjust subscriptions' budgets.
- Admins can also connect directly to the database (e.g. with `psql`) if they need more detail than the CLI or frontend provides.
- The web server will email users about changes to their subscriptions.

## Minimal Setup

The simplest setup would comprise the web server, database and one or more function apps running on your local machine.
The steps to set this up are:

1. Clone this repo and follow the development instructions in the [./README.md](./README.md) to set up a database & web server and to register an application with Active Directory.
2. Clone the Function Apps [repo](https://github.com/alan-turing-institute/rctab-functions) and follow the installation instructions in that README too.
  Note that the function apps rely on several environment variables to be able to communicate with the web server.
  In particular, they need to be given the hostname and port of the web server and each function app needs the private half of a key pair (the public halves are set as environment variables on the web server).
3. As per their documentation, each of the function apps requires a different set of permissions to function correctly.
  Once you have the right role assignments, you should log in to Azure with Visual Studio or the Azure CLI so that the function apps can authenticate as you.
4. With the web server listening, you can run the Status and/or Billing function apps to populate the database.
5. With data in your database, you can do any of the following:
   - View it via the web server frontend
   - Approve some budget for your subscription to spend with the RCTab CLI
   - Disable and enable subscriptions by running the Controller function app
