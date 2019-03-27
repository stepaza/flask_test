Flask Application Documentation
****************************************

Welcome to the Flask application for members of the IDSC! This project serves as a `template` and follows all rules in the IDSC rulebook. These include all rules on:

+ Python Coding
+ Virtual Environment Control
+ Code Versioning
+ Code Documentation (`this is what you're reading right now`)
+ Sensitive Data Handling
+ Testing
+ Deployment with Docker
+ Security Issues for Exposed Applications

This is an example Flask App, so it's written in `Python` and documented with *Sphinx*. The final application is containerized with *Docker* and launched with *Gunicorn*. Not only does this project 
adhere to the IDSC rulebook, but it also addresses important network questions:

+ Once mounted, is the application available from all networks (clinical, public, etc.)?
+ If *no*, can this be achieved in collaboration with IT security (opening ports, firewall issues, etc.)?
+ Does this application adhere to the Insel IT security framework? 

A thorough how-to-Sphinx overview is beyond the scope of this project, so have a look at the 
`official documentation`_. For those already familiar with reStructuredText, there's also a `Quickguide on reStructuredText`_.

.. _official documentation: http://www.sphinx-doc.org/en/master/
.. _Quickguide on reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html


-------


The Flask App
==============

.. automodule:: flask_app
   :members:

Auxiliary Functions
====================

.. automodule:: flask_functions
   :members:


   
   