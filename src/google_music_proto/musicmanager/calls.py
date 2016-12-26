import os
import subprocess
from base64 import b64encode

import audio_metadata
import pendulum
from attr import attrib, attrs

from .models import MusicManagerCall
from .pb import download_pb2, locker_pb2, upload_pb2
from .utils import generate_client_id, get_album_art, transcode_to_mp3
from ..models import Call, JSONCall


@attrs(slots=True)
class ClientState(MusicManagerCall):
	"""Get information about the state of a Google Music account.

	Note:
		This provides things like the quota for uploaded songs.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
	"""

	endpoint = 'clientstate'
	method = 'POST'
	request_type = upload_pb2.ClientStateRequest

	uploader_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.uploader_id)


@attrs(slots=True)
class Export(Call):
	"""Download a song from a Google Music library.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
		song_id (str): A song ID.
	"""

	base_url = 'https://music.google.com/music/export'
	follow_redirects = True
	method = 'GET'

	uploader_id = attrib()
	song_id = attrib()

	def __attrs_post_init__(self):
		self._headers = {'X-Device-ID': self.uploader_id}
		self._params.update({'songid': self.song_id})
		self._url = Export.base_url


@attrs(slots=True)
class ExportIDs(Call):
	"""Get a listing of uploaded and purchased library tracks.

	Note:
		The track list is paged. Getting all tracks will require looping through all pages.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
		continuation_token (str, Optional): The token of the page to return.
			Default: Not sent to get first page.
		export_type (int, Optional): The type of tracks to return:
			1 for all tracks, 2 for promotional and purchased.
			Default: ``1``
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.
	"""

	base_url = 'https://music.google.com/music/exportids'
	method = 'POST'
	request_type = download_pb2.GetTracksToExportRequest
	response_type = download_pb2.GetTracksToExportResponse

	uploader_id = attrib()
	continuation_token = attrib(default=None)
	export_type = attrib(default=1)
	updated_min = attrib(default=-1)

	def __attrs_post_init__(self):
		self._data = self.request_type()
		self._data.client_id = self.uploader_id
		self._data.export_type = self.export_type
		self._data.updated_min = self.updated_min

		self._headers.update({
			'Content-Type': 'application/x-google-protobuf',
			'X-Device-ID': self.uploader_id
		})

		self._params.update({'version': 1})

		if self.continuation_token is not None:
			self._data.continuation_token = self.continuation_token

		self._url = ExportIDs.base_url

	@property
	def body(self):
		"""Binary-encoded body of the HTTP request."""

		return self._data.SerializeToString() if self._data else b''

	@staticmethod
	def check_success(response_body):
		return response_body.status == download_pb2.GetTracksToExportResponse.OK

	parse_response = MusicManagerCall.parse_response


@attrs(slots=True)
class GetJobs(MusicManagerCall):
	"""Get a listing of pending upload jobs.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
	"""

	endpoint = 'getjobs'
	method = 'POST'
	request_type = upload_pb2.GetJobsRequest

	uploader_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.uploader_id)

	@staticmethod
	def check_success(response):
		return response.get_tracks_success


@attrs(slots=True)
class Metadata(MusicManagerCall):
	"""Send upload track metadata to Google Music.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
		tracks (list): A list of tracks in the form of :class:`locker_pb2.Track`.
			Use :meth:`Metadata.get_track_info` to generate locker tracks from audio files.
	"""

	endpoint = 'metadata'
	method = 'POST'
	request_type = upload_pb2.UploadMetadataRequest

	uploader_id = attrib()
	tracks = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.uploader_id)

		self._data.track.extend(self.tracks)

		# do_not_rematch seems to be ignored.
		# Defaults to False.
		for track in self._data.track:
			track.do_not_rematch = False

	@staticmethod
	def get_track_info(song):
		"""Create a locker track from an audio file.

		Parameters:
			song (os.PathLike or str or audio_metadata.Format): The path to an audio file or an instance of :class:`audio_metadata.Format`.

		Returns:
			locker_pb2.Track: A locker track of the given audio file.
		"""

		try:
			if isinstance(song, audio_metadata.Format):
				metadata = song
			else:
				metadata = audio_metadata.load(song)
		except audio_metadata.AudioMetadataException as e:
			raise ValueError(f'Could not read metadata from {song}.') from e

		# TODO: Some might not match (E.g. AAC, ALAC).
		extension = metadata.__class__.__name__
		if not hasattr(locker_pb2.Track, extension):
			raise ValueError(f'{extension} is not a supported filetype.')

		# TODO: Can probably fill more fields.
		track = locker_pb2.Track()

		track.client_id = generate_client_id(metadata)

		track.original_content_type = getattr(locker_pb2.Track, extension)
		track.estimated_size = metadata.filesize
		try:
			track.last_modified_timestamp = int(os.path.getmtime(metadata.filepath))
		except TypeError:
			track.last_modified_timestamp = int(pendulum.utcnow().timestamp())

		track.play_count = 0
		track.client_date_added = 0
		track.recent_timestamp = 0
		track.rating = locker_pb2.Track.NOT_RATED

		bitrate = round(metadata.streaminfo.bitrate / 1000)
		track.original_bit_rate = bitrate
		track.duration_millis = int(metadata.streaminfo.duration * 1000)

		# If 'artist'/'album'/'title' aren't provided, they render as "undefined" in the web interface.
		# Setting them to empty strings fixes this.
		if 'artist' in metadata.tags:
			track.artist = metadata.tags.artist[0]
		else:
			track.artist = ''

		if 'album' in metadata.tags:
			track.album = metadata.tags.album[0]
		else:
			track.album = ''

		if 'title' in metadata.tags:
			track.title = metadata.tags.title[0]
		else:
			try:
				track.title = os.path.basename(song.filepath)
			except TypeError:
				track.title = ''

		if 'albumartist' in metadata.tags:
			track.album_artist = metadata.tags.albumartist[0]

		if 'bpm' in metadata.tags:
			track.beats_per_minute = int(metadata.tags.bpm[0])

		if 'composer' in metadata.tags:
			track.composer = metadata.tags.composer[0]

		if 'date' in metadata.tags:
			date = metadata.tags.date[0]
			year = pendulum.parse(date).year

			track.year = year

		if 'genre' in metadata.tags:
			track.genre = metadata.tags.genre[0]

		if 'discnumber' in metadata.tags:
			disc_split = metadata.tags.discnumber[0].split('/')

			track.track_number = int(disc_split[0])
			if len(disc_split) == 2:
				track.total_disc_count = int(disc_split[1])

		if 'disctotal' in metadata.tags:
			track.total_disc_count = int(metadata.tags.disctotal[0])

		if 'tracknumber' in metadata.tags:
			track_split = metadata.tags.tracknumber[0].split('/')

			track.track_number = int(track_split[0])
			if len(track_split) == 2:
				track.total_track_count = int(track_split[1])

		if 'tracktotal' in metadata.tags:
			track.total_track_count = int(metadata.tags.tracktotal[0])

		# The track protobuf message supports an additional metadata list field.
		# ALBUM_ART_HASH has been observed being sent in this field so far.
		# Append locker_pb2.AdditionalMetadata objects to additional_metadata.
		# AdditionalMetadata objects consist of two fields, 'tag_name' and 'value'.
		additional_metadata = []

		if additional_metadata:
			track.track_extras.additional_metadata.extend(additional_metadata)

		return track


@attrs(slots=True)
class Sample(MusicManagerCall):
	"""Send samples of audio files to Google Music.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
		track_samples (list): A list of track samples in the form of :class:`upload_pb2.TrackSample`.
			Use :meth:`Sample.generate_sample` to generate a track sample from an audio file.
	"""

	endpoint = 'sample'
	method = 'POST'
	request_type = upload_pb2.UploadSampleRequest

	uploader_id = attrib()
	track_samples = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.uploader_id)

		self._data.track_sample.extend(self.track_samples)

	# TODO: album art documentation.
	# TODO: Improved album art API?
	@staticmethod
	def generate_sample(song, track, sample_request, *, external_art=None):
		"""Generate a track sample from an audio file.

		Parameters:
			track (locker_pb2.Track): A locker track of the audio file as created by :meth:`Metadata.get_track_info`.
			sample_request (upload_pb2.SignedChallengeInfo):
				The ``'signed_challenge_info'`` portion for the audio file from the :class:`Metadata` response.
			external_art(bytes, optional): The binary data of an external album art image.
				If not provided, embedded album art will be used, if present.
		"""

		track_sample = upload_pb2.TrackSample()
		track_sample.track.CopyFrom(track)
		track_sample.signed_challenge_info.CopyFrom(sample_request)

		try:
			track_sample.sample = transcode_to_mp3(
				song, slice_start=sample_request.challenge_info.start_millis // 1000,
				slice_duration=sample_request.challenge_info.duration_millis // 1000, quality='128k'
			)

			album_art = external_art or get_album_art(song)

			if album_art:
				album_art_image = upload_pb2.ImageUnion()
				album_art_image.user_album_art = album_art
				track_sample.user_album_art.CopyFrom(album_art_image)
		except (OSError, ValueError, subprocess.CalledProcessError) as e:
			raise

		return track_sample


# TODO: Album art.
# TODO: contentType for title and external.
# TODO: FLAC seems to be put as 'audio/mpeg'?
# TODO: XingHeaderLength.
# TODO: AlbumArtLength/AlbumArtStart.
@attrs(slots=True)
class ScottyAgentPost(JSONCall):
	"""Request an upload URL for a track from Google Music.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
		server_track_id (str): The server ID of the audio file to upload as given in the response of :class:`Metadata` or :class:`Sample`.
		track (locker_pb2.Track): A locker track of the audio file as created by :meth:`Metadata.get_track_info`.
		song (os.PathLike or str or audio_metadata.Format): The path to an audio file or an instance of :class:`audio_metadata.Format`.
		external_art(bytes, optional): The binary data of an external album art image.
			If not provided, embedded album art will be used, if present.
		total_song_count (int, Optional): Total number of songs to be uploaded in this session.
			Default: 1
		total_uploaded_count (int, Optional): Number of songs uploaded in this session.
			Default: 0
	"""

	base_url = 'https://uploadsj.clients.google.com/uploadsj/scottyagent'
	method = 'POST'

	uploader_id = attrib()
	server_track_id = attrib()
	track = attrib()
	song = attrib()
	external_art = attrib(default=None)
	total_song_count = attrib(default=1)
	total_uploaded_count = attrib(default=0)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		inlined = {
			'title': 'jumper-uploader-title-42',
			'ClientId': self.track.client_id,
			'ClientTotalSongCount': str(self.total_song_count),
			'CurrentTotalUploadedCount': str(self.total_uploaded_count),
			'CurrentUploadingTrackArtist': self.track.artist,
			'CurrentUploadingTrack': self.track.title,
			'ServerId': self.server_track_id,
			'SyncNow': 'true',
			'TrackBitRate': str(self.track.original_bit_rate),
			'TrackDoNotRematch': 'false',
			'UploaderId': self.uploader_id
		}

		if not isinstance(self.song, audio_metadata.Format):
			self.song = audio_metadata.load(self.song)

		album_art = self.external_art or get_album_art(self.song)

		if album_art:
			inlined['AlbumArt'] = b64encode(album_art).decode()

		self._data.update({
			'clientId': 'Jumper Uploader',
			'createSessionRequest': {
				'fields': [
					{
						'external': {
							'filename': os.path.basename(self.song.filepath),
							'name': os.path.abspath(self.song.filepath),
							'put': {},
							# Size seems to be sent when uploading MP3, but not FLAC.
							# In fact, uploading FLAC directly fails when this is given.
							# Leaving it out works for everything.
							# 'size': track.estimated_size
						}
					}
				]
			},
			'protocolVersion': '0.8'
		})

		for field, value in inlined.items():
			self._data['createSessionRequest']['fields'].append(
				{
					'inlined': {
						'content': value,
						'name': field
					}
				}
			)

		self._url = ScottyAgentPost.base_url


@attrs(slots=True)
class ScottyAgentPut(Call):
	"""Upload a file to a Google Music library.

	Parameters:
		upload_url (str): The upload URL given by :class:`ScottyAgentPost` response.
		audio_file (os.PathLike or str or bytes): An audio file as :class:`os.PathLike`, a file/bytes-like object, or binary data.
		content_type (str): The mime type to be sent in the ContentType header field.
			Default: ``'audio/mpeg'``
	"""

	method = 'PUT'

	upload_url = attrib()
	audio_file = attrib()
	content_type = attrib(default='audio/mpeg')

	def __attrs_post_init__(self):
		if hasattr(self.audio_file, 'read'):
			self._data = self.audio_file.read()
		elif isinstance(self.audio_file, (os.PathLike, str)):
			with open(self.audio_file, 'rb') as f:
				self._data = f.read()
		elif isinstance(self.audio_file, bytes):
			self._data = self.audio_file
		else:
			raise ValueError("'audio_file' must be os.PathLike, filepath string, a file/bytes-like object, or binary data.")

		self._headers.update({'ContentType': self.content_type})
		self._url = self.upload_url

	parse_response = JSONCall.parse_response


@attrs(slots=True)
class UpAuth(MusicManagerCall):
	"""Authenticate device as a Music Manager uploader.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
		uploader_name (str): The name given to the device in the Google Music device listing.
	"""

	endpoint = 'upauth'
	method = 'POST'
	request_type = upload_pb2.UpAuthRequest
	response_type = upload_pb2.UpAuthResponse

	uploader_id = attrib()
	uploader_name = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.uploader_id)

		self._data.friendly_name = self.uploader_name

	@staticmethod
	def check_response(response):
		return response.HasField('auth_status') and response.auth_status == upload_pb2.UploadResponse.OK


@attrs(slots=True)
class UploadState(MusicManagerCall):
	"""Notify Google Music of the state of an upload.

	Parameters:
		uploader_id (str): A unique ID given as a MAC address.
			Only one Music Manager client may use a given uploader ID.
		state (str): Can be one of ``'START'``, ``'PAUSED'``, ``'STOPPED'``.
			Will be uppercased if lowercase is given.
	"""

	endpoint = 'uploadstate'
	method = 'POST'
	request_type = upload_pb2.UpdateUploadStateRequest

	uploader_id = attrib()
	state = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.uploader_id)

		state = self.state.upper()

		try:
			self._data.state = getattr(upload_pb2.UpdateUploadStateRequest, state)
		except AttributeError as e:
			raise ValueError from e
