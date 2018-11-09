# Change Log

Notable changes to this project based on the [Keep a Changelog](https://keepachangelog.com) format.
This project adheres to [Semantic Versioning](https://semver.org).


## [Unreleased](https://github.com/thebigmunch/google-music-proto/tree/master)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.0.0...master)

### Added

* ``PlaylistEntriesBatch``

### Fixed

* ``PlaylistEntriesShared``



## [2.0.0](https://github.com/thebigmunch/google-music-proto/releases/tag/2.0.0) (2018-11-05)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/1.3.0...2.0.0)

### Added

* Expose undocumented batch call base classes:
	* ``ActivityRecord``
	* ``PlaylistBatch``
	* ``RadioEditStation``
	* ``TrackBatch``

### Changed

* Batch calls now use staticmethods to build the events/mutations.
  See the docs for each call's methods.
  The events/mutations are passed to the batch call class.
  This allows for multiple and different types of and operations to be done in one call.

### Removed

* Batch call subclasses:
	* ``ActivityRecordPlay``
	* ``ActivityRecordRate``
	* ``PlaylistBatchCreate``
	* ``PlaylistBatchDelete``
	* ``PlaylistBatchUpdate``
	* ``RadioEditStationCreateOrGet``
	* ``RadioEditStationDelete``
	* ``TrackBatchCreate``
	* ``TrackBatchDelete``
	* ``TrackBatchUpdate``


## [1.3.0](https://github.com/thebigmunch/google-music-proto/releases/tag/1.2.0) (2018-10-25)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/1.2.0...1.3.0)

### Added

* Support for I'm Feeling Lucky Radio by ``station_id`` set to ``'IFL'``.
* ``PlaylistsDelete``


## [1.2.0](https://github.com/thebigmunch/google-music-proto/releases/tag/1.2.0) (2018-10-23)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/1.1.0...1.2.0)

### Added

* ``ListenNowItemType``

### Changed

* Update ``SearchResultSchema`` for new response format.

### Fixed

* Fix default for ``numEntries`` in ``RadioStationFeed``.
* Fix ``tz_offset`` default in ``LibraryNowSituations``.


## [1.1.0](https://github.com/thebigmunch/google-music-proto/releases/tag/1.1.0) (2018-10-20)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/1.0.0...1.1.0)

### Added

* Add ActivityRecordPlay call for incrementing play counts.


## [1.0.0](https://github.com/thebigmunch/google-music-proto/releases/tag/1.0.0) (2018-10-19)

[Commits](https://github.com/thebigmunch/google-music-proto/commit/eeb3c159d131b1d8f28ee92ac9acd464ff67818d)

* Initial release.
