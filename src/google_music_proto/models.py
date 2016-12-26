import json

from attr import attrib, attrs


@attrs(frozen=True, slots=True)
class ParsedResponse:
	headers = attrib()
	body = attrib()


@attrs(slots=True)
class Call():
	follow_redirects = False

	_data = attrib(default=b'', init=False)
	_headers = attrib(factory=dict, init=False)
	_params = attrib(factory=dict, init=False)
	_url = attrib(default=None, init=False)

	@property
	def body(self):
		"""Binary-encoded body of the HTTP request."""

		return self._data

	@property
	def headers(self):
		"""Headers to send with the HTTP request."""

		return self._headers

	@property
	def params(self):
		"""Dict of parameters to send in the query string of the HTTP request."""

		return self._params

	@property
	def url(self):
		"""URL for the HTTP request."""

		return self._url

	@staticmethod
	def check_success(*args, **kwargs):
		return True

	def parse_response(self, response_headers, response_body):
		return ParsedResponse(headers=response_headers, body=response_body)


@attrs(slots=True)
class JSONCall(Call):
	_data = attrib(factory=dict, init=False)

	def __attrs_post_init__(self):
		self._headers['Content-Type'] = 'application/json'

	@property
	def body(self):
		"""Binary-encoded body of the HTTP request."""

		return json.dumps(self._data) if self._data else b''

	def parse_response(self, response_headers, response_body):
		body = json.loads(response_body) if response_body else b''

		return ParsedResponse(headers=response_headers, body=body)
