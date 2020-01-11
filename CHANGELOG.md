# Change Log

Notable changes to this project based on the [Keep a Changelog](https://keepachangelog.com) format.
This project adheres to [Semantic Versioning](https://semver.org).


## [Unreleased](https://github.com/thebigmunch/google-music-proto/tree/master)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.5.2...master)


## [2.5.2](https://github.com/thebigmunch/google-music-proto/releases/tag/2.5.2) (2020-01-11)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.5.1...2.5.2)

### Changed

* Decode stream call ``sig`` param to str.
	HTTP client libraries don't necessarily support bytes param values.


### Fixed

* Param name for ``MobileClientStreamCall``.
* Use correct param name for streaming podcast episodes.


## [2.5.1](https://github.com/thebigmunch/google-music-proto/releases/tag/2.5.1) (2019-10-18)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.5.0...2.5.1)

### Fixed

* Use try/except for track/disc number conversions.
* Add check for files above maximum allowed upload size.
* Properly calculate client ID for MP3s that don't
  have an MPEG frame at the start of the file or
	immediately following an ID3v2 tag.


## [2.5.0](https://github.com/thebigmunch/google-music-proto/releases/tag/2.5.0) (2019-07-22)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.4.0...2.5.0)

### Added

* Ability to subscribe to public playlists using
	``PlaylistBatch`` with ``PlaylistBatch.create``.
	Unsubscribing is the same as deleting a user playlist.

### Fixed

* Handle unsupported and invalid dates when getting track info.


## [2.4.0](https://github.com/thebigmunch/google-music-proto/releases/tag/2.4.0) (2019-02-01)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.3.0...2.4.0)

### Changed

* Return ``str`` instead of ``bytes`` from ``generate_client_id``.

### Removed

* Workaround to support ``TDRC`` ID3v2.4 frame for year.


## [2.3.0](https://github.com/thebigmunch/google-music-proto/releases/tag/2.3.0) (2019-01-26)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.2.0...2.3.0)

### Added

* Workaround to support ``TDRC`` ID3v2.4 frame for year.


## [2.2.0](https://github.com/thebigmunch/google-music-proto/releases/tag/2.2.0) (2019-01-15)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.1.2...2.2.0)

### Added

* ``no_sample`` parameter to ``Sample.generate_sample`` for
	sending empty audio sample to avoid ffmpeg/avconv dependency.

### Fixed

* Handle float values for beats per minute.


## [2.1.2](https://github.com/thebigmunch/google-music-proto/releases/tag/2.1.2) (2018-11-30)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.1.1...2.1.2)

### Fixed

* Spoof WAV file content type in ``Metadata.get_track_info``.
* Transcode quality option selection.


## [2.1.1](https://github.com/thebigmunch/google-music-proto/releases/tag/2.1.1) (2018-11-24)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.1.0...2.1.1)

### Fixed

* Incorrect response type for ``UpAuth``.


## [2.1.0](https://github.com/thebigmunch/google-music-proto/releases/tag/2.1.0) (2018-11-24)

[Commits](https://github.com/thebigmunch/google-music-proto/compare/2.0.0...2.1.0)

### Added

* ``PlaylistEntriesBatch``

### Changed

* Mobile client types enums to use string values instead of integers.

### Fixed

* ``PlaylistEntriesShared``
* Misnamed ``check_success`` method for ``UpAuth``.
* Raise an exception if ``check_success`` fails.


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
