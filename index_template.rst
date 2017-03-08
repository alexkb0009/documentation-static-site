.. Documentation Static Site Generator documentation master file, created by
   sphinx-quickstart on Mon Mar  6 10:55:06 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Documentation for {{ title }}
=============================

.. toctree::
   :maxdepth: 2

   {% for section in sections %}
   {{ section.saveAs }}
   {% endfor %}
   jsdoc/index
   pydoc/modules
   



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`