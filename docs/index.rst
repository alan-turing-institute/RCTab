Welcome to RCTab
----------------

RCTab is an open-source subscription management and reporting system for Microsoft Azure.
It gives users visibility of their subscriptions' spending via the web front-end and allows administrators to set hard budget limits using the CLI.
With RCTab, you can give users more control over resource creation without spending extra time monitoring costs.

Features
++++++++

* A CLI for administrative tasks.
* A web front-end for admins and end-users.
* Automated deployment with Pulumi.
* Single Sign On with Azure Active Directory.
* Email notifications.

Components
++++++++++

The complete system comprises:

* A web server (A.K.A. the "RCTab API").
* The CLI, which allows command line interaction with the web server.
* Three function apps, which run background jobs to interact with Azure:

  * Usage: Gets usage data from Azure and posts to this API.
  * Status: Gets information about subscriptions from Azure, such as state and RBAC and posts to this API.
  * Controller: Gets list of subscriptions and their desired state from the API and then enables or disables subscriptions on Azure.
* An `authentication library <https://github.com/alan-turing-institute/fastapimsal>`_, which handles authentication using Microsoft's MSAL library for FastAPI.
* Logging and alerts.

Contribute
++++++++++

We welcome contributions in the form of issues and pull requests. Please see our :doc:`contributing guidelines <content/contributing>` and :doc:`code of conduct <content/code_of_conduct>`.

Contact Us
++++++++++

If you need to get in touch with us, please open an issue on our `GitHub repo <https://github.com/alan-turing-institute/rctab>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents
   :glob:
   :hidden:

   content/*

.. toctree::
   :maxdepth: 2
   :caption: External Links
   :glob:
   :hidden:

   API docs <https://rctab-api.readthedocs.io/en/latest/>
   API repository <https://github.com/alan-turing-institute/rctab-api>
   Function Apps docs <https://rctab-functions.readthedocs.io/en/latest/>
   Function Apps repository <https://github.com/alan-turing-institute/rctab-functions>
   CLI docs <https://rctab-cli.readthedocs.io/en/latest/>
   CLI repository <https://github.com/alan-turing-institute/rctab-cli>
   Infrastructure docs <https://rctab-infrastructure.readthedocs.io/en/latest/>
   Infrastructure repository <https://github.com/alan-turing-institute/rctab-infrastructure>
