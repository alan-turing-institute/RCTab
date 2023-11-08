---
title: 'RCTab: An Azure subscription management system'
tags:
  - Python
  - Cloud Computing
  - Microsoft Azure
  - Infrastructure as Code
authors:
  - name: Iain Stenson
    orcid: 0000-0001-7848-4154
    affiliation: 1
  - name: Tomas Lazauskas
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Oscar Giles
    orcid: 0000-0000-0000-0000
  - name: Joseph Palmer
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Pamela Wochner
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Eseoghene Ben-Iwhiwhu
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: The Research Computing Team
    orcid: 0000-0000-0000-0000
    affiliation: 1
    corresponding: true
affiliations:
  - name: The Alan Turing Institute, United Kingdom
    index: 1
date: 13 October 2023
bibliography: paper.bib
---
## Summary

Commercial cloud services provide users with the benefits of access to advanced computing services as well as various services like web hosting, machine learning, and data analytics. However, they can also present challenges for organizations that require a degree of predictability and stability in their cost planning, as the cost control mechanisms are not always designed to accommodate the management of a large number of projects and users with different budgetary requirements.

In response, we have developed [RCTab](https://rctab.readthedocs.io/) (**R**esearch **C**omputing **Tab**les), an open-source system for automating the management of [subscriptions](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-setup-guide/organize-resources#management-levels-and-hierarchy) on Azure, Microsoft’s cloud computing platform. It not only automates mundane management tasks, but also provides a framework for monitoring usage and reporting on costs, thus saving people's time and reducing the risk of excessive spending.

RCTab is designed to be flexible and extensible and can be easily adapted to the needs of different organisations. It is written in Python and has Infrastructure as Code (IaC) deployment that can be used to quickly and repeatably deploy it to Azure.

## Statement of Need

Commercial cloud services, such as Amazon Web Services, Microsoft Azure, Google Cloud Platform, and others, offer users flexible and scalable computing and storage resources, in addition to a variety of services and unique solutions. Due to their flexibility and convenient on-demand access to these resources, commercial cloud services are increasingly becoming the preferred platform for both academic and commercial users. They are especially suited for handling heterogeneous workloads, enabling cloud bursting, or even serving as components of a hybrid cloud solution where the cloud complements on-premises resources.

On-demand access can present challenges for organisations that require a degree of predictability and stability in their cost planning. This is because the cost of cloud services can vary from month to month, and some providers do not offer convenient ways to set hard limits on the amount of money that can be spent or the duration until which the allocated budget is valid. This is especially true for organisations with a large number of users, such as research institutes, and can lead to significant unexpected costs, if the service is not monitored closely. To address this, organisations typically either limit the number of users accessing resources and the type of resources they can access, or employ dedicated staff to monitor resource usage and costs. Neither approach is ideal: the former can restrict the cloud's potential, while the latter can be time-consuming and prone to errors.


In particular, Microsoft Azure, which is the focus of this work, offers various tools for managing costs, such as [budgets](https://docs.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets), [cost alerts](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending), and [cost analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis). While these tools are designed for individual subscriptions, they do not scale effectively for organisations with a large number of subscriptions. Moreover, they do not offer a mechanism to impose strict limits on spending or specify the duration for which a budget is valid.

Our response to addresing this challenge on Azure is the development of [RCTab](https://rctab.readthedocs.io/), an open-source system for automating the management of subscriptions on Azure.

## Source Code

The source code for RCTab is contained in five repositories:

- the [CLI](https://github.com/alan-turing-institute/rctab-cli) repo contains a Pip-installable Python package.
- the [Infrastructure](https://github.com/alan-turing-institute/rctab-infrastructure) repo contains code for automated deployment with Pulumi.
- the [API](https://github.com/alan-turing-institute/rctab-api) repo has code for the webserver, which is pushed [to DockerHub](https://hub.docker.com/r/turingrc/rctab-api) each time there is a new release.
- the Functions repo contains three Azure function apps, which are also pushed to DockerHub ([usage](https://hub.docker.com/r/turingrc/rctab-usage), [status](https://hub.docker.com/r/turingrc/rctab-status) and [controller](https://hub.docker.com/r/turingrc/rctab-controller)) each release.
- the [eponymous repo](https://github.com/alan-turing-institute/rctab) houses the general documentation (the other repos also have sites for component-specific documentation).

Detailed instructions on how to deploy RCTab to Azure with Pulumi can be found in the docs for the Infrastructure repository.

## Operation

Once deployed to Azure, an instance of RCTab will comprise:

- A FastAPI web server, which uses the API Docker image. This allows users to view budgets, RBAC assignments and the state of subscriptions.
- Three function apps, running their respective Docker images, that collect data and enable/disable subscriptions.
- A PostgreSQL database.
- Logging and alerts.

![System diagram.\label{fig:Figure 1}](figure1.png)

Users can use the web frontend to see their subscriptions' spending while administrators can use the CLI to create and edit budgets. RCTab integrates with Microsoft Entra ID (previously "Azure Active Directory") to provide "Single Sign On" authentication for both users and administrators.

The Usage and Status functions run on an schedule to collect information about subscriptions and post it to the web server.

The Controller function will check hourly to see whether any subscriptions need to be turned off or on.

The web server will email users about changes to their subscriptions.

## Lifecycle of a Subscription

As mentioned previously, a simple method for organising an Azure tenant is to create one subscription per project (or per-group or per-department, etc). Role-based Access Control (RBAC) can be used to grant permissions to researchers at the subscription level, allowing them to create, modify and delete resource groups and resources within that subscription.

Once a subscription has been created, it will need to be placed into a management group so that RCTab can monitor it. RCTab will have been given control over a management group during setup.

Using the CLI, an administrator must add an "approval" for the subscription to RCTab that specifies the amount and duration of the budget for the subscription.

When the subscription approaches its budget or expiration date, RCTab will send an email to users with role assignments to give them a chance to request a budget increase or an extension.

If this is granted, the admin can extend the approval with the CLI.

If the request is denied, the subscription will eventually be disabled by RCTab and, again, users will be notified by email. Azure will permanently delete the subscription after approximately 90 days, though the subscription can be re-activated up until the point that they are deleted.

## Acknowledgements

- This work was supported in part through computational resources provided by The Alan Turing Institute under EPSRC grant EP/N510129/1 and with the help of a generous gift from Microsoft Corporation.
- We acknowledge contributions by Oscar Giles, Markus Hauru, Jim Madge and Federico Nanni.
