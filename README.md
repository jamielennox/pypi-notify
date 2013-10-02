#PyPi Notify

PyPi Notify is a program that can check to see if a new version of a project has been published on PyPi.

PyPi publishes an RSS feed of the last 40 updates. Given how popular PyPi is, this means a package change is advertised by RSS for about 3 hours. If you don't have a reader up for that period then you will miss the update. PyPi Notify instead keeps a list of packages that you are interested in, and checks to see if a new version of the package has been published since the last time it was run. By putting this on a cron job you can never miss an update again.

#Alpha
PyPi notify is still very new, the information on this README is very likely out of date. Consult the code for certainty.

#Configuration

At the very least you need to set the [mail] to= parameter in the config file so that PyPi Notify knows who to send email to. Depending on how it has been installed you will probably need to update the templates directory as well.

#Usage

###Add a package to watch list

```
pypi-notify package-add requests
```

###Remove a package from watch list

```
pypi-notify package-remove requests
```

###List packages

```
pypi-notify package-list

+----------+---------+
|   Name   | Version |
+----------+---------+
| requests |  2.0.0  |
+----------+---------+
```
