.. Documentation Static Site Generator documentation master file, created by
   sphinx-quickstart on Mon Mar  6 10:55:06 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


{{ title }}
=============================

.. toctree::
   :maxdepth: 2

   static_documentation_contents
   jsdoc/index
   pydoc/modules
   

{% if readme %}
Getting Started
===============

.. include:: <{{readme}}>

{% endif %}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`