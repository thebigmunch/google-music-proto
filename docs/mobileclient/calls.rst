:mod:`mobileclient.calls <google_music_proto.mobileclient.calls>` --- Mobile API call classes
=============================================================================================

Example of making an HTTP request using the `requests <http://docs.python-requests.org>`_ library::

    # Assuming an authenticated session named 'session'.
    >>> from google_music_proto.mobileclient.calls import TrackFeed
    >>> call = TrackFeed()
    >>> response = session.request(
            call.method, call.url, params=call.params, headers=call.headers,
            data=call.body, allow_redirects=call.follow_redirects
        )


Attributes
----------

Call class instances have the following attributes:

.. attribute:: body

Binary-encoded body of the HTTP request.

.. attribute:: follow_redirects

Boolean to enable/disable request redirects.

.. attribute:: headers

Headers to send with the HTTP request.

.. attribute:: method

Method for the HTTP request.

.. attribute:: params

Dict of parameters to send in the query string of the HTTP request.

.. attribute:: url

URL for the HTTP request.


Classes
-------

.. automodule:: google_music_proto.mobileclient.calls
	:members:
