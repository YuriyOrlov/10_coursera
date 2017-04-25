# Coursera Dump

This script is very simple. It dumps XML list of coursera courses [here](https://www.coursera.org/sitemap~www~courses.xml) and creates a XLSX file.
It has information about course name, language, beginning date, course length in weeks and average course rating.

If you want to specify the place, where to save XLSX file please see next example.

```#!bash
$ python coursera.py /home/user/Documents/coursera.xlsx
File "/home/user/Documents/coursera.xlsx" created.

```

If you haven't specified XLSX file it will appear at the same folder.


```#!bash
$ python coursera.py
File "coursera_courses.xlsx" created.

```

Program uses multiproccessing, but time of coursera courses dump creation depends on your internet connection.
In my case it took about ~5 minutes to parse and create the XLSX file.


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
