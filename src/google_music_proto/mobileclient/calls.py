import calendar
import time
import uuid

from attr import attrib, attrs

from .models import (
	MobileClientBatchCall, MobileClientCall, MobileClientFeedCall,
	MobileClientFetchCall, MobileClientStreamCall
)
from .types import QueryResultType, TrackRating

# TODO: Batch call schemas.
# TODO: Calls: add songs to playlist, reorder playlist songs, plentries.
# TODO: Situations are now returned through a protobuf call?


@attrs(slots=True)
class ActivityRecordRealtime(MobileClientBatchCall):
	"""Record track play and rate events.

	Use :meth:`play` to build track play event dicts.
	Use :meth:`rate` to build track rate events dicts.

	Parameters:
		events (list or dict): A list of event dicts or a single event dict.

	Attributes:
		endpoint: ``activity/recordrealtime``
		method: ``POST``
	"""

	endpoint = 'activity/recordrealtime'
	method = 'POST'
	batch_key = 'events'

	# TODO: termination?
	@staticmethod
	def play(track_id, track_duration, *, play_time=None, stream_auth_id=None):
		"""Build a track play event.

		Parameters:
			track_id (str): A track ID.
			track_duration (int or str): The duration of the track.
			play_time (int, Optional): The amount of time user played the track in seconds.
				Default: ``track_duration``
			stream_auth_id (str, Optional): The stream auth ID from a stream call's headers.

		Returns:
			dict: An event dict.
		"""

		event_id = str(uuid.uuid1())
		timestamp = int(time.time())
		play_time = track_duration if play_time is None else play_time * 1000

		if track_id.startswith('T'):
			track = {'metajamCompactKey': track_id}
		else:
			track = {'lockerId': track_id}

		return {
			'createdTimestampMillis': timestamp,
			'details': {
				'play': {
					'context': {},
					'isExplicitTrackStart': True,
					'playTimeMillis': play_time,
					'streamAuthId': stream_auth_id or '',
					'termination': 1,
					'trackDurationMillis': track_duration,
					'woodstockPlayDetails': {
						'isWoodstockPlay': False
					}
				}
			},
			'eventId': event_id,
			'trackId': track
		}

	@staticmethod
	def rate(track_id, rating):
		"""Build a track rate event.

		Parameters:
			track_id (str): A track ID.
			rating (int): 0 (not rated), 1 (thumbs down), or 5 (thumbs up).

		Returns:
			dict: An event dict.
		"""

		event_id = str(uuid.uuid1())
		timestamp = int(time.time())

		if track_id.startswith('T'):
			track = {'metajamCompactKey': track_id}
		else:
			track = {'lockerId': track_id}

		return {
			'createdTimestampMillis': timestamp,
			'details': {
				'rating': {
					'context': {},
					'rating': TrackRating(rating).name
				}
			},
			'eventId': event_id,
			'trackId': track
		}


@attrs(slots=True)
class BrowseStationCategories(MobileClientCall):
	"""Get a listing of station categories from the browse stations tab.

	Attributes:
		endpoint: ``browse/stationcategories``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.BrowseStationCategoriesSchema`
	"""

	endpoint = 'browse/stationcategories'
	method = 'GET'


@attrs(slots=True)
class BrowseStations(MobileClientCall):
	"""Get a listing of stations by category from browse tab.

	Parameters:
		station_category_id (str): A station category ID as found in :class:`BrowseStationCategories` response.

	Attributes:
		endpoint: ``browse/stations``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.BrowseStationsSchema`
	"""

	endpoint = 'browse/stations'
	method = 'GET'

	station_category_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._url += f"/{self.station_category_id}"


@attrs(slots=True)
class BrowseTopChart(MobileClientCall):
	"""Get a listing of the default top charts.

	Attributes:
		endpoint: ``browse/topchart``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.BrowseTopChartSchema`
	"""

	endpoint = 'browse/topchart'
	method = 'GET'


@attrs(slots=True)
class BrowseTopChartForGenre(MobileClientCall):
	"""Get a listing of top charts for a top chart genre.

	Parameters:
		genre_id (str): A top chart genre ID as found in :class:`BrowseTopChartGenres` response.

	Attributes:
		endpoint: ``browse/topchartforgenres``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.BrowseTopChartSchema`
	"""

	endpoint = 'browse/topchartforgenre'
	method = 'GET'

	genre_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._url += f'/{self.genre_id}'


@attrs(slots=True)
class BrowseTopChartGenres(MobileClientCall):
	"""Get a listing of genres from the browse top charts tab.

	Attributes:
		endpoint: ``browse/topchartgenres``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.BrowseTopChartGenresSchema`
	"""

	endpoint = 'browse/topchartgenres'
	method = 'GET'


@attrs(slots=True)
class Config(MobileClientCall):
	"""Get a listing of mobile client configuration settings.

	Attributes:
		endpoint: ``config``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.ConfigListSchema`
	"""

	endpoint = 'config'
	method = 'GET'


@attrs(slots=True)
class DeviceManagementInfo(MobileClientCall):
	"""Get a listing of devices registered to a Google Music account.

	Attributes:
		endpoint: ``devicemanagementinfo``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.UserClientIDListSchema`
	"""

	endpoint = 'devicemanagementinfo'
	method = 'GET'


@attrs(slots=True)
class DeviceManagementInfoDelete(DeviceManagementInfo):
	"""Delete a registered device.

	Parameters:
		device_id (str): A device ID as found in :class:`DeviceManagementInfo` response.

	Attributes:
		endpoint: ``devicemanagementinfo``
		method: ``DELETE``
	"""

	method = 'DELETE'

	device_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._params.update({
			'delete-id': self.device_id
		})


@attrs(slots=True)
class EphemeralTop(MobileClientFeedCall):
	"""Get a listing of 'Thumbs Up' store tracks.

	Note:
		'Thumbs Up' library tracks are handled client-side.
		Use the :class:`TrackFeed` call to find library tracks
		with a ``'rating'`` of 5.

	Note:
		The track list is paged. Getting all tracks will require looping through all pages.

	Parameters:
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``1000``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``ephemeral/top``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.EphemeralTopSchema`
	"""

	endpoint = 'ephemeral/top'

	max_results = attrib(default=1000)
	start_token = attrib(default=None)
	updated_min = attrib(default=None)


@attrs(slots=True)
class ExploreGenres(MobileClientCall):
	"""Get a listing of track genres.

	Parameters:
		parent_genre_id (str): A genre ID. If given, a listing of this genre's sub-genres is returned.

	Attributes:
		endpoint: ``explore/genres``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.GenreListSchema`
	"""

	endpoint = 'explore/genres'
	method = 'GET'

	parent_genre_id = attrib(default=None)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		if self.parent_genre_id is not None:
			self._params.update({'parent-genre-id': self.parent_genre_id})


# TODO: 'tabs' param?
# ExploreTabsSchema
@attrs(slots=True)
class ExploreTabs(MobileClientCall):
	endpoint = 'explore/tabs'
	method = 'GET'

	genre_id = attrib(default=None)
	num_items = attrib(default=100)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._params.update({
			'num-items': self.num_items
		})

		if self.genre_id is not None:
			self._params.update(genre=self.genre_id)


@attrs(slots=True)
class FetchAlbum(MobileClientFetchCall):
	"""Get information about an album.

	Parameters:
		album_id (str): The album ID to look up.
		include_description (bool): Include description of the album in the response.
		include_tracks (bool): Include tracks from the album in the response.
			Default: ``True``

	Attributes:
		endpoint: ``fetchalbum``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.AlbumSchema`
	"""

	endpoint = 'fetchalbum'

	album_id = attrib()
	include_description = attrib(default=True)
	include_tracks = attrib(default=True)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.album_id)

		include_tracks = self.include_tracks if self.include_tracks else None

		self._params.update({
			'include-description': self.include_description,
			'include-tracks': include_tracks
		})


@attrs(slots=True)
class FetchArtist(MobileClientFetchCall):
	"""Get information about an artist.

	Parameters:
		artist_id (str): The artist ID to look up.
		include_albums (bool): Include albums from the artist in the response.
			Default: ``True``
		num_related_artists (int): The maximum number of related artists to include in the response.
		num_top_tracks (int): The maximum number of top tracks to include in the response.

	Attributes:
		endpoint: ``fetchartist``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.ArtistSchema`
	"""

	endpoint = 'fetchartist'

	artist_id = attrib()
	include_albums = attrib(default=True)
	num_related_artists = attrib(default=5)
	num_top_tracks = attrib(default=5)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.artist_id)

		self._params.update({
			'include-albums': self.include_albums,
			'num-related_artists': self.num_related_artists,
			'num-top-tracks': self.num_top_tracks
		})


@attrs(slots=True)
class FetchTrack(MobileClientFetchCall):
	"""Get information about a track.

	Parameters:
		track_id (str): A track ID to look up.

	Attributes:
		endpoint: ``fetchtrack``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.StoreTrackSchema`
	"""

	endpoint = 'fetchtrack'

	track_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.track_id)


@attrs(slots=True)
class IsPlaylistShared(MobileClientCall):
	"""Check if a playlist is shared.

	Parameters:
		playlist_id (str): A playlist ID.

	Attributes:
		endpoint: ``isplaylistshared``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.IsPlaylistSharedSchema`
	"""

	endpoint = 'isplaylistshared'
	method = 'GET'

	playlist_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._params.update(id=self.playlist_id)


@attrs(slots=True)
class ListenNowGetDismissedItems(MobileClientCall):
	"""Get a listing of items dismissed from Listen Now tab.

	Attributes:
		endpoint: ``listennow/get_dismissed_items``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.ListenNowDismissedItemsSchema`
	"""

	endpoint = 'listennow/get_dismissed_items'
	method = 'GET'


@attrs(slots=True)
class ListenNowGetListenNowItems(MobileClientCall):
	"""Get a listing of Listen Now items.

	Note:
		This does not include situations; use :class:`ListenNowSituations` to get situations.

	Attributes:
		endpoint: ``listennow/getlistennowitems``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.ListenNowItemListSchema`
	"""

	endpoint = 'listennow/getlistennowitems'
	method = 'GET'


@attrs(slots=True)
class ListenNowSituations(MobileClientCall):
	"""Get a listing of Listen Now situations.

	Parameters:
		tz_offset (int): A time zone offset from UTC in seconds.

	Attributes:
		endpoint: ``listennow/situations``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.ListenNowSituationListSchema`
	"""

	endpoint = 'listennow/situations'
	method = 'POST'

	tz_offset = attrib(default=None)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		if self.tz_offset is None:
			self.tz_offset = calendar.timegm(time.localtime()) - calendar.timegm(time.gmtime())

		self._data.update({
			'requestSignals': {'timeZoneOffsetSecs': self.tz_offset}
		})


@attrs(slots=True)
class PlaylistBatch(MobileClientBatchCall):
	"""Create, delete, and edit playlists.

	Use :meth:`create` to build playlist creation mutation dicts.
	Use :meth:`delete` to build playlist delete mutation dicts.
	Use :meth:`edit` to build playlist edit mutation dicts.

	Parameters:
		mutations (list or dict): A list of mutation dicts or a single mutation dict.

	Attributes:
		endpoint: ``playlistbatch``
		method: ``POST``
	"""

	endpoint = 'playlistbatch'

	@staticmethod
	def create(name, description, share_state):
		"""Build a playlist create event.

		Parameters:
			name (str): Name to give the playlist.
			description (str): Description to give the playlist.
			make_public (bool): If ``True`` and account has a subscription, make playlist public.
				Default: ``False``

		Returns:
			dict: A mutation dict.
		"""

		timestamp = int(time.time() * 1000000)

		return {
			'create': {
				'creationTimestamp': timestamp,
				'deleted': False,
				'description': description,
				'lastModifiedTimestamp': timestamp,
				'name': name,
				'shareState': share_state,
				'type': 'USER_GENERATED'
			}
		}

	@staticmethod
	def delete(playlist_id):
		"""Build a playlist delete event.

		Parameters:
			playlist_id (str): A playlist ID.

		Returns:
			dict: A mutation dict.
		"""

		return {'delete': playlist_id}

	@staticmethod
	def edit(playlist_id, name, description, share_state):
		"""Build a playlist edit event.

		Parameters:
			playlist_id (str): A playlist ID.
			name (str): Name to give the playlist.
			description (str): Description to give the playlist.
			make_public (bool): If ``True`` and account has a subscription, make playlist public.

		Returns:
			dict: A mutation dict.
		"""

		return {
			'update': {
				'description': description,
				'id': playlist_id,
				'name': name,
				'shareState': share_state
			}
		}


@attrs(slots=True)
class PlaylistEntriesBatch(MobileClientBatchCall):
	"""Create, delete, and edit playlist entries.

	Use :meth:`create` to build playlist entry creation mutation dicts.
	Use :meth:`delete` to build playlist entry delete mutation dicts.
	Use :meth:`update` to build playlist entry update mutation dicts.

	Parameters:
		mutations (list or dict): A list of mutation dicts or a single mutation dict.

	Attributes:
		endpoint: ``plentriesbatch``
		method: ``POST``
	"""

	endpoint = 'plentriesbatch'

	@staticmethod
	def create(track_id, playlist_id, *, playlist_entry_id=None, preceding_entry_id=None, following_entry_id=None):
		"""Build a playlist entry create event.

		Note:


		Parameters:
			track_id (str): A track ID.
			playlist_id (str): A playlist ID.
			playlist_entry_id (str, Optional): A playlist entry ID to
				assign to the created entry.
				Default: Automatically generated.
			preceding_entry_id (str, Optional): The playlist entry ID
				that should precede the added track.
			following_entry_id (str, Optional): The playlist entry ID
				that should follow the added track.

		Returns:
			dict: A mutation dict.
		"""

		mutation = {
			'create': {
				'clientId': playlist_entry_id or str(uuid.uuid1()),
				'creationTimestamp': '-1',
				'deleted': False,
				'lastModifiedTimestamp': '0',
				'playlistId': playlist_id,
				'source': 2 if track_id.startswith('T') else 1,
				'trackId': track_id
			}
		}

		if preceding_entry_id is not None:
			mutation['create']['precedingEntryId'] = preceding_entry_id

		if following_entry_id is not None:
			mutation['create']['followingEntryId'] = following_entry_id

		return mutation

	@staticmethod
	def delete(playlist_entry_id):
		"""Build a playlist entry delete event.

		Parameters:
			playlist_entry_id (str): A playlist entryID.

		Returns:
			dict: A mutation dict.
		"""

		return {'delete': playlist_entry_id}

	@staticmethod
	def update(playlist_entry, *, preceding_entry_id=None, following_entry_id=None):
		"""Build a playlist entry update event.

		Parameters:
			playlist_id (str): A playlist ID.

		Returns:
			dict: A mutation dict.
		"""

		keys = {
			'clientId', 'deleted', 'id', 'lastModifiedTimestamp',
			'playlistId', 'source', 'trackId'
		}

		entry = {k: v for k, v in playlist_entry.items() if k in keys}
		entry['creationTimestamp'] = -1

		if preceding_entry_id is not None:
			entry['precedingEntryId'] = preceding_entry_id

		if following_entry_id is not None:
			entry['followingEntryId'] = following_entry_id

		mutation = {'update': entry}

		return mutation


@attrs(slots=True)
class PlaylistEntriesShared(MobileClientCall):
	"""Get a listing of shared playlist entries.

	Note:
		The shared playlist entries list is paged. Getting all shared playlist entries will require looping through all pages.

	Parameters:
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``250``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``plentries/shared``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.SharedPlaylistEntryListSchema`
	"""

	endpoint = 'plentries/shared'
	method = 'POST'

	share_tokens = attrib()
	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=0)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		if not isinstance(self.share_tokens, list):
			self.share_tokens = [self.share_tokens]

		self._data = {'entries': []}

		# TODO: includeDeleted.
		for share_token in self.share_tokens:
			self._data['entries'].append(
				{
					'maxResults': self.max_results,
					'shareToken': share_token,
					'startToken': self.start_token,
					'updatedMin': self.updated_min
				}
			)


@attrs(slots=True)
class PlaylistEntryFeed(MobileClientFeedCall):
	"""Get a listing of user playlist entries.

	Note:
		The playlist entry list is paged. Getting all playlist entries will require looping through all pages.

	Parameters:
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``250``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``plentryfeed``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.PlaylistEntryListSchema`
	"""

	endpoint = 'plentryfeed'

	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)


@attrs(slots=True)
class PlaylistFeed(MobileClientFeedCall):
	"""Get a listing of library playlists.

	Note:
		The playlist list is paged. Getting all playlists will require looping through all pages.

	Parameters:
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``250``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``playlistfeed``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.PlaylistListSchema`
	"""

	endpoint = 'playlistfeed'

	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)


# TODO: Explore params
@attrs(slots=True)
class Playlists(MobileClientCall):
	"""Get a listing of library playlists.

	Attributes:
		endpoint: ``playlists``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.PlaylistListSchema`
	"""

	method = 'GET'
	endpoint = 'playlists'


@attrs(slots=True)
class PlaylistsCreate(Playlists):
	"""Create a playlist.

	Parameters:
		name (str): Name to give the playlist.
		description (str): Description to give the playlist.
		public (bool): If ``True`` and account has a subscription, make playlist public.
			Default: ``False``

	Attributes:
		endpoint: ``playlists``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.PlaylistSchema`
	"""

	method = 'POST'

	name = attrib()
	description = attrib()
	public = attrib(default=False)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		timestamp = int(time.time() * 1000000)

		self._data.update({
			'creationTimestamp': timestamp,
			'deleted': False,
			'description': self.description,
			'lastModifiedTimestamp': timestamp,
			'name': self.name,
			'shareState': 'PUBLIC' if self.public else 'PRIVATE',
			'type': 'USER_GENERATED'
		})


@attrs(slots=True)
class PlaylistsDelete(Playlists):
	"""Delete a playlist.

	Parameters:
		playlist_id (str): A playlist ID.

	Attributes:
		endpoint: ``playlists``
		method: ``DELETE``
	"""

	method = 'DELETE'

	playlist_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._url += f'/{self.playlist_id}'


@attrs(slots=True)
class PlaylistsUpdate(Playlists):
	"""Edit a playlist.

	Attributes:
		endpoint: ``playlists``
		method: ``PUT``
		schema: :class:`~google_music_proto.mobileclient.schemas.PlaylistSchema`
	"""

	method = 'PUT'

	playlist_id = attrib()
	name = attrib()
	description = attrib()
	public = attrib(default=False)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._url += f'/{self.playlist_id}'

		timestamp = int(time.time() * 1000000)

		self._data.update({
			'creationTimestamp': timestamp,
			'deleted': False,
			'description': self.description,
			'lastModifiedTimestamp': timestamp,
			'name': self.name,
			'shareState': 'PUBLIC' if self.public else 'PRIVATE',
			'type': 'USER_GENERATED'
		})


@attrs(slots=True)
class PodcastBrowse(MobileClientCall):
	"""Get a listing of podcasts from Podcasts browse tab.

	Parameters:
		podcast_genre_id (str, Optional): A podcast genre ID as found in :class:`PodcastBrowseHierarchy`.
			Default: ``'JZCpodcasttopchartall'``

	Attributes:
		endpoint: ``podcast/browse``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.PodcastBrowseSchema`
	"""

	endpoint = 'podcast/browse'
	method = 'GET'

	podcast_genre_id = attrib(default='JZCpodcasttopchartall')

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._params.update(id=self.podcast_genre_id)


@attrs(slots=True)
class PodcastBrowseHierarchy(MobileClientCall):
	"""Get a listing of genres from Podcasts browse tab dropdown.

	Attributes:
		endpoint: ``podcast/browsehierarchy``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.PodcastBrowseHierarchySchema`
	"""

	endpoint = 'podcast/browsehierarchy'
	method = 'GET'


@attrs(slots=True)
class PodcastEpisode(MobileClientCall):
	"""Retrieve list of episodes from user-subscribed podcast series.

	Note:
		The podcast episode list is paged. Getting all podcast episodes will require looping through all pages.

	Parameters:
		device_id (str): A mobile device ID.
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``250``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``podcastepisode``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.PodcastEpisodeListSchema`
	"""

	endpoint = 'podcastepisode'
	method = 'GET'

	device_id = attrib(default=None)
	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		if self.device_id:
			self._headers.update({
				'X-Device-ID': self.device_id
			})

		self._params.update({
			'max-results': self.max_results,
			'start-token': self.start_token,
			'updated-min': self.updated_min
		})


@attrs(slots=True)
class PodcastEpisodeStreamURL(MobileClientStreamCall):
	"""Get a URL to stream a podcast episode.

	Parameters:
		podcast_episode_id (str): A podcast episode ID.
		device_id (str): A mobile device ID.
		quality (str, Optional): Stream quality is one of ``'hi'`` (320Kbps), ``'med'`` (160Kbps), or ``'low'`` (128Kbps).
			Default: ``'hi'``
	"""

	endpoint = 'fplay'

	podcast_episode_id = attrib()
	quality = attrib(default='hi')
	device_id = attrib(default=None)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.podcast_episode_id, quality=self.quality, device_id=self.device_id)

		self._params['mjck'] = self.podcast_episode_id


@attrs(slots=True)
class PodcastFetchEpisode(MobileClientFetchCall):
	"""Get information about a podcast episode.

	Parameters:
		podcast_episode_id (str): A podcast episode ID to look up.

	Attributes:
		endpoint: ``podcast/fetchepisode``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.PodcastEpisodeSchema`
	"""

	endpoint = 'podcast/fetchepisode'

	podcast_episode_id = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.podcast_episode_id)


@attrs(slots=True)
class PodcastFetchSeries(MobileClientFetchCall):
	"""Get information about a podcast series.

	Parameters:
		podcast_series_id (str): A podcast series ID to look up.

	Attributes:
		endpoint: ``podcast/fetchseries``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.PodcastSeriesSchema`
	"""

	endpoint = 'podcast/fetchseries'

	podcast_series_id = attrib()
	max_episodes = attrib(default=50)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.podcast_series_id)

		self._params.update(num=self.max_episodes)


@attrs(slots=True)
class PodcastSeries(MobileClientCall):
	"""Retrieve list of user-subscribed podcast series.

	Note:
		The podcast series list is paged. Getting all podcast series will require looping through all pages.

	Parameters:
		device_id (str): A mobile device ID.
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``250``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``podcastseries``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.PodcastSeriesListSchema`
	"""

	endpoint = 'podcastseries'
	method = 'GET'

	device_id = attrib(default=None)
	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		if self.device_id:
			self._headers.update({
				'X-Device-ID': self.device_id
			})

		self._params.update({
			'max-results': self.max_results,
			'start-token': self.start_token,
			'updated-min': self.updated_min
		})


# TODO: Implement.
@attrs(slots=True)
class PodcastSeriesBatchMutate(MobileClientBatchCall):
	"""

	Attributes:
		endpoint: ``podcastseries/batchmutate``
		method: ``POST``
	"""

	endpoint = 'podcastseries/batchmutate'

	@staticmethod
	def add():
		pass

	@staticmethod
	def delete():
		pass


# TODO: **kwargs with attrs.
@attrs(slots=True, init=False)
class Query(MobileClientCall):
	"""Search Google Music.

	Parameters:
		query (str): Search text.
		max_results (int): Maximum number of results per type to retrieve.
			Google only acepts values up to 100.
			Setting to ``None`` allows up to 1000 results per type but won't return playlist results.
			Default: ``100``
		kwargs (bool, Optional): Any of ``albums``, ``artists``, ``genres``, ``playlists``,
			``podcasts``, ``situations``, ``songs``, ``stations``, ``videos``
			set to ``True`` will include that result type in the response.
			Setting none of them will include all result types in the response.

	Attributes:
		endpoint: ``query``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.SearchResponseSchema`
	"""

	endpoint = 'query'
	method = 'GET'

	def __init__(self, query, *, max_results=100, **kwargs):
		super().__init__()

		if not kwargs:
			query_types = ','.join(
				type_.value
				for type_ in QueryResultType
			)
		else:
			# Make type names singular for enum lookup.
			query_types = ','.join(
				QueryResultType[type_[:-1]].value
				for type_ in kwargs
			)

		self._params.update({
			'ct': query_types,
			'ic': True,  # Setting to False or not including this returns old format which stopped including playlists.
			'max-results': max_results,
			'q': query
		})


@attrs(slots=True)
class QuerySuggestion(MobileClientCall):
	"""Get a search suggestion.

	Parameters:
		query (str): Search text.
	"""

	endpoint = 'querysuggestion'
	method = 'POST'

	query = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._data.update({'query': self.query})


# TODO: Implement.
@attrs(slots=True)
class RadioEditStation(MobileClientBatchCall):
	endpoint = 'radio/editstation'

	@staticmethod
	def add():
		pass

	@staticmethod
	def delete(station_id):
		return {'delete': station_id}

	@staticmethod
	def get():
		pass


@attrs(slots=True)
class RadioStation(MobileClientFeedCall):
	"""Generate a listing of stations.

	Note:
		The station list is paged. Getting all stations will require looping through all pages.

	Parameters:
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``250``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``radio/station``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.RadioListSchema`
	"""

	endpoint = 'radio/station'

	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)


# TODO: rz=sc/dl param?
# TODO: libraryContentOnly/recentlyPlayed with no stations?
# TODO: Make sure all uses of this endpoint are covered.
# TODO: Instant mixes/shuffle.
@attrs(slots=True)
class RadioStationFeed(MobileClientCall):
	"""Generate stations and get tracks from station(s).

	Parameters:
		station_infos (list): A list of station dicts containing keys:
			``'station_id'`` or ``'seed'``, ``'num_entries'``, ``'library_content_only'``, ``'recently_played'``.

			``station_id`` is a station ID.

			``'seed'`` is a dict containing a seed ID and seed type (``'seedType'``).
				A seed ID can be: ``artistId``, ``albumId``, ``genreId``, ``trackId`` (store track), ``trackLockerId`` (library track).
				See :data:`~google_music_proto.mobileclient.types.StationSeedType` for seed type values.

			``num_entries`` is the maximum number of tracks to return from the station.

			``library_content_only`` when True limits the station to library tracks. Default: ``False``

			``recently_played`` is a list of dicts in the form of {'id': '', 'type'} where ``id`` is a track ID and
				``type`` is 0 for a library track and 1 for a store track.
		num_entries (int): The total number of tracks to return. Default: ``25``
		num_stations (int): The number of stations to return when no station_infos is provided. Default: ``4``

	Attributes:
		endpoint: ``radio/stationfeed``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.RadioFeedSchema`
	"""

	endpoint = 'radio/stationfeed'
	method = 'POST'

	station_infos = attrib(default=None)
	num_entries = attrib(default=25)
	num_stations = attrib(default=4)

	# Recently played is list of {'id': , 'type': }.
	# Type 0 is library, 1 is store.
	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._data.update({
			'contentFilter': 1,
			'stations': []
		})

		if self.station_infos is None:
			self._data.update(
				mixes={
					'numEntries': self.num_entries,
					'numSeeds': self.num_stations
				}
			)
		else:
			for station_info in self.station_infos:
				if ('station_id' in station_info) and (station_info['station_id'] == 'IFL'):
					del station_info['station_id']
					station_info['seed'] = {'seedType': 6}

				if 'station_id' in station_info:
					self._data['stations'].append({
						'libraryContentOnly': station_info.get('libraryContentOnly', False),
						'numEntries': station_info.get('num_entries', 25),
						'radioId': station_info['station_id'],
						'recentlyPlayed': station_info.get('recently_played', [])
					})
				elif 'seed' in station_info:
					self._data['stations'].append({
						'libraryContentOnly': station_info.get('library_content_only', False),
						'numEntries': station_info.get('num_entries', 25),
						'seed': station_info['seed'],
						'recentlyPlayed': station_info.get('recently_played', [])
					})


@attrs(slots=True)
class RadioStationTrackStreamURL(MobileClientStreamCall):
	"""Get a URL to stream a station track with a free account.

	Note:
		Subscribed accounts should use :class:`TrackStreamURL`.

		Unlike the other stream calls, this returns JSON with a 'url' key, not the location in headers.

	Parameters:
		track_id (str): A station track ID.
		wentry_id (str): The ``wentryid`` from a station track dict.
		session_token (str): The ``sessionToken`` from a :class:`RadioStationFeed` response.
		quality (str, Optional): Stream quality is one of ``'hi'`` (320Kbps), ``'med'`` (160Kbps), or ``'low'`` (128Kbps).
			Default: ``'hi'``
		device_id (str): A mobile device ID.
	"""

	endpoint = 'wplay'

	track_id = attrib()
	wentry_id = attrib()
	session_token = attrib()
	quality = attrib(default='hi')
	device_id = attrib(default=None)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.track_id, quality=self.quality, device_id=self.device_id)

		del self._headers['X-Device-ID']  #

		self._params['sesstok'] = self.session_token
		self._params['wentryid'] = self.wentry_id

		if self.track_id.startswith('T'):
			self._params['mjck'] = self.track_id
		else:
			self._params['songid'] = self.track_id


@attrs(slots=True)
class TrackBatch(MobileClientBatchCall):
	"""Add, delete, and edit library tracks.

	Note:
		This previously supported editing most metadata.
		It now only supports changing ``rating``.
		However, changing the rating should be done with
		:class:`ActivityRecord` and :meth:`ActivityRecord.rate` instead.

	Use :meth:`add` to build track add mutation dicts.
	Use :meth:`delete` to build track delete mutation dicts.
	Use :meth:`edit` to build track edit mutation dicts.

	Parameters:
		mutations (list or dict): A list of mutation dicts or a single mutation dict.

	Attributes:
		endpoint: ``trackbatch``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.TrackBatchSchema`
	"""

	endpoint = 'trackbatch'

	@staticmethod
	def add(store_track):
		"""Build a track add event.

		Parameters:
			store_track (dict): A store track dict.

		Returns:
			dict: A mutation dict.
		"""

		store_track['trackType'] = 8

		return {'create': store_track}

	@staticmethod
	def delete(track_id):
		"""Build a track add event.

		Parameters:
			track_id (str): A track ID.

		Returns:
			dict: A mutation dict.
		"""

		return {'delete': track_id}

	@staticmethod
	def edit(track):
		"""Build a track edit event.

		Parameters:
			track (dict): A library track dict.

		Returns:
			dict: A mutation dict.
		"""

		return track


@attrs(slots=True)
class TrackFeed(MobileClientFeedCall):
	"""Get a listing of library tracks.

	Note:
		The track list is paged. Getting all tracks will require looping through all pages.

	Parameters:
		max_results (int, Optional): The maximum number of results on returned page.
			Default: ``250``
		start_token (str, Optional): The token of the page to return. Default: Not sent to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``trackfeed``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.TrackListSchema`
	"""

	endpoint = 'trackfeed'

	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)


@attrs(slots=True)
class Tracks(MobileClientCall):
	"""Get a listing of library tracks.

	Note:
		The track list is paged. Getting all tracks will require looping through all pages.

	Parameters:
		max_results (int, Optional): The maximum number of results on returned page. Max allowed is ``49995``.
			Default: ``1000``
		start_token (str, Optional): The token of the page to return. Default: ``None`` to get first page.
		updated_min (int, Optional): List changes since the given Unix epoch time in microseconds.

	Attributes:
		endpoint: ``tracks``
		method: ``GET``
		schema: :class:`~google_music_proto.mobileclient.schemas.TrackListSchema`
	"""

	endpoint = 'tracks'
	method = 'GET'

	max_results = attrib(default=1000)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		if self.start_token is not None:
			self._params.update({'start-token': self.start_token})

		self._params.update({
			'max-results': self.max_results,
			'updated-min': self.updated_min
		})


@attrs(slots=True)
class TrackStreamURL(MobileClientStreamCall):
	"""Get a URL to stream a track.

	Parameters:
		device_id (str): A mobile device ID.
		track_id (str): A library or store track ID.
			A Google Music subscription is required to stream store tracks.
		quality (str, Optional): Stream quality is one of ``'hi'`` (320Kbps), ``'med'`` (160Kbps), or ``'low'`` (128Kbps).
			Default: ``'hi'``
	"""

	endpoint = 'mplay'

	track_id = attrib()
	quality = attrib(default='hi')
	device_id = attrib(default=None)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.track_id, quality=self.quality, device_id=self.device_id)

		if self.track_id.startswith('T'):
			self._params['mjck'] = self.track_id
		else:
			self._params['songid'] = self.track_id
