## ℹ️ Changes in mapp Framework 6

With Automation Studio 6, a couple of changes were introduced. During the mapp Framework migration to Automation Studio 6, we tried to keep as much functionality unchanged as possible. All changes to mapp components are described in the respective chapters. Here is only a short overview of frequently asked questions.

## Default login to mappView visualization

To show all features of the mapp Framework 6 visualization after import, a new AdminDefault user with admin rights was created and is used as a forced user. This configuration must be changed and adapted after import according to the application needs.

Default behavior and password are documented in the mapp Framework documentation: https://br-automation-community.github.io/mapp-Framework-6/userx/features/

![QnA1][def]

## User log in/log out audit events

Whenever any user logs out and logs in to mappView, four audit records are immediately generated. This change was introduced with mapp View 6.0.0, where interface authentication was switched to OPC UA .

https://help.br-automation.com/#/en/6/visualization/mappview/common/versioninformation/6.1/otherchanges.html

![QnA2][def2]


## Audit Configuration does not take effect

The Save button is used for storing the configuration, not for exporting itself. Unfortunately, in mapp Services 6.5 there is a bug where automatic export happens at midnight regardless of the time set in the configuration. This will be fixed in one of the next mapp Services versions.

![QnA3][def3]

## VC4 cannot be imported

With migration to AS6, a decision was made to remove VC4, which is obsolete, from mapp Framework 6. Only mappView visualization is supported.

## AS Help does not contain documentation of mapp Framework 6

A decision was made to no longer maintain offline AS Help. mapp Framework 6 documentation is available online and is automatically updated with each new feature commit. Only the English version of the documentation is maintained. Automatic browser translation (German, Chinese, etc.) can be used for documentation localization.

[def]: images/QnA1.png
[def2]: images/QnA2.png
[def3]: images/QnA3.png