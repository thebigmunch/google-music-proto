# flake8: noqa

__all__ = [
	'AlbumSchema', 'ArtRefSchema', 'ArtistSchema', 'AttributionSchema', 'BrowseStationCategoriesSchema',
	'BrowseStationsSchema', 'BrowseTopChartGenresSchema', 'BrowseTopChartSchema', 'ColorStyleSchema',
	'ConfigEntrySchema', 'ConfigListEntriesSchema', 'ConfigListSchema', 'DeviceManagementInfoSchema',
	'DistilledContextWrapperSchema', 'EphemeralTopItemsSchema', 'EphemeralTopSchema', 'ExploreTabEntityGroupSchema',
	'ExploreTabEntitySchema', 'ExploreTabSchema', 'ExploreTabsSchema', 'GenreListSchema', 'GenreRefSchema', 'GenreSchema',
	'ImageColorStylesSchema', 'ImageRefSchema', 'IsPlaylistSharedSchema', 'ListenNowAlbumIDSchema', 'ListenNowAlbumSchema',
	'ListenNowDismissedItemsSchema', 'ListenNowItemListSchema', 'ListenNowItemSchema', 'ListenNowRadioStationIDSchema',
	'ListenNowRadioStationSchema', 'ListenNowSituationListSchema', 'PlaylistEntryItemsSchema', 'PlaylistEntryListSchema',
	'PlaylistEntrySchema', 'PlaylistListItemsSchema', 'PlaylistListSchema', 'PlaylistSchema', 'PodcastBrowseHierarchySchema',
	'PodcastBrowseSchema', 'PodcastEpisodeListItemsSchema', 'PodcastEpisodeListSchema', 'PodcastEpisodeSchema',
	'PodcastGenreSchema', 'PodcastSeriesListItemsSchema', 'PodcastSeriesListSchema', 'PodcastSeriesSchema',
	'PodcastSeriesUserPreferencesSchema', 'RadioFeedItemsSchema', 'RadioFeedSchema', 'RadioListItemsSchema',
	'RadioListSchema', 'RadioSeedMetadataSchema', 'RadioSeedSchema', 'RadioStationSchema', 'SearchResponseSchema',
	'SearchResultSchema', 'SearchResultVideoSchema', 'SearchSuggestedQuerySchema', 'SearchSuggestionSchema',
	'SharedPlaylistEntryItemSchema', 'SharedPlaylistEntryListSchema', 'SharedPlaylistEntrySchema', 'SituationSchema',
	'StationCategorySchema', 'StoreTrackSchema', 'TopChartHeaderSchema', 'TopChartSchema', 'TrackBatchItemSchema',
	'TrackBatchSchema', 'TrackListItemsSchema', 'TrackListSchema', 'TrackSchema', 'UploadedTrackSchema',
	'UserClientIDListItemsSchema', 'UserClientIDListSchema', 'VideoSchema', 'VideoThumbnailSchema'
]

from marshmallow import fields
from marshmallow.validate import Equal, OneOf, Range

from .models import MobileClientSchema


class AdTargetingSchema(MobileClientSchema):
	"""

	**Validates**::

		{'keyword': ['keyword']}
	"""

	keyword = fields.List(fields.Str, required=True)


class ArtRefSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'url': 'url'
		}
	"""

	url = fields.Str(required=True)


class AttributionSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'kind': 'sj#attribution',
			'license_title': 'license title',
			'license_url': 'license url',
			'source_title': 'source title',
			'source_url': 'source url'
		}
	"""

	kind = fields.Str(required=True, validate=Equal('sj#attribution'))
	license_title = fields.Str()
	license_url = fields.Str()
	source_title = fields.Str()
	source_url = fields.Str()


class ColorStyleSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'blue': 0,
			'green': 0,
			'red': 0
		}
	"""

	blue = fields.Int(required=True, validate=Range(0, 255))
	green = fields.Int(required=True, validate=Range(0, 255))
	red = fields.Int(required=True, validate=Range(0, 255))


class DistilledContextWrapperSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'distilledContextToken': 'distilledContextToken'
		}
	"""

	distilledContextToken = fields.Str(required=True)


class GenreRefSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'id': 'id',
			'kind': 'sj#genreRef',
			'title': 'title'
		}
	"""

	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#genreRef'))
	title = fields.Str(required=True)


class ImageColorStylesSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'accent': {
				'blue': 0,
				'green': 0,
				'red': 0
			},
			'primary': {
				'blue': 0,
				'green': 0,
				'red': 0
			},
			'scrim': {
				'blue': 0,
				'green': 0,
				'red': 0
			}
		}
	"""

	accent = fields.Nested(ColorStyleSchema, required=True)
	primary = fields.Nested(ColorStyleSchema, required=True)
	scrim = fields.Nested(ColorStyleSchema, required=True)


class ImageRefSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'aspectRatio': 'aspectRatio',
			'autogen': False,
			'colorStyles': {
				'accent': {
					'blue': 0,
					'green': 0,
					'red': 0
				},
				'primary': {
					'blue': 0,
					'green': 0,
					'red': 0
				},
				'scrim': {
					'blue': 0,
					'green': 0,
					'red': 0
				}
			},
			'kind': 'sj#imageRef',
			'url': 'url'
		}
	"""

	aspectRatio = fields.Str()
	autogen = fields.Bool()
	colorStyles = fields.Nested(ImageColorStylesSchema)
	kind = fields.Str(required=True, validate=Equal('sj#imageRef'))
	url = fields.Str(required=True)


class VideoThumbnailSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'height': 100,
			'url': 'url',
			'width': 100
		}
	"""

	height = fields.Int(required=True)
	url = fields.Str(required=True)
	width = fields.Int(required=True)


class VideoSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'id': 'id',
			'kind': 'sj#video',
			'thumbnails': [
				{
					'height': 100,
					'url': 'url',
					'width': 100
				}
			]
		}
	"""

	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#video'))
	thumbnails = fields.Nested(VideoThumbnailSchema, many=True)


class StoreTrackSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'album': 'album',
			'albumArtRef': [IMAGE_REF],
			'albumArtist': 'albumArtist',
			'albumAvailableForPurchase': True,
			'albumId': 'albumId',
			'artist': 'artist',
			'artistArtRef': [IMAGE_REF],
			'artistId': ['artistId'],
			'composer': 'composer',
			'discNumber': 1,
			'durationMillis': 'durationMillis',
			'estimatedSize': 'estimatedSize',
			'explicitType': 'explicitType',
			'genre': 'genre',
			'kind': 'sj#track',
			'lastModifiedTimestamp': 'lastModifiedTimestamp',
			'lastRatingChangeTimestamp': 'lastRatingChangeTimestamp',
			'nid': 'nid',
			'playCount': 42,
			'primaryVideo': VIDEO,
			'rating': '5',
			'storeId': 'storeId',
			'title': 'title',
			'trackAvailableForPurchase': True,
			'trackAvailableForSubscription': True,
			'trackNumber': 1,
			'trackType': 'trackType',
			'year': 2000
		}
	"""

	album = fields.Str(required=True)
	albumArtRef = fields.Nested(ImageRefSchema, many=True, required=True)
	albumArtist = fields.Str(required=True)
	albumAvailableForPurchase = fields.Bool(required=True)
	albumId = fields.Str(required=True)
	artist = fields.Str(required=True)
	artistArtRef = fields.Nested(ImageRefSchema, many=True)
	artistId = fields.List(fields.Str, required=True)
	composer = fields.Str(required=True)
	discNumber = fields.Int(required=True)
	durationMillis = fields.Str(required=True)
	estimatedSize = fields.Str(required=True)
	explicitType = fields.Str(required=True)
	genre = fields.Str()
	kind = fields.Str(required=True, validate=Equal('sj#track'))
	lastModifiedTimestamp = fields.Str()
	lastRatingChangeTimestamp = fields.Str()
	nid = fields.Str(required=True)
	playCount = fields.Int()
	primaryVideo = fields.Nested(VideoSchema)
	rating = fields.Str(
		validate=OneOf(
			['0', '1', '5'],
			labels=('Not Rated', 'Thumbs Down', 'Thumbs Up'),
			error="rating is not one of {choices} ({labels})."
		)
	)
	storeId = fields.Str(required=True)
	title = fields.Str(required=True)
	trackAvailableForPurchase = fields.Bool(required=True)
	trackAvailableForSubscription = fields.Bool(required=True)
	trackNumber = fields.Int(required=True)
	trackType = fields.Str(required=True)
	year = fields.Int(required=True)


class UploadedTrackSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'album': 'album',
			'albumArtRef': [IMAGE_REF],
			'albumArtist': 'albumArtist',
			'albumId': 'albumId',
			'artist': 'artist',
			'artistArtRef': [IMAGE_REF],
			'artistId': ['artistId'],
			'beatsPerMinute': 142,
			'clientId': 'clientId',
			'comment': 'comment',
			'composer': 'composer',
			'creationTimestamp': 'creationTimestamp',
			'deleted': False,
			'discNumber': 1,
			'durationMillis': 'durationMillis',
			'estimatedSize': 'estimatedSize',
			'explicitType': 'explicitType',
			'genre': 'genre',
			'id': 'id',
			'kind': 'sj#track',
			'lastModifiedTimestamp': 'lastModifiedTimestamp',
			'lastRatingChangeTimestamp': 'lastRatingChangeTimestamp',
			'nid': 'nid',
			'playCount': 42,
			'primaryVideo': VIDEO,
			'rating': '5',
			'recentTimestamp': 'recentTimestamp',
			'storeId': 'storeId',
			'title': 'title',
			'totalDiscCount': 1,
			'totalTrackCount': 1,
			'trackNumber': 1,
			'trackType': 'trackType',
			'year': 2000
		}
	"""

	album = fields.Str(required=True)
	albumArtRef = fields.Nested(ImageRefSchema, many=True)
	albumArtist = fields.Str()
	albumId = fields.Str()
	artist = fields.Str(required=True)
	artistArtRef = fields.Nested(ImageRefSchema, many=True)
	artistId = fields.List(fields.Str)
	beatsPerMinute = fields.Int()
	clientId = fields.Str(required=True)
	comment = fields.Str()
	composer = fields.Str()
	creationTimestamp = fields.Str(required=True)
	deleted = fields.Bool(required=True)
	discNumber = fields.Int()
	durationMillis = fields.Str(required=True)
	estimatedSize = fields.Str()
	explicitType = fields.Str()
	genre = fields.Str()
	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#track'))
	lastModifiedTimestamp = fields.Str(required=True)
	lastRatingChangeTimestamp = fields.Str()
	nid = fields.Str()
	playCount = fields.Int()
	primaryVideo = fields.Nested(VideoSchema)
	rating = fields.Str(
		required=True,
		validate=OneOf(
			['0', '1', '5'],
			labels=('Not Rated', 'Thumbs Down', 'Thumbs Up'),
			error="rating is not one of {choices} ({labels})."
		)
	)
	recentTimestamp = fields.Str(required=True)
	storeId = fields.Str()
	title = fields.Str(required=True)
	totalDiscCount = fields.Int()
	totalTrackCount = fields.Int()
	trackNumber = fields.Int()
	trackType = fields.Str()
	year = fields.Int()


class TrackSchema(MobileClientSchema):
	"""Combination of :class:`StoreTrackSchema` and :class:`UploadedTrackSchema`."""

	album = fields.Str(required=True)
	albumArtRef = fields.Nested(ImageRefSchema, many=True)
	albumArtist = fields.Str()
	albumAvailableForPurchase = fields.Bool()
	albumId = fields.Str()
	artist = fields.Str(required=True)
	artistArtRef = fields.Nested(ImageRefSchema, many=True)
	artistId = fields.List(fields.Str)
	beatsPerMinute = fields.Integer()
	clientId = fields.Str()
	comment = fields.Str()
	composer = fields.Str()
	creationTimestamp = fields.Str()
	deleted = fields.Bool()
	discNumber = fields.Int()
	durationMillis = fields.Str(required=True)
	estimatedSize = fields.Str()
	explicitType = fields.Str()
	genre = fields.Str()
	id = fields.Str()
	kind = fields.Str(required=True, validate=Equal('sj#track'))
	lastModifiedTimestamp = fields.Str()
	lastRatingChangeTimestamp = fields.Str()
	nid = fields.Str()
	playCount = fields.Int()
	primaryVideo = fields.Nested(VideoSchema)
	rating = fields.Str(
		validate=OneOf(
			['0', '1', '5'],
			labels=('Not Rated', 'Thumbs Down', 'Thumbs Up'),
			error="rating is not one of {choices} ({labels})."
		)
	)
	recentTimestamp = fields.Str()
	storeId = fields.Str()
	title = fields.Str(required=True)
	totalDiscCount = fields.Int()
	totalTrackCount = fields.Int()
	trackAvailableForPurchase = fields.Bool()
	trackAvailableForSubscription = fields.Bool()
	trackNumber = fields.Int()
	trackType = fields.Str()
	year = fields.Int()


class GenreSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'children': ['child'],
			'id': 'id',
			'images': [ART_REF],
			'kind': 'sj#musicGenre',
			'name': 'name',
			'parentId': 'parentId'
		}
	"""

	children = fields.List(fields.Str)
	id = fields.Str(required=True)
	images = fields.Nested(ArtRefSchema, many=True)
	kind = fields.Str(required=True, validate=Equal('sj#musicGenre'))
	name = fields.Str()
	parentId = fields.Str()


class PlaylistSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'accessControlled': False,
			'albumArtRef': [ART_REF],
			'clientId': 'clientId',
			'contentType': 'contentType',
			'creationTimestamp': 'creationTimestamp',
			'deleted': False,
			'description': 'description',
			'explicitType': 'explicitType',
			'id': 'id',
			'kind': 'sj#playlist',
			'lastModifiedTimestamp': 'lastModifiedTimestamp',
			'name': 'name',
			'ownerName': 'ownerName',
			'ownerProfilePhotoUrl': 'ownerProfilePhotoUrl',
			'recentTimestamp': 'recentTimestamp',
			'shareState': 'shareState',
			'shareToken': 'shareToken',
			'type': 'USER_GENERATED'
		}

	"""

	accessControlled = fields.Bool()
	albumArtRef = fields.Nested(ArtRefSchema, many=True)
	clientId = fields.Str()
	contentType = fields.Str()
	creationTimestamp = fields.Str(required=True)
	deleted = fields.Bool(required=False)
	description = fields.Str()
	explicitType = fields.Str()
	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#playlist'))
	lastModifiedTimestamp = fields.Str(required=True)
	name = fields.Str(required=True)
	ownerName = fields.Str()
	ownerProfilePhotoUrl = fields.Str()
	recentTimestamp = fields.Str()
	shareState = fields.Str(validate=OneOf(['PRIVATE', 'PUBLIC']))
	shareToken = fields.Str(required=True)
	type = fields.Str(
		validate=OneOf(
			['MAGIC', 'SHARED', 'USER_GENERATED'],
			error="type is not one of {choices}."
		)
	)


class AlbumSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'albumArtist': 'albumArtist',
			'albumArtRef': 'albumArtRef',
			'albumId': 'albumId',
			'artist': 'artist',
			'artistId': ['artistId'],
			'contentType': 'contentType',
			'description': 'description',
			'description_attribution': ATTRIBUTION,
			'explicitType': 'explicitType',
			'kind': 'sj#album',
			'name': 'name',
			'tracks': [STORE_TRACK],
			'year': 2000
		}
	"""

	albumArtist = fields.Str()
	albumArtRef = fields.Str()
	albumId = fields.Str(required=True)
	artist = fields.Str()
	artistId = fields.List(fields.Str)
	contentType = fields.Str()
	description = fields.Str()
	description_attribution = fields.Nested(AttributionSchema)
	explicitType = fields.Str()
	kind = fields.Str(required=True, validate=Equal('sj#album'))
	name = fields.Str(required=True)
	tracks = fields.Nested(StoreTrackSchema, many=True)
	year = fields.Int()


class ArtistSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'albums': [ALBUM],
			'artistArtRef': 'artistArtRef',
			'artistArtRefs': [IMAGE_REF],
			'artistBio': 'artistBio',
			'artistId': 'artistId',
			'artist_bio_attribution': ATTRIBUTION,
			'kind': 'sj#artist',
			'name': 'name',
			'related_artists': [],
			'topTracks': [STORE_TRACK],
			'total_albums': 1
		}
	"""

	albums = fields.Nested(AlbumSchema, many=True)
	artistArtRef = fields.Str()
	artistArtRefs = fields.Nested(ImageRefSchema, many=True)
	artistBio = fields.Str()
	artistId = fields.Str()
	artist_bio_attribution = fields.Nested(AttributionSchema)
	kind = fields.Str(required=True, validate=Equal('sj#artist'))
	name = fields.Str(required=True)
	related_artists = fields.Nested('self', many=True)
	topTracks = fields.Nested(StoreTrackSchema, many=True)
	total_albums = fields.Int()


class DeviceManagementInfoSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'friendlyName': 'friendlyName',
			'id': 'id',
			'kind': 'sj#devicemanagementinfo',
			'lastAccessedTimeMs': 42,
			'smartPhone': True,
			'type': 'type'
		}
	"""

	friendlyName = fields.Str(required=True)
	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#devicemanagementinfo'))
	lastAccessedTimeMs = fields.Int(required=True)
	smartPhone = fields.Bool()
	type = fields.Str(required=True)


class ExploreTabEntitySchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'album': ALBUM,
			'genre': GENRE,
			'kind': 'sj#exEntity',
			'playlist': PLAYLIST,
			'track': STORE_TRACK
		}
	"""

	album = fields.Nested(AlbumSchema)
	genre = fields.Nested(GenreSchema)
	kind = fields.Str(requried=True, validate=Equal('sj#exEntity'))
	playlist = fields.Nested(PlaylistSchema(
		only=['albumArtRef', 'description', 'kind', 'name', 'ownerName', 'shareToken', 'type'])
	)
	track = fields.Nested(StoreTrackSchema)


class ExploreTabEntityGroupSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'continuationToken': 'continuationToken',
			'entities': [EXPLORE_TAB_ENTITY],
			'group_type': 'group_type',
			'kind': 'sj#exEntityGroup',
			'start_position': 0,
			'title': 'title'
		}
	"""

	continuation_token = fields.Str()
	description = fields.Str()
	entities = fields.Nested(ExploreTabEntitySchema, many=True)
	group_type = fields.Str(validate=OneOf(['KEY_ALBUMS', 'NEW_RELEASE', 'TOP_ALBUMS', 'TOP_PLAYLISTS', 'TOP_SONGS']))
	kind = fields.Str(required=True, validate=Equal('sj#exEntityGroup'))
	start_position = fields.Int()
	title = fields.Str()


class ExploreTabSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'groups': [EXPLORE_TAB_ENTITY_GROUP],
			'kind': 'sj#exTab',
			'tab_type': 'tab_type'
		}
	"""

	groups = fields.Nested(ExploreTabEntityGroupSchema, many=True)
	kind = fields.Str(required=True, validate=Equal('sj#exTab'))
	tab_type = fields.Str(validate=OneOf(['GENRES', 'NEW_RELEASES', 'RECOMMENDED', 'TOP_CHARTS']))


class PlaylistEntrySchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'absolutePosition': 'absolutePosition',
			'clientId': 'clientId',
			'creationTimestamp': 'creationTimestamp',
			'deleted': False,
			'id': 'id',
			'kind': 'sj#playlistEntry',
			'lastModifiedTimestamp': 'lastModifiedTimestamp',
			'playlistId': 'playlistId',
			'track': STORE_TRACK,
			'trackId': 'trackId'
		}
	"""

	absolutePosition = fields.Str(required=True)
	clientId = fields.Str(required=True)
	creationTimestamp = fields.Str(required=True)
	deleted = fields.Bool(required=True)
	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#playlistEntry'))
	lastModifiedTimestamp = fields.Str(required=True)
	playlistId = fields.Str(required=True)
	track = fields.Nested(StoreTrackSchema)
	trackId = fields.Str(required=True)


class PodcastEpisodeSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'art': [IMAGE_REF],
			'author': 'author',
			'deleted': False,
			'description': 'description',
			'durationMillis': 'durationMillis',
			'episodeId': 'episodeId',
			'explicitType': 'explicitType',
			'fileSize': 'fileSize',
			'playbackPositionMillis': 'playbackPositionMillis',
			'publicationTimestampMillis': 'publicationTimestampMillis',
			'seriesId': 'seriesId',
			'seriesTitle': 'seriesTitle',
			'title': 'title'
		}
	"""

	art = fields.Nested(ImageRefSchema, many=True)
	author = fields.Str()
	deleted = fields.Bool()
	description = fields.Str()
	durationMillis = fields.Str(required=True)
	episodeId = fields.Str(required=True)
	explicitType = fields.Str(required=True)
	fileSize = fields.Str(required=True)
	playbackPositionMillis = fields.Str()
	publicationTimestampMillis = fields.Str()
	seriesId = fields.Str(required=True)
	seriesTitle = fields.Str(required=True)
	title = fields.Str(required=True)


class PodcastGenreSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'displayName': 'displayName',
			'id': 'id',
			'subgroups': []
		}
	"""

	displayName = fields.Str(required=True)
	id = fields.Str(required=True)
	subgroups = fields.Nested('self', many=True)


class PodcastSeriesUserPreferencesSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'autoDownload': False,
			'notifyOnNewEpisode': False,
			'subscribed': True
		}
	"""

	autoDownload = fields.Bool()
	notifyOnNewEpisode = fields.Bool()
	subscribed = fields.Bool(required=True)


class PodcastSeriesSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'art': [IMAGE_REF],
			'author': 'author',
			'continuationToken': 'continuationToken',
			'copyright': 'copyright',
			'description': 'description',
			'episodes': [PODCAST_EPISODE],
			'explicitType': 'explicitType',
			'link': 'link',
			'seriesId': 'seriesId',
			'title': 'title',
			'totalNumEpisodes': 42,
			'userPreferences': PODCAST_SERIES_USER_PREFERENCES
		}
	"""

	art = fields.Nested(ImageRefSchema, many=True)
	author = fields.Str(required=True)
	continuationToken = fields.Str()
	copyright = fields.Str()
	description = fields.Str()
	episodes = fields.Nested(PodcastEpisodeSchema, many=True)
	explicitType = fields.Str(required=True)
	link = fields.Str()
	seriesId = fields.Str(required=True)
	title = fields.Str(required=True)
	totalNumEpisodes = fields.Int(required=True)
	userPreferences = fields.Nested(PodcastSeriesUserPreferencesSchema)


class RadioSeedMetadataSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'artist': ARTIST,
			'genre': GENRE,
			'kind': 'sj#radioSeedMetadata',
			'track': STORE_TRACK
		}
	"""

	artist = fields.Nested(ArtistSchema)
	genre = fields.Nested(GenreSchema)
	kind = fields.Str(required=True, validate=Equal('sj#radioSeedMetadata'))
	track = fields.Nested(TrackSchema)


class RadioSeedSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'albumId': 'albumId',
			'artistId': 'artistId',
			'curatedStationId': 'curatedStationId',
			'genreId': 'genreId',
			'kind': 'sj#radioSeed',
			'metadataSeed': RADIO_SEED_METADATA,
			'seedType': 'seedType',
			'trackId': 'trackId',
			'trackLockerId': 'trackLockerId'
		}
	"""

	albumId = fields.Str()
	artistId = fields.Str()
	curatedStationId = fields.Str()
	genreId = fields.Str()
	kind = fields.Str(required=True, validate=Equal('sj#radioSeed'))
	metadataSeed = fields.Nested(RadioSeedMetadataSchema)
	seedType = fields.Str(required=True)
	trackId = fields.Str()
	trackLockerId = fields.Str()


class RadioStationSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'byline': 'byline',
			'clientId': 'clientId',
			'compositeArtRefs': [IMAGE_REF],
			'contentTypes': ['contentType'],
			'deleted': False,
			'description': 'description',
			'enforcementResult': False,
			'id': 'id',
			'imageUrl': 'imageUrl',
			'imageUrls': [IMAGE_REF],
			'inLibrary': True,
			'kind': 'sj#radioStation',
			'lastModifiedTimestamp': 'lastModifiedTimestamp',
			'name': 'name',
			'recentTimestamp': 'recentTimestamp',
			'seed': RADIO_SEED,
			'sessionToken': 'sessionToken',
			'skipEventHistory': [],
			'stationSeeds': [RADIO_SEED],
			'tracks': [STORE_TRACK]
		}
	"""

	adTargeting = fields.Nested(AdTargetingSchema)
	byline = fields.Str()
	clientId = fields.Str()
	compositeArtRefs = fields.Nested(ImageRefSchema, many=True)
	contentTypes = fields.List(fields.Str)
	deleted = fields.Bool()
	description = fields.Str()
	enforcementResult = fields.Bool()
	id = fields.Str()
	imageUrl = fields.Str()
	imageUrls = fields.Nested(ImageRefSchema, many=True)
	inLibrary = fields.Bool()
	kind = fields.Str(required=True, validate=Equal('sj#radioStation'))
	lastModifiedTimestamp = fields.Str()
	name = fields.Str()
	recentTimestamp = fields.Str()
	seed = fields.Nested(RadioSeedSchema)
	sessionToken = fields.Str()
	skipEventHistory = fields.List(fields.Field)  # TODO What's in this array?
	stationSeeds = fields.Nested(RadioSeedSchema, many=True)
	tracks = fields.Nested(TrackSchema, many=True)


class SharedPlaylistEntrySchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'absolutePosition': 'absolutePosition',
			'creationTimestamp': 'creationTimestamp',
			'deleted': False,
			'id': 'id',
			'kind': 'sj#playlistEntry',
			'lastModifiedTimestamp': 'lastModifiedTimestamp',
			'source': 'source',
			'track': STORE_TRACK,
			'trackId': 'trackId'
		}
	"""

	absolutePosition = fields.Str(required=True)
	creationTimestamp = fields.Str(required=True)
	deleted = fields.Bool(required=True)
	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#playlistEntry'))
	lastModifiedTimestamp = fields.Str(required=True)
	source = fields.Str()
	track = fields.Nested(StoreTrackSchema)
	trackId = fields.Str(required=True)


class SituationSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'description': 'description',
			'id': 'id',
			'imageUrl': 'imageUrl',
			'situations': [],
			'stations': [RADIO_STATION],
			'title': 'title',
			'wideImageUrl': 'wideImageUrl'
		}
	"""

	description = fields.Str(required=True)
	id = fields.Str(required=True)
	imageUrl = fields.Str()
	situations = fields.Nested('self', many=True)
	stations = fields.Nested(RadioStationSchema, many=True)
	title = fields.Str(required=True)
	wideImageUrl = fields.Str()


class StationCategorySchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'display_name': 'display_name',
			'id': 'id',
			'kind': 'sj#stationCategory',
			'subcategories': []
		}
	"""

	display_name = fields.Str(required=True)
	id = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#stationCategory'))
	subcategories = fields.Nested('self', many=True)


class TopChartSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'albums': [ALBUM],
			'kind': 'sj#topChart',
			'tracks': [STORE_TRACK]
		}
	"""

	albums = fields.Nested(AlbumSchema, required=True, many=True)
	kind = fields.Str(required=True, validate=Equal('sj#topChart'))
	tracks = fields.Nested(StoreTrackSchema, required=True, many=True)


class TopChartHeaderSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'header_image': IMAGE_REF,
			'kind': 'sj#topChartHeader'
		}
	"""

	header_image = fields.Nested(ImageRefSchema, required=True)
	kind = fields.Str(required=True, validate=Equal('sj#topChartHeader'))


class BrowseStationCategoriesSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'kind': 'sj#getStationCategoriesResponse',
			'root': STATION_CATEGORY
		}
	"""
	kind = fields.Str(required=True, validate=Equal('sj#getStationCategoriesResponse'))
	root = fields.Nested(StationCategorySchema, required=True)


class BrowseStationsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'kind': 'sj#getStationsResponse',
			'stations': [RADIO_STATION]
		}
	"""

	kind = fields.Str(required=True, validate=Equal('sj#getStationsResponse'))
	stations = fields.Nested(RadioStationSchema, required=True, many=True)


class BrowseTopChartSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'chart': TOP_CHART,
			'header': TOP_CHART_HEADER
		}
	"""

	chart = fields.Nested(TopChartSchema, required=True)
	header = fields.Nested(TopChartHeaderSchema, required=True)


class BrowseTopChartGenresSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'genres': [GENRE_REF]
		}
	"""

	genres = fields.Nested(GenreRefSchema, required=True, many=True)


class ConfigEntrySchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'key': 'key',
			'kind': 'sj#configEntry',
			'value': 'value'
		}
	"""

	key = fields.Str(required=True)
	kind = fields.Str(required=True, validate=Equal('sj#configEntry'))
	value = fields.Str(required=True)


class ConfigListEntriesSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'entries': [CONFIG_ENTRY]
		}
	"""

	entries = fields.Nested(ConfigEntrySchema, many=True)


class ConfigListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': CONFIG_LIST_ENTRIES,
			'kind': 'sj#configList'
		}
	"""

	data = fields.Nested(ConfigListEntriesSchema)
	kind = fields.Str(required=True, validate=Equal('sj#configList'))


class EphemeralTopItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items' = [STORE_TRACKS]
		}
	"""

	items = fields.Nested(StoreTrackSchema, many=True)


class EphemeralTopSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': EPHEMERAL_TOP_ITEMS,
			'kind': 'sj#trackList',
			'nextPageToken': 'nextPageToken'
		}
	"""

	data = fields.Nested(EphemeralTopItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#trackList'))
	nextPageToken = fields.Str()


class ExploreTabsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'kind': 'sj#exGetTabsResponse',
			'tabs': [EXPLORE_TAB]
		}
	"""

	kind = fields.Str(required=True, validate=Equal('sj#exGetTabsResponse'))
	tabs = fields.Nested(ExploreTabSchema, many=True)


class GenreListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'genres': [GENRE],
			'kind': 'sj#exGetMusicGenresResponse'
		}
	"""

	genres = fields.Nested(GenreSchema, many=True)
	kind = fields.Str(required=True, validate=Equal('sj#exGetMusicGenresResponse'))


class IsPlaylistSharedSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'is_shared': True
		}
	"""

	is_shared = fields.Bool(required=True)


class ListenNowAlbumIDSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'artist': 'artist',
			'metajamCompactKey': 'metajamCompactKey',
			'title': 'title'
		}
	"""

	artist = fields.Str(required=True)
	metajamCompactKey = fields.Str(required=True)
	title = fields.Str(required=True)


class ListenNowAlbumSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'artist_metajam_id': 'artist_metajam_id',
			'artist_name': 'artist_name',
			'artist_profile_image': ART_REF,
			'description': 'description',
			'description_attribution': ATTRIBUTION,
			'explicitType': 'explicitType',
			'id': LISTEN_NOW_ALBUM_ID,
			'title': 'title'
		}
	"""

	artist_metajam_id = fields.Str(required=True)
	artist_name = fields.Str(required=True)
	artist_profile_image = fields.Nested(ArtRefSchema, required=True)
	description = fields.Str(required=True)
	description_attribution = fields.Nested(AttributionSchema)
	explicitType = fields.Str()
	id = fields.Nested(ListenNowAlbumIDSchema, required=True)
	title = fields.Str(required=True)


class ListenNowDismissedItemSchema(MobileClientSchema):
	dismissalTimestamp = fields.Str(required=True)
	item_id = fields.Dict()  # TODO: Find all version of this. Know to have 'type' field and can have an 'album_id' dict.
	kind = fields.Str(required=True, validate=Equal('sj#dismissedItem'))
	suggestion_reason = fields.Str(required=True)
	uuid = fields.UUID(required=True)


class ListenNowDismissedItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'kind': 'sj#listenNowDismissedItemList',
			'minLastModifiedIgnored': True
		}
	"""

	kind = fields.Str(required=True, validate=Equal('sj#listenNowDismissedItemList'))
	minLastModifiedIgnored = fields.Bool()


class ListenNowRadioStationIDSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'seeds': [RADIO_SEED]
		}
	"""

	seeds = fields.Nested(RadioSeedSchema, many=True)


class ListenNowRadioStationSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'highlight_color': 'highlight_color',
			'id': LISTEN_NOW_RADIO_STATION_ID,
			'profile_image': ART_REF,
			'title': 'title'
		}
	"""

	highlight_color = fields.Str()
	id = fields.Nested(ListenNowRadioStationIDSchema, required=True)
	profile_image = fields.Nested(ArtRefSchema)
	title = fields.Str(required=True)


class ListenNowItemSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'album': LISTEN_NOW_ALBUM,
			'compositeArtRefs': [IMAGE_REF],
			'images': [IMAGE_REF],
			'kind': 'sj#listennowitem',
			'radio_station': LISTEN_NOW_RADIO_STATION,
			'suggestion_reason': 'suggestion_reason',
			'suggestion_text': 'suggestion_text',
			'type': 'type'
		}
	"""

	album = fields.Nested(ListenNowAlbumSchema)
	compositeArtRefs = fields.Nested(ImageRefSchema, many=True)
	images = fields.Nested(ImageRefSchema, many=True)
	kind = fields.Str(required=True, validate=Equal('sj#listennowitem'))
	radio_station = fields.Nested(ListenNowRadioStationSchema)
	suggestion_reason = fields.Str(required=True)
	suggestion_text = fields.Str(required=True)
	type = fields.Str(required=True)


class ListenNowItemListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'kind': 'sj#listenNowItemList',
			'listennow_items': [LISTEN_NOW_ITEM]
		}
	"""

	kind = fields.Str(required=True, validate=Equal('sj#listenNowItemList'))
	listennow_items = fields.Nested(ListenNowItemSchema, many=True)


class ListenNowSituationListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'distilledContextWrapper': DISTILLED_CONTEXT_WRAPPER,
			'primaryHeader': 'primaryHeader',
			'situations': [SITUATION],
			'subHeader': 'subHeader'
		}
	"""

	distilledContextWrapper = fields.Nested(DistilledContextWrapperSchema)
	primaryHeader = fields.Str(required=True)
	situations = fields.Nested(SituationSchema, many=True)
	subHeader = fields.Str(required=True)


class PlaylistEntryItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items': [PLAYLIST_ENTRY]
		}
	"""

	items = fields.Nested(PlaylistEntrySchema, many=True)


class PlaylistEntryListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': PLAYLIST_ENTRY_ITEMS,
			'kind': 'sj#playlistEntryList',
			'nextPageToken': 'nextPageToken'
		}
	"""

	data = fields.Nested(PlaylistEntryItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#playlistEntryList'))
	nextPageToken = fields.Str()


class PlaylistListItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items': [PLAYLIST]
		}
	"""

	items = fields.Nested(PlaylistSchema, many=True)


class PlaylistListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': PLAYLIST_LIST_ITEMS,
			'kind': 'sj#playlistList',
			'nextPageToken': 'nextPageToken'
		}
	"""

	data = fields.Nested(PlaylistListItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#playlistList'))
	nextPageToken = fields.Str()


class PodcastBrowseSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'series': [PODCAST_SERIES]
		}
	"""

	series = fields.Nested(PodcastSeriesSchema, required=True, many=True)


class PodcastBrowseHierarchySchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'groups': [PODCAST_GENRE]
		}
	"""

	groups = fields.Nested(PodcastGenreSchema, required=True, many=True)


class PodcastEpisodeListItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items': [PODCAST_EPISODE]
		}
	"""

	items = fields.Nested(PodcastEpisodeSchema, many=True)


class PodcastEpisodeListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': PODCAST_EPISODE_LIST_ITEMS,
			'kind': 'sj#podcastEpisodeList',
			'nextPageToken': 'nextPageToken'
		}
	"""

	data = fields.Nested(PodcastEpisodeListItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#podcastEpisodeList'))
	nextPageToken = fields.Str()


class PodcastSeriesListItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items': [PODCAST_SERIES]
		}
	"""

	items = fields.Nested(PodcastSeriesSchema, many=True)


class PodcastSeriesListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': PODCAST_SERIES_LIST_ITEMS,
			'kind': 'sj#podcastSeriesList',
			'nextPageToken': 'nextPageToken'
		}
	"""

	data = fields.Nested(PodcastSeriesListItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#podcastSeriesList'))
	nextPageToken = fields.Str()


class RadioConstraintsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'kind': 'sj#radioConstraints',
			'prefetchLeadTimeMillis': 'prefetchLeadTimeMillis',
			'prefetchesAllowed': 1,
			'skipEnforcementPeriodMillis': 'skipEnforcementPeriodMillis',
			'skipsAllowed': 6
		}
	"""


class RadioFeedItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'currentTimestampMillis': 'currentTimestampMillis',
			'radioConstraints': RADIO_CONSTRAINTS
			'stations': [RADIO_STATION],
		}
	"""

	currentTimestampMillis = fields.Str(required=True)
	radioConstraints = fields.Nested(RadioConstraintsSchema)
	stations = fields.Nested(RadioStationSchema, many=True)


class RadioFeedSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': RADIO_FEED_ITEMS,
			'kind': 'sj#radioFeed'
		}
	"""

	data = fields.Nested(RadioFeedItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#radioFeed'))


class RadioListItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items': [RADIO_STATION]
		}
	"""

	items = fields.Nested(RadioStationSchema, many=True)


class RadioListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': RADIO_LIST_ITEMS,
			'kind': 'sj#radioList',
			'nextPageToken': 'nextPageToken'
		}
	"""

	data = fields.Nested(RadioListItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#radioList'))
	nextPageToken = fields.Str()


class SearchResultVideoSchema(VideoSchema):
	"""

	**Validates**::

		SEARCH_RESULT_VIDEO = {
			'id': 'id',
			'kind': 'sj#video',
			'thumbnails': [VIDEO_THUMBNAIL],
			'title': 'title'
		}
	"""

	title = fields.Str(required=True)


class SearchResultClusterInfoSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'category': 'category',
			'id': 'id',
			'type': 'type'
		}
	"""

	category = fields.Str(required=True)
	id = fields.Str(required=True)
	type = fields.Str(required=True)


class SearchResultSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'album': ALBUM,
			'artist': ARTIST,
			'best_result': False,
			'navigational_confidence': 42,
			'navigational_result': False,
			'playlist': {k: v for k, v in PLAYLIST.items() if k not in ['creationTimestamp', 'id', 'lastModifiedTimestamp']},
			'score': 42,
			'series': PODCAST_SERIES,
			'situation': SITUATION,
			'station': RADIO_STATION,
			'track': STORE_TRACK,
			'type': 'type',
			'youtube_video': SEARCH_RESULT_VIDEO
		}
	"""

	album = fields.Nested(AlbumSchema)
	artist = fields.Nested(ArtistSchema)
	best_result = fields.Bool()
	cluster = fields.Nested(SearchResultClusterInfoSchema, many=True)
	navigational_confidence = fields.Number()
	navigational_result = fields.Bool()
	playlist = fields.Nested(PlaylistSchema(exclude=['creationTimestamp', 'id', 'lastModifiedTimestamp']))
	score = fields.Number()
	series = fields.Nested(PodcastSeriesSchema)
	situation = fields.Nested(SituationSchema)
	station = fields.Nested(RadioStationSchema)
	track = fields.Nested(StoreTrackSchema)
	type = fields.Str(required=True)
	youtube_video = fields.Nested(SearchResultVideoSchema)


class SearchResultClusterSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'cluster': {SEARCH_RESULT_CLUSTER_INFO},
			'entries': [SEARCH_RESULT],
			'resultToken': 'resultToken'
		}

	"""

	cluster = fields.Nested(SearchResultClusterInfoSchema, required=True)
	displayName = fields.Str()
	entries = fields.Nested(SearchResultSchema, many=True)
	resultToken = fields.Str(required=True)


class SearchResponseSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'clusterDetail': [SEARCH_RESULT_CLUSTER],
			'kind': 'sj#searchresponse'
		}
	"""

	clusterDetail = fields.Nested(SearchResultClusterSchema, many=True)
	kind = fields.Str(required=True, validate=Equal('sj#searchresponse'))


class SearchSuggestedQuerySchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'suggestionCategory': 'suggestionCategory',
			'suggestion_string': 'suggestion_string',
			'type': 'type'
		}
	"""

	suggestionCategory = fields.Str(required=True)
	suggestion_string = fields.Str(required=True)
	type = fields.Str(required=True)


class SearchSuggestionSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'suggested_queries': [SEARCH_SUGGESTED_QUERY]
		}
	"""

	suggested_queries = fields.Nested(SearchSuggestedQuerySchema, many=True)


class SharedPlaylistEntryItemSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'playlistEntry': SHARED_PLAYLIST_ENTRY,
			'responseCode': 'responseCode',
			'shareToken': 'shareToken'
		}
	"""

	playlistEntry = fields.Nested(SharedPlaylistEntrySchema)
	responseCode = fields.Str(required=True)
	shareToken = fields.Str(required=True)


class SharedPlaylistEntryListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'entries': [SHARED_PLAYLIST_ENTRY_ITEM],
			'kind': 'sj#listSharedPlaylistEntriesResponse'
		}
	"""

	entries = fields.Nested(SharedPlaylistEntryItemSchema, many=True)
	kind = fields.Str(required=True, validate=Equal('sj#listSharedPlaylistEntriesResponse'))


class TrackBatchItemSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'client_id': 'client_id',
			'id': 'id',
			'response_code': 'response_code'
		}
	"""

	client_id = fields.Str()
	id = fields.Str()
	response_code = fields.Str(required=True)


class TrackBatchSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'mutate_response': [TRACK_BATCH_ITEMS]
		}
	"""

	mutate_response = fields.Nested(TrackBatchItemSchema, many=True)


class TrackListItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items': [STORE_TRACK, UPLOADED_TRACK]
		}
	"""

	items = fields.Nested(TrackSchema, many=True)


class TrackListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': TRACK_LIST_ITEMS,
			'kind': 'sj#trackList',
			'nextPageToken': 'nextPageToken'
		}
	"""

	data = fields.Nested(TrackListItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#trackList'))
	nextPageToken = fields.Str()


class UserClientIDListItemsSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'items': [DEVICE_MANAGEMENT_INFO]
		}
	"""

	items = fields.Nested(DeviceManagementInfoSchema, many=True)


class UserClientIDListSchema(MobileClientSchema):
	"""

	**Validates**::

		{
			'data': USER_CLIENT_ID_LIST_ITEMS,
			'kind': 'sj#userClientIdList'
		}
	"""

	data = fields.Nested(UserClientIDListItemsSchema)
	kind = fields.Str(required=True, validate=Equal('sj#userClientIdList'))
