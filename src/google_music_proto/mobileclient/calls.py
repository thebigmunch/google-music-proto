import calendar
import time
import uuid

from attr import attrib, attrs

from .models import (
	MobileClientBatchCall, MobileClientCall, MobileClientFeedCall,
	MobileClientFetchCall, MobileClientStreamCall
)
from .types import QueryResultType, SongRating

# TODO: Calls: increment play count, add songs to playlist, reorder playlist songs, mixes.
# TODO: plentries, trackstats, playlists/magic.


# TODO: Supports multiple events in one call.
@attrs(slots=True)
class ActivityRecordRealtime(MobileClientCall):
	endpoint = 'activity/recordrealtime'
	method = 'POST'


# TODO: streamAuthId from stream call headers necessary?
# @attrs(slots=True)
# class ActivityRecordPlay(ActivityRecordRealtime):
# 	song_id = attrib()
# 	song_duration = attrib()
#
# 	def __attrs_post_init__(self):
# 		super().__attrs_post_init__()
#
# 		event_id = str(uuid.uuid1())
# 		timestamp = int(time.time())
#
# 		if self.song_id.startswith('T'):
# 			track_id = {'metajamCompactKey': self.song_id}
# 		else:
# 			track_id = {'lockerId': self.song_id}
#
# 		self._data.update({
# 			'clientTimeMillis': 0,
# 			'events': [{
# 				'createdTimestampMillis': timestamp,
# 				'details': {
# 					'play': {
# 						'context': {},
# 						'isExplicitTrackStart': True,
# 						'playTimeMillis': self.song_duration,
# 						'streamAuthId': '',
# 						'termination': 1,
# 						'trackDurationMillis': self.song_duration,
# 						'woodstockPlayDetails': {
# 							'isWoodstockPlay': False
# 						}
# 					}
# 				},
# 				'eventId': event_id,
# 				'trackId': track_id
# 			}]
# 		})


@attrs(slots=True)
class ActivityRecordRate(ActivityRecordRealtime):
	song_id = attrib()
	rating = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		event_id = str(uuid.uuid1())
		timestamp = int(time.time())

		if self.song_id.startswith('T'):
			track_id = {'metajamCompactKey': self.song_id}
		else:
			track_id = {'lockerId': self.song_id}

		self._data.update({
			'clientTimeMillis': 0,
			'events': [{
				'createdTimestampMillis': timestamp,
				'details': {
					'rating': {
						'context': {},
						'rating': SongRating(self.rating).name
					}
				},
				'eventId': event_id,
				'trackId': track_id
			}]
		})


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
	"""Get a listing of promoted tracks.

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
	"""Get a listing of song genres.

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


# TODO: Schema.
# TODO: This doesn't appear to return anything while the ExploreTabs call returns new releases and top charts?
# @attrs(slots=True)
# class ExploreNewReleases(MobileClientCall):
# 	endpoint = 'explore/newreleases'
# 	method = 'GET'


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

	tz_offset = attrib(default=calendar.timegm(time.localtime()) - calendar.timegm(time.gmtime()))

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._data.update({
			'requestSignals': {'timeZoneOffsetSecs': self.tz_offset}
		})


@attrs(slots=True)
class PlaylistBatch(MobileClientBatchCall):
	endpoint = 'playlistbatch'


@attrs(slots=True)
class PlaylistBatchCreate(PlaylistBatch):
	"""Create playlist(s).

	Attributes:
		endpoint: ``playlistbatch``
		method: ``POST``
	"""

	playlist_infos = attrib()

	def __attrs_post_init__(self):
		timestamp = int(time.time() * 1000000)

		mutations = []

		for name, description, share_state in self.playlist_infos:
			mutations.append({
				'create': {
					'creationTimestamp': timestamp,
					'deleted': False,
					'description': description,
					'lastModifiedTimestamp': timestamp,
					'name': name,
					'shareState': share_state,
					'type': 'USER_GENERATED'
				}
			})

		super().__attrs_post_init__(mutations)


@attrs(slots=True)
class PlaylistBatchDelete(PlaylistBatch):
	"""Delete playlist(s).

	Attributes:
		endpoint: ``playlistbatch``
		method: ``POST``
	"""

	playlist_ids = attrib()

	def __attrs_post_init__(self):
		mutations = [{'delete': playlist_id} for playlist_id in self.playlist_ids]

		super().__attrs_post_init__(mutations)


@attrs(slots=True)
class PlaylistBatchUpdate(PlaylistBatch):
	"""Edit playlist(s).

	Attributes:
		endpoint: ``playlistbatch``
		method: ``POST``
	"""

	playlist_edits = attrib()

	def __attrs_post_init__(self):
		mutations = []

		for playlist_id, name, description, share_state in self.playlist_edits:
			mutations.append({
				'update': {
					'description': description,
					'id': playlist_id,
					'name': name,
					'shareState': share_state
				}
			})

		super().__attrs_post_init__(mutations)


# TODO
# @attrs(slots=True)
# class PlaylistEntriesBatch(MobileClientBatchCall):
# 	endpoint = 'plentriesbatch'
#
#
# # TODO: Necessary keys in json?
# @attrs(slots=True)
# class PlaylistEntriesBatchAdd(PlaylistEntriesBatch):
# 	"""
#
# 	Attributes:
# 		endpoint: ``plentriesbatch``
# 		method: ``POST``
# 	"""
#
# 	song_ids = attrib()
#
# 	def __attrs_post_init__(self):
# 		pass
#
#
# @attrs(slots=True)
# class PlaylistEntriesBatchDelete(PlaylistEntriesBatch):
# 	"""Delete playlist entries.
#
# 	Attributes:
# 		endpoint: ``plentriesbatch``
# 		method: ``POST``
# 	"""
#
# 	song_ids = attrib()
#
# 	def __attrs_post_init__(self):
# 		mutations = [{'delete': song_id} for song_id in self.song_ids]
#
# 		super().__attrs_post_init__(mutations)


@attrs(slots=True)
class PlaylistEntriesShared(MobileClientFeedCall):
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

	share_tokens = attrib()
	max_results = attrib(default=250)
	start_token = attrib(default=None)
	updated_min = attrib(default=-1)

	def __attrs_post_init__(self):
		# TODO: includeDeleted.
		self._data['entries'] = [{'shareToken': share_token} for share_token in self.share_tokens]


@attrs(slots=True)
class PlaylistEntryFeed(MobileClientFeedCall):
	"""Get a listing of library playlist entries.

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


# TODO: Not sure this exists.
# @attrs(slots=True)
# class PlaylistsDelete(Playlists):
# 	method = 'DELETE'
#
# 	playlist_id = attrib()
#
# 	def __attrs_post_init__(self):
# 		super().__attrs_post_init__()
#
# 		self._url += f'/{self.playlist_id}'


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


@attrs(slots=True)
class PodcastSeriesBatchMutate(MobileClientBatchCall):
	"""

	Attributes:
		endpoint: ``podcastseries/batchmutate``
		method: ``POST``
	"""

	endpoint = 'podcastseries/batchmutate'

	updates = attrib()

	def __attrs_post_init__(self, updates):
		super().__attrs_post_init__(updates)


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
			query_types = ','.join(str(type.value) for type in QueryResultType)
		else:
			query_types = ','.join(str(QueryResultType[type[:-1]].value) for type in kwargs)  # Make type names singular for enum lookup.

		self._params.update({
			'ct': query_types,
			'ic': True,  # Setting to False or not including this returns old format which stopped including playlists.
			'max-results': max_results,
			'q': query
		})


@attrs(slots=True)
class QuerySuggestion(MobileClientCall):
	__slots__ = ()

	endpoint = 'querysuggestion'
	method = 'POST'

	query = attrib()

	def __attrs_post_init__(self):
		super().__attrs_post_init__()

		self._data.update({'query': self.query})


@attrs(slots=True)
class RadioEditStation(MobileClientBatchCall):
	endpoint = 'radio/editstation'


# TODO: Implement.
@attrs(slots=True)
class RadioEditStationCreateOrGet(RadioEditStation):
	"""Create a radio station.

	Attributes:
		endpoint: ``radio/editstation``
		method: ``POST``
	"""

	def __init__(self, mutations):
		super().__init__(mutations)


@attrs(slots=True)
class RadioEditStationDelete(RadioEditStation):
	"""Delete a radio station.

	Attributes:
		endpoint: ``radio/editstation``
		method: ``POST``
	"""

	station_ids = attrib()

	def __attrs_post_init__(self):
		mutations = [{'delete': station_id} for station_id in self.station_ids]

		super().__attrs_post_init__(mutations)


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


# TODO: rz=sc param?
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

			``'seed'`` is a dict containing a seed ID and type.
				A seed ID can be: ``artistId``, ``albumId``, ``genreId``, ``trackId`` (store track), ``trackLockerId`` (library track).

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
				if 'station_id' in station_info:
					self._data['stations'].append({
						'libraryContentOnly': station_info.get('libraryContentOnly', False),
						'numEntries': station_info.get('num_entries', 100),
						'radioId': station_info['station_id'],
						'recentlyPlayed': station_info.get('recently_played', [])
					})
				elif 'seed' in station_info:
					self._data['stations'].append({
						'libraryContentOnly': station_info.get('library_content_only', False),
						'numEntries': station_info.get('num_entries', 100),
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
		song_id (str): A station song ID.
		wentry_id (str): The ``wentryid`` from a station song dict.
		session_token (str): The ``sessionToken`` from a :class:`RadioStationFeed` response.
		quality (str, Optional): Stream quality is one of ``'hi'`` (320Kbps), ``'med'`` (160Kbps), or ``'low'`` (128Kbps).
			Default: ``'hi'``
		device_id (str): A mobile device ID.
	"""

	endpoint = 'wplay'

	song_id = attrib()
	wentry_id = attrib()
	session_token = attrib()
	quality = attrib(default='hi')
	device_id = attrib(default=None)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.song_id, quality=self.quality, device_id=self.device_id)

		del self._headers['X-Device-ID']  #

		self._params['sesstok'] = self.session_token
		self._params['wentryid'] = self.wentry_id

		if self.song_id.startswith('T'):
			self._params['mjck'] = self.song_id
		else:
			self._params['songid'] = self.song_id


@attrs(slots=True)
class TrackBatch(MobileClientBatchCall):
	endpoint = 'trackbatch'


@attrs(slots=True)
class TrackBatchCreate(TrackBatch):
	"""Add store song(s) to library.

	Attributes:
		endpoint: ``trackbatch``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.TrackBatchSchema`
	"""

	store_songs = attrib()

	def __attrs_post_init__(self):
		mutations = []

		for song in self.store_songs:
			# TODO: What are the track types?
			song['trackType'] = 8

			mutations.append({'create': song})

		super().__attrs_post_init__(mutations)


@attrs(slots=True)
class TrackBatchDelete(TrackBatch):
	"""Delete song(s) from library.

	Parameters:
		song_ids (list): A list of song IDs.

	Attributes:
		endpoint: ``trackbatch``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.TrackBatchSchema`
	"""

	track_ids = attrib()

	def __attrs_post_init__(self):
		mutations = [{'delete': track_id} for track_id in self.track_ids]

		super().__attrs_post_init__(mutations)


@attrs(slots=True)
class TrackBatchUpdate(TrackBatch):
	"""Edit song(s) in library.

	Note:
		This previously supported changing most metadata. It now only supports changing ``rating``.

	Attributes:
		endpoint: ``trackbatch``
		method: ``POST``
		schema: :class:`~google_music_proto.mobileclient.schemas.TrackBatchSchema`
	"""

	track_edits = attrib()

	def __attrs_post_init__(self):
		mutations = self.track_edits

		super().__attrs_post_init__(mutations)


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


# TODO: Implement.
# @attrs(slots=True)
# class TrackStats(MobileClientCall):
# 	endpoint = 'trackstats'
# 	method = 'POST'


@attrs(slots=True)
class TrackStreamURL(MobileClientStreamCall):
	"""Get a URL to stream a track.

	Parameters:
		device_id (str): A mobile device ID.
		song_id (str): A library or store song ID.
			A Google Music subscription is required to stream store songs.
		quality (str, Optional): Stream quality is one of ``'hi'`` (320Kbps), ``'med'`` (160Kbps), or ``'low'`` (128Kbps).
			Default: ``'hi'``
	"""

	endpoint = 'mplay'

	song_id = attrib()
	quality = attrib(default='hi')
	device_id = attrib(default=None)

	def __attrs_post_init__(self):
		super().__attrs_post_init__(self.song_id, quality=self.quality, device_id=self.device_id)

		if self.song_id.startswith('T'):
			self._params['mjck'] = self.song_id
		else:
			self._params['songid'] = self.song_id
