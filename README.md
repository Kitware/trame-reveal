# trame-revealjs

This is a Python package designed to help integrate trame applications into reveal.js slides.

## Guide

To embed one or multiple trame applications into a reveal.js set of slides:

1) Create a HTML file, with reveal.js syntax, for your slides

2) To embed a trame application in a slide use the syntax

        <trame-embedded-app app-id="app1"></trame-embedded-app>

    `app-1` is an ID for your trame application. If you create another `<trame-embedded-app>` with the same ID, it will use the same application

3) Create a Python file where you instantiate a SlidesApp, it takes up to 5 arguments:

    1) slides_path: The relative path to the HTML file containing the slides

    2) server: An optionnal trame Server instance

    3) port: a port (defaults to 8080) on which to deploy the application running the slides

    4) iframe_port_start: the port from which will start the deployment of the embedded applications. If you have N applications, the ports from iframe_port_start to iframe_port_start + N - 1 will be used

    5) trame_apps: a dictionary associating the trame-embedded-app IDs used in the HTML and a tuple containing a TrameApp constructor (the application to be started) and a list of arguments to pass to the constructor

Any necessary additional file (png, css, md, etc) should be stored in a "www" directory next to the source python file.

A dictionary associating application IDs and ports is maintained under the name `app_urls` in the main application's state.
