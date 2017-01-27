# S3Explorer
## Intro
Simple Flask application to explore AWS S3 buckets.

This app uses official boto3 to communicate with S3 instances. 
Implemented features are:
- [x] Simple login with just auth keys.
- [x] List all bucket
- [x] View each bucket content
- [x] Create and delete buckets
- [x] Upload or remove files to/from buckets
- [ ] Rename buckets

Code is separated to main `apps` module whic sub includs the blueprints module frontpage which is responsible for entire views logic.
Since this application is very simple the logic is implemented in the views.
While this is a kind of sloppy implementation - it perfectly works for such simple app.

---
## Direcotories
* root project directory have a run.py file which starts development server and a config file which holds the configuration of the application.
* apps folder holds the entry point to application as `__init__`, submodules and static files
* static and templates folders are for static files (like `css` files) and jinja2 templates
* frontend folder hold all the views and logic of the application
* utils for third party modules that require initialization

A short guide to S3Explorer can be found [here](https://walldev.github.io/S3Explorer/)
A running instance can be found [here][http://88.99.85.182:5000]
