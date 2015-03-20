.. Family Legacy API documentation master file, created by
   sphinx-quickstart on Wed Mar 18 14:58:51 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Family Legacy API
=================

This document provides the information you need to access back-end resources for
"Family Legacy" application, and details on how to provision and deploythe API
it self.


.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api_v1
