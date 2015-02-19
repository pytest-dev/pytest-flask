Markers
=======

``pytest-flask`` registers the following markers. See the py.test
documentation_ on what marks are and for notes on using_ them.

.. _documentation: http://pytest.org/latest/mark.html
.. _using: http://pytest.org/latest/example/markers.html#marking-whole-classes-or-modules


``pytest.mark.app`` - pass options to your application config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: pytest.mark.app(**kwargs)

   The mark uses to pass options to your application config.

   :type kwargs: dict
   :param kwargs:
     The dictionary uses to extend application config.

   Example usage:

   .. code:: python

       @pytest.mark.app(debug=False)
       def test_app(app):
           assert not app.debug, 'Ensure the app not in debug mode'
