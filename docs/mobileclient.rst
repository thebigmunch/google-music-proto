.. _mobileclient:

=============
Mobile Client
=============

Classes representing calls, schemas, and types for the Google Music mobile client API.

Example of making an HTTP request using the `requests <http://docs.python-requests.org>`_ library::

	# Assuming an authenticated session called 'session'.
	>>> call = TrackFeed()
	>>> response = session.request(
			call.method, call.url, params=call.params, headers=call.headers,
			data=call.body, allow_redirects=call.follow_redirects
		)


Calls
=====

Attributes
----------

Call classes have the following attributes:

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

Classes representing calls to the Google Music mobile client API.

.. automodule:: google_music_proto.mobileclient.calls
	:members:


Schemas
-------

Classes representing schemas to validate Google Music mobile client responses.

All mobile client schemas are a subclass of :class:`marshmallow.Schema` with the ``strict`` option set to ``True``.
Unknown fields trigger a :exc:`marshmallow.ValidationError <marshmallow.exceptions.ValidationError>` exception.

.. automodule:: google_music_proto.mobileclient.schemas
	:members:


Types
-----

.. automodule:: google_music_proto.mobileclient.types
	:members:
