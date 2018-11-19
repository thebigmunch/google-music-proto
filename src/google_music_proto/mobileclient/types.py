__all__ = ['ListenNowItemType', 'QueryResultType', 'StationSeedType', 'TrackRating']

from enum import Enum, unique


class _BaseEnum(Enum):
	def __repr__(self):
		return f'<{self.__class__.__name__}.{self.name}>'


@unique
class ListenNowItemType(_BaseEnum):
	"""Listen Now item type."""

	album = '1'
	station = '3'


@unique
class QueryResultType(_BaseEnum):
	"""Search result types.

	::

		search_result['type']
	"""

	song = '1'
	artist = '2'
	album = '3'
	playlist = '4'
	genre = '5'
	station = '6'
	situation = '7'
	video = '8'
	podcast = '9'


@unique
class StationSeedType(_BaseEnum):
	"""Station seed types.

	::

		station['seed']['seedType']
	"""

	library_track = '1'
	store_track = '2'
	artist_related = '3'
	album = '4'
	genre = '5'
	ifl = '6'
	artist_only = '7'
	playlist = '8'
	curated_station = '9'


@unique
class TrackRating(_BaseEnum):
	"""Track ratings.

	::

		song['rating']
	"""

	NOT_RATED = '0'
	ONE_STAR = '1'
	FIVE_STARS = '5'
