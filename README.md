# trame-revealjs

This is a Python package designed to help integrate trame applications into reveal.js slides.

## Local set up

If you pulled the repository manually, you must retrieve the necessary reveal.js files with the following commands:

### Windows

    $env:SRC_URL="https://unpkg.com/reveal.js@6.0.1/dist"
    $env:DST_PATH="./src/trame_revealjs/serve"

    curl.exe $env:SRC_URL/reveal.js -Lo $env:DST_PATH/revealjs/js/reveal.js
    curl.exe $env:SRC_URL/plugin/notes.js -Lo $env:DST_PATH/revealjs/js/notes.js
    curl.exe $env:SRC_URL/plugin/markdown.js -Lo $env:DST_PATH/revealjs/js/markdown.js
    curl.exe $env:SRC_URL/plugin/highlight.js -Lo $env:DST_PATH/revealjs/js/highlight.js

    curl.exe $env:SRC_URL/reset.css -Lo $env:DST_PATH/revealjs/css/reset.css
    curl.exe $env:SRC_URL/reveal.css -Lo $env:DST_PATH/revealjs/css/reveal.css
    curl.exe $env:SRC_URL/theme/black.css -Lo $env:DST_PATH/revealjs/css/black.css
    curl.exe $env:SRC_URL/plugin/highlight/monokai.css -Lo $env:DST_PATH/revealjs/css/monokai.css

### Unix

    export SRC_URL=https://unpkg.com/reveal.js@6.0.1/dist
    export DST_PATH=./src/trame_revealjs/serve

    curl $SRC_URL/reveal.js -Lo $DST_PATH/revealjs/js/reveal.js
    curl $SRC_URL/plugin/notes.js -Lo $DST_PATH/revealjs/js/notes.js
    curl $SRC_URL/plugin/markdown.js -Lo $DST_PATH/revealjs/js/markdown.js
    curl $SRC_URL/plugin/highlight.js -Lo $DST_PATH/revealjs/js/highlight.js

    curl $SRC_URL/reset.css -Lo $DST_PATH/revealjs/css/reset.css
    curl $SRC_URL/reveal.css -Lo $DST_PATH/revealjs/css/reveal.css
    curl $SRC_URL/theme/black.css -Lo $DST_PATH/revealjs/css/black.css
    curl $SRC_URL/plugin/highlight/monokai.css -Lo $DST_PATH/revealjs/css/monokai.css

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
