---
title: 'RCTab: An Azure Subscription Management System'
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

Commercial cloud services provide researchers with the benefits of flexible and scalable computing and storage resources. However, they can also present challenges for organizations that require a degree of predictability and stability in their cost planning, as the cost control mechanisms are not always designed to accommodate large numbers of projects and users with different budgetary requirements.

In response, we have developed [RCTab](https://rctab.readthedocs.io/) (**R**esearch **C**omputing **Tab**les), an open-source system for automating the management of [subscriptions](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-setup-guide/organize-resources#management-levels-and-hierarchy) on Azure, Microsoft’s cloud computing platform. It not only automates mundane management tasks, but also provides a framework for monitoring usage and reporting on costs, thus saving people's time and reducing the risk of excessive spending, and a rich source of data for usage forecasting.

RCTab is designed to be extensible, so can be easily adapted to the needs of different organisations. It is written in Python and has Infrastructure as Code (IaC) deployment for quick and reliable deployment to Azure.

## Statement of Need

Institutions are increasingly adopting cloud platforms, such as Amazon Web Services, Microsoft Azure and Google Cloud Platform, for both operational and research computing infrastructure. Cloud platforms are especially suited to heterogeneous or unpredictable workloads and can be employed as part of a hybrid solution, where the cloud complements on-premises resources.

However, on-demand access can present challenges for organisations that require a degree of certainty in their outgoings. This is because the cost of cloud services can vary by region and over time, and some providers do not offer convenient ways to set hard limits on a project's budget or duration. This is especially true for organisations with many technical users, such as research institutes, and can lead to significant unexpected costs if the service is not monitored closely. To address this, organisations typically either limit the number of users accessing resources and the type of resources they can access or employ dedicated staff to monitor resource usage and costs. Neither approach is ideal: the former can restrict the cloud's potential, while the latter can be time-consuming and prone to errors.

In particular, Microsoft Azure, which is the focus of this work, offers tools for managing costs, such as [budgets](https://docs.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets), [cost alerts](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending), and [cost analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis). These tools are designed for individual subscriptions, and they do not scale effectively for organisations with many subscriptions. Moreover, they do not offer a mechanism to impose strict limits on spending or specify the duration for which a budget is valid.

Our response to this challenge is development of [RCTab](https://rctab.readthedocs.io/), an open-source system for automating the management of subscriptions on Azure.

## Source Code

The source code for RCTab is contained in five repositories:

- the [CLI](https://github.com/alan-turing-institute/rctab-cli) repository contains the command-line interface (used for administrative tasks), which is a Pip-installable Python package.
- the [Infrastructure](https://github.com/alan-turing-institute/rctab-infrastructure) repository contains code for automated deployment with [Pulumi](https://www.pulumi.com/).
- the [API](https://github.com/alan-turing-institute/rctab-api) repository has code for the webserver, which is pushed [to DockerHub](https://hub.docker.com/r/turingrc/rctab-api) each time there is a new release.
- the [Functions](https://github.com/alan-turing-institute/rctab-functions) repository contains three Azure function apps, which are also pushed to DockerHub ([usage](https://hub.docker.com/r/turingrc/rctab-usage), [status](https://hub.docker.com/r/turingrc/rctab-status) and [controller](https://hub.docker.com/r/turingrc/rctab-controller)) each release.
- the [eponymous repository](https://github.com/alan-turing-institute/rctab) houses the general documentation (the other repositories also have sites for component-specific documentation).

Detailed instructions on how to deploy RCTab to Azure with Pulumi can be found in the docs for the Infrastructure repository.

## Operation

Once deployed to Azure, an instance of RCTab will comprise:

- A FastAPI web server, which uses the API Docker image. This allows users to view budgets, Role-Based Access Control (RBAC) assignments and the state of subscriptions.
- Three function apps, running their respective Docker images, that collect data and enable/disable subscriptions.
- A PostgreSQL database.
- Logging and alerts.

![System diagram.\label{fig:Figure 1}](figure1.png)

Users can use the web frontend to see subscriptions' spending and budget details, such as remaining amount, expiration date, the project to which spending will be charged and list of RBAC assignments.

Administrators can use the CLI to create and edit budgets, override budgets (for critical subscriptions that must never be turned off) and get JSON-format summaries.

RCTab integrates with Microsoft Entra ID (previously "Azure Active Directory") to provide "Single Sign On" authentication for the frontend and CLI.

The Usage and Status functions run on a schedule to collect information about subscriptions' recent spending and current state, respectively, and post it to the web server.

The Controller function will poll the web server to see whether any subscriptions need to be turned off or on.

The web server will email users about changes to their subscriptions and send daily email summaries.

## Lifecycle of a Subscription

A simple method for organising an Azure tenant is to create one subscription per project (or per-group or per-department, etc). RBAC assignments can be used to grant permissions to researchers at the subscription level, giving them the freedom to create, modify and delete resources within that subscription as their work requires.

Once a subscription has been created, it will need to be placed into a management group so that RCTab can monitor it. RCTab will have been given control over a management group during setup.

Using the CLI, an administrator can add an "approval" for the subscription to RCTab that specifies the amount and duration of the budget for the subscription.

When the subscription approaches its budget or expiration date, RCTab will email users with role assignments to give them a chance to request a budget increase or an extension.

If this is granted, the admin can extend the approval with the CLI. The approval has fields to link to the email or support request used to request the extension.

If the request is denied, the subscription will be disabled by RCTab and, again, users will be notified by email. Azure will permanently delete the subscription after approximately 90 days, though the subscription can be re-activated up until that point.

## Acknowledgements

- This work was supported in part through computational resources provided by The Alan Turing Institute under EPSRC grant EP/N510129/1 and with the help of a generous gift from Microsoft Corporation.
- We would like to acknowledge code and documentation contributions by Oscar Giles, Markus Hauru, Jim Madge and Federico Nanni.
