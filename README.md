Simplistic blogging tool using Django on App Engine.

# Features

* Google Account authentication
* Multi-user (anyone with a Google Account can log in and create a post)
* Tagging
* Draft posts
* Markdown support
* Public comments with Disqus
* Search functionality

# Running

For local development:

	./install_deps
	./manage.py runserver

Deploying to Google App Engine:

	./install_deps
	appcfg.py update ./

# Live version

A live version of this blog running on Google App Engine can be found at [jkal-blog.appspot.com](https://jkal-blog.appspot.com).