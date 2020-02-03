from pathlib import Path

import pytest
from google_music_proto.musicmanager.utils import (
	generate_client_id,
	get_album_art,
)

TEST_FILES_PATH = Path(__file__).parent / 'files'
TEST_FLAC = TEST_FILES_PATH / 'test.flac'
TEST_MP3_ID3V1 = TEST_FILES_PATH / 'test-id3v1.mp3'
TEST_MP3_ID3V2 = TEST_FILES_PATH / 'test-id3v2.mp3'
TEST_WAV = TEST_FILES_PATH / 'test.wav'


@pytest.mark.parametrize(
	'song,expected',
	[
		(
			TEST_FLAC,
			'mxvofGtXn94jQVFfTYLACA',
		),
		(
			TEST_MP3_ID3V1,
			'sFbjnunOBS+hwjB0UQXCvQ',
		),
		(
			TEST_MP3_ID3V2,
			'sFbjnunOBS+hwjB0UQXCvQ',
		),
		(
			TEST_WAV,
			'AaaDJcxutpaqPAmqSZg4gg',
		),
	],
)
def test_generate_client_id(song, expected):
	assert generate_client_id(song) == expected


def test_get_album_art():
	assert get_album_art(TEST_MP3_ID3V1) is None
	assert get_album_art(TEST_WAV) is None

	assert get_album_art(
		TEST_FLAC
	) == get_album_art(
		TEST_MP3_ID3V2
	) == get_album_art(
		TEST_FILES_PATH / 'test-back-cover.mp3'
	) == get_album_art(
		TEST_FILES_PATH / 'test-other.mp3'
	) == get_album_art(
		TEST_FILES_PATH / 'test-back-cover-other.mp3'
	) == get_album_art(
		TEST_FILES_PATH / 'test-other-back-cover.mp3'
	) == get_album_art(
		TEST_FILES_PATH / 'test-back-cover-other-front-cover.mp3'
	) == get_album_art(
		TEST_FILES_PATH / 'test-front-cover-front-cover.mp3'
	) == (
		b'\x89PNG\r\n\x1a\n\x00\x00\x00\r'
		b'IHDR\x00\x00\x00\x10\x00\x00\x00'
		b'\x10\x08\x06\x00\x00\x00\x1f\xf3'
		b'\xffa\x00\x00\x00\tpHYs\x00\x00\x0b'
		b'\x12\x00\x00\x0b\x12\x01\xd2\xdd~'
		b'\xfc\x00\x00\x00\x12IDAT8\xcbc`\x18'
		b'\x05\xa3`\x14\x8c\x02\x08\x00\x00\x04'
		b'\x10\x00\x01\x85?\xaar\x00\x00\x00'
		b'\x00IEND\xaeB`\x82'
	)
