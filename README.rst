trame-reveal
----------------------------------------

Reveal.js widget and helper application

License
----------------------------------------

This library is OpenSource and follow the Apache Software License

Installation
----------------------------------------

Install the application/library

.. code-block:: console

    pip install trame-reveal

Development setup
----------------------------------------

We recommend using uv for setting up and managing a virtual environment for your development.

.. code-block:: console

    # Create venv and install all dependencies
    uv sync --all-extras --dev

    # Activate environment
    source .venv/bin/activate

    # Install commit analysis
    pre-commit install
    pre-commit install --hook-type commit-msg



Build and install the Vue components

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

For running tests and checks, you can run ``nox``.

.. code-block:: console

    # run all
    nox

    # lint
    nox -s lint

    # tests
    nox -s tests


Guide
----------------------------------------

To embed one or multiple trame applications into a reveal.js set of slides:

1. Create an HTML file, with reveal.js syntax, for your slides
2. To embed a trame application in a slide use the syntax

.. code-block:: console

    <reveal-trame-app name="app1"></reveal-trame-app>

    `app-1` is an ID for your trame application. If you create another `<trame-embedded-app>` with the same ID, it will use the same application

3. Create a Python file where you instantiate a SlidesApp, it takes up to 5 arguments:

3.1 slides_path: The relative path to the HTML file containing the slides
3.2 server: An optional trame Server instance
3.3 port: a port (defaults to 8080) on which to deploy the application running the slides
3.4 iframe_port_start: the port from which will start the deployment of the embedded applications. If you have N applications, the ports from iframe_port_start to iframe_port_start + N - 1 will be used
3.5 trame_apps: a dictionary associating the trame-embedded-app IDs used in the HTML and a tuple containing a TrameApp constructor (the application to be started) and a list of arguments to pass to the constructor

Any necessary additional file (png, css, md, etc) should be stored in a "www" directory next to the source python file.

A dictionary associating application IDs and ports is maintained under the name ``app_urls`` in the main application's state.


Professional Support
----------------------------------------

* `Training <https://www.kitware.com/courses/trame/>`_: Learn how to confidently use trame from the expert developers at Kitware.
* `Support <https://www.kitware.com/trame/support/>`_: Our experts can assist your team as you build your web application and establish in-house expertise.
* `Custom Development <https://www.kitware.com/trame/support/>`_: Leverage Kitware’s 25+ years of experience to quickly build your web application.
