:mod:`musicmanager.calls <google_music_proto.musicmanager.calls>` --- Music Manager API call classes
====================================================================================================

.. module:: google_music_proto.musicmanager.calls

Example of making an HTTP request using the `requests <http://docs.python-requests.org>`_ library::

    # Assuming an authenticated session called 'session'.
    >>> from google_music_proto.musicmanager.calls import ExportIds
    >>> call = ExportIds(<uploader_id>)
    >>> response = session.request(
            call.method, call.url, params=call.params, headers=call.headers,
            data=call.body, allow_redirects=call.follow_redirects
        )


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

.. autoclass:: ClientState
.. autoclass:: Export
.. autoclass:: ExportIDs
.. autoclass:: GetJobs
.. autoclass:: Metadata
	:members: get_track_info
.. autoclass:: Sample
	:members: generate_sample
.. autoclass:: ScottyAgentPost
.. autoclass:: ScottyAgentPut
.. autoclass:: UpAuth
.. autoclass:: UploadState
