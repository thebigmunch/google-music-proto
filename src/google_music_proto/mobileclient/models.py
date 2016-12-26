__all__ = [
	'MobileClientBatchCall', 'MobileClientCall',
	'MobileClientFeedCall', 'MobileClientFetchCall',
	'MobileClientSchema', 'MobileClientStreamCall'
]

import base64
import hmac
import time
from hashlib import sha1

from attr import attrib, attrs
from marshmallow import Schema, ValidationError, pre_load

from .constants import API_URL, STREAM_URL
from ..models import Call, JSONCall


class MobileClientSchema(Schema):
	class Meta:
		strict = True

	@pre_load
	def check_for_unknown_fields(self, data):
		if not isinstance(data, dict):
			return

		new_fields = [key for key in data.keys() if key not in self.fields]

		if new_fields:
			raise ValidationError(f"Unknown fields found: {new_fields}")


@attrs(slots=True)
class MobileClientCall(JSONCall):
	base_url = API_URL
	follow_redirects = True

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._params.update({
			'alt': 'json',
			'dv': 0,
			'hl': 'en_US',
			'tier': 'fr'
		})

		if self.endpoint:
			self._url = f'{self.base_url}/{self.endpoint}'


@attrs(slots=True)
class MobileClientBatchCall(MobileClientCall):
	method = 'POST'

	def __attrs_post_init__(self, mutations):
		super().__attrs_post_init__()

		self._data.update({'mutations': mutations})


@attrs(slots=True)
class MobileClientFeedCall(MobileClientCall):
	method = 'POST'

	max_results = attrib(default=None)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		if self.max_results is not None:
			self._data.update({'max-results': self.max_results})

		if self.start_token is not None:
			self._data.update({'start-token': self.start_token})

		self._params.update({
			'updated-min': self.updated_min
		})


@attrs(slots=True)
class MobileClientFetchCall(MobileClientCall):
	method = 'GET'

	def __attrs_post_init__(self, item_id):
		super().__attrs_post_init__()

		self._params.update({
			'nid': item_id
		})


@attrs(slots=True)
class MobileClientStreamCall(Call):
	base_url = STREAM_URL
	method = 'GET'

	def __attrs_post_init__(self, item_id, quality='hi', device_id=None):
		self._params.update({
			'alt': 'json',
			'dv': 0,
			'locale': 'en_US',
			'tier': 'fr'
		})
		self._url = f'{self.base_url}/{self.endpoint}'

		if device_id:
			self._headers['X-Device-ID'] = device_id

		_s1 = base64.b64decode(
			b'VzeC4H4h+T2f0VI180nVX8x+Mb5HiTtGnKgH52Otj8ZCGDz9jRWyHb6QXK0JskSiOgzQfwTY5xgLLSdUSreaLVMsVVWfxfa8Rw=='
		)
		_s2 = base64.b64decode(
			b'ZAPnhUkYwQ6y5DdQxWThbvhJHN8msQ1rqJw0ggKdufQjelrKuiGGJI30aswkgCWTDyHkTGK9ynlqTkJ5L4CiGGUabGeo8M6JTQ=='
		)

		# bitwise and of _s1 and _s2 ascii, converted to string
		_key = ''.join([chr(c1 ^ c2) for (c1, c2) in zip(_s1, _s2)]).encode("ascii")
		_mac = hmac.new(_key, item_id.encode("utf-8"), sha1)
		_salt = str(int(time.time() * 1000))
		_mac.update(_salt.encode("utf-8"))

		_sig = base64.urlsafe_b64encode(_mac.digest())[:-1]

		self._params.update({
			'audio_formats': 'mp3',
			'net': 'mob',
			'opt': quality,
			'pt': 'e',
			'sig': _sig,
			'slt': _salt
		})
