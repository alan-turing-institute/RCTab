Subscription Management
-----------------------

Using RCTab to manage subscriptions.

Intro
+++++

After completing the setup steps, you will have an RCTab system deployed to Azure.
This means that:

* The Usage and Status functions run on an schedule to collect information about subscriptions and post it to the web server.
* The Controller function will check hourly to see whether any subscriptions need to be turned off or on.
  Note that, by default, only subscriptions in the whitelist will be turned on or off.
  See `Rollout`_ for more details.
* The web server will email users about changes to their subscriptions.
* Admins can install the CLI to check or adjust subscriptions' budgets, expiration dates, etc.
* Admins and other users can log in to the front-end, which should have the URL of ``rctab-{ticker}-{orgname}@azurewebsites.net``.
  This is often the quickest way to check a subscription's balance and history of approvals.
* Admins can connect directly to the database (e.g. with `psql`) if they need more detail than the CLI or frontend provides.
  The database admin password can be found in a keyvault on Azure.

Rollout
+++++++

To enable a gradual rollout of the system, RCTab has a whitelist.
By default, RCTab will only enable/disable and send emails for subscriptions in the whitelist, which starts out empty.
Once you are happy that RCTab has deployed successfully, that it is collecting data, that you can log into the frontend and set `Approvals and Allocations`_ using the CLI, you can use Pulumi to either add subscriptions to the ``WHITELIST`` environment variable or roll out to all subscriptions by setting the ``IGNORE_WHITELIST`` environment variable.

Ignoring Subscriptions
======================

The whitelist is one way to get RCTab to ignore subscriptions.
Subscriptions that aren't on the whitelist will not be enabled/disabled and will not receive emails but their data will be collected.
There are two other ways to determine whether RCTab will ignore a subscription:

* A subscription can be marked as "persistent" with the CLI.
  "Persistent" subscriptions do receive emails but will not be disbaled.
* A subscription can be placed outside of the management group that RCTab has permissions over.
  In this case, RCTab will have no knowledge of the subscription, will not collect data, will not send emails and will not disable it.

Approvals and Allocations
+++++++++++++++++++++++++

RCTab will try to disable all subscriptions that it can see (i.e. that it is collecting data for with the Status and Usage functions) unless they have approvals.
To create an approval for a subscription, use the CLI.
To review approvals for a subscription, go to that subscription's detail page on the frontend.
An approval is like a grant in that it covers some amount of spending over some time period.
To make use of an approval, a subscription additionally needs an allocation (also created with the CLI).
An allocation determines how much of the approved amount is available to spend right now.
To extend an approval, you can make a £0 approval with a later end date.
To reduce the amount of an approval, you can make a negative allocation followed by a negative approval.

Subscription Lifecycle
++++++++++++++++++++++

The typical lifecycle of subscription managed by RCTab might be as follows:

#. An admin creates a subscription on Azure (e.g. via the portal or CLI).
   Note that RCTab does not create subscriptions, it only enables/disables them.
   The subscription is placed into the management group where the function apps have the requisite permissions.
#. The admin manually adds the subscription to RCTab with the CLI.
   If it isn't added manually, it will be picked up by the Status or Usage app.
#. An approval and an allocation are made for the subscription with the CLI.
#. When the subscription approaches its budget or expiration date, RCTab will send an email to users with role assignments.
#. Users of the subscription can request a budget increase or an extension from the admins.
#. If this is granted, the admin can extend the approval and/or make a new allocation with the CLI.
#. If the request is denied, the subscription will eventually be disabled by RCTab.
   Users will be notified by email.
   Azure will permanently delete the subscription after approximately 90 days.
#. The subscription can be re-activated before the 90 days are up.
#. If the subscription is not re-activated, RCTab will mark the the subscription as "abolished" and archive it.
