from attr import attrs
from google.protobuf.message import DecodeError

from .constants import API_URL
from .pb import upload_pb2
from ..models import Call, ParsedResponse


@attrs(slots=True)
class MusicManagerCall(Call):
	base_url = API_URL
	request_type = response_type = upload_pb2.UploadResponse

	def __attrs_post_init__(self, uploader_id):
		self._data = self.request_type()
		self._data.uploader_id = uploader_id

		self._headers.update({
			'Content-Type': 'application/x-google-protobuf'
		})

		self._params.update({'version': 1})

		if self.endpoint:
			self._url = f'{self.base_url}/{self.endpoint}'

	@property
	def body(self):
		"""Binary-encoded body of the HTTP request."""

		return self._data.SerializeToString() if self._data else b''

	def parse_response(self, response_headers, response_body):
		try:
			res_body = self.response_type()
			res_body.ParseFromString(response_body)
		except DecodeError as e:
			raise

		if not self.check_success(res_body):
			raise

		return ParsedResponse(headers=response_headers, body=res_body)
