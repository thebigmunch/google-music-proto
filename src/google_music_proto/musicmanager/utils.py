__all__ = [
	'generate_client_id',
	'get_album_art',
	'get_transcoder',
	'transcode_to_mp3',
]

import os
import shutil
import subprocess
from base64 import b64encode
from binascii import unhexlify
from hashlib import md5

import audio_metadata
from tbm_utils import DataReader


# The id is found by getting md5sum of audio, base64 encode md5sum, removing trailing '=', except for FLAC.
# FLAC: Unhexlify md5sum from stream info block.
# MP3: Audio starts right after ID3v2 tag if present, else beginning of file.
# MP3: Audio ends right before ID3v1 tag if present, else end of file.
# MP4: Audio is the entire 'mdat' atom.
# Ogg Vorbis: For some reason, Google seems to use the start of the 2nd audio page for client ID generation.
# Ogg Vorbis: This could actually just be an off-by-one error in their code.
def generate_client_id(song):
	def _hash_data(m, f, audio_size):
		# Speed up by reading in chunks
		read = 0
		read_size = min(audio_size - read, 65536)
		while read_size > 0:
			data = f.read(read_size)
			m.update(data)

			read += read_size
			read_size = min(audio_size - read, 65536)

		return m.digest()

	if not isinstance(song, audio_metadata.Format):  # pragma: nobranch
		song = audio_metadata.load(song)

	md5sum = None
	if isinstance(song, audio_metadata.FLAC):
		md5sum = unhexlify(song.streaminfo.md5)
	else:
		m = md5()
		if isinstance(song, audio_metadata.MP3):
			if '_id3' in song and isinstance(song._id3, audio_metadata.ID3v2):
				audio_start = song._id3._size
			else:
				audio_start = 0

			audio_size = song.streaminfo._end - audio_start
			with open(song.filepath, 'rb') as f:
				f.seek(audio_start, os.SEEK_SET)
				md5sum = _hash_data(m, f, audio_size)
		elif isinstance(song, audio_metadata.OggVorbis):
			f = DataReader(song.filepath)
			f.seek(song.streaminfo._start)

			while True:
				page = audio_metadata.OggPage.load(f)
				if page.position:
					break

			audio_start = f.tell()
			audio_size = song.streaminfo._size
			md5sum = _hash_data(m, f, audio_size)
		else:
			audio_size = song.streaminfo._size
			with open(song.filepath, 'rb') as f:
				f.seek(song.streaminfo._start)
				md5sum = _hash_data(m, f, audio_size)

	client_id = b64encode(md5sum).rstrip(b'=').decode('ascii')

	return client_id


def get_album_art(song):
	if not isinstance(song, audio_metadata.Format):  # pragma: nobranch
		song = audio_metadata.load(song)

	# Google's Music manager uses this album art selection algorithm:
	# * If picture(s) of type 'front cover' are found, use the first one of those in the list.
	# * If picture(s) of type 'other' are found, use the first one of those in the list.
	# * If picture(s) of type 'back cover' are found, use the first one of those in the list.
	for picture_type in [3, 0, 4]:
		album_art = next(
			(
				picture.data
				for picture in song.pictures
				if picture.type == picture_type
			),
			None
		)

		if album_art is not None:
			break

	return album_art


def get_transcoder(*, path=None):
	"""Return the path to a transcoder (ffmpeg or avconv) with MP3 support."""

	transcoders = ['ffmpeg', 'avconv']
	transcoder_details = {}

	for transcoder in transcoders:
		command_path = shutil.which(transcoder, path=path)
		if command_path is None:
			transcoder_details[transcoder] = 'Not installed.'
			continue

		stdout = subprocess.run(
			[command_path, '-codecs'],
			stdout=subprocess.PIPE,
			stderr=subprocess.DEVNULL,
			universal_newlines=True,
		).stdout

		mp3_encoding_support = (
			'libmp3lame' in stdout
			and 'disable-libmp3lame' not in stdout
		)

		if mp3_encoding_support:
			break
		else:
			transcoder_details[transcoder] = "No MP3 encoding support."
	else:
		raise ValueError(
			f"ffmpeg or avconv must be in the path and support mp3 encoding."
			f"\nDetails: {transcoder_details}"
		)

	return command_path


def _transcode(command, input_=None):
	try:
		transcode = subprocess.run(
			command,
			input=input_,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)

		transcode.check_returncode()
	except (OSError, subprocess.CalledProcessError) as e:
		error_msg = f"Transcode command '{' '.join(command)}' failed: {e}. "

		if 'No such file or directory' in str(e):
			error_msg += '\nffmpeg or avconv must be installed PATH.'

		if transcode.stderr is not None:
			error_msg += f"\nstderr: '{transcode.stderr}'"

		e.message = error_msg

		raise
	else:
		return transcode.stdout


def transcode_to_mp3(song, *, slice_start=None, slice_duration=None, quality='320k'):
	command_path = get_transcoder()
	input_ = None

	if isinstance(song, audio_metadata.Format):
		if song.filepath is None:
			raise ValueError("Audio metadata must be from a file.")
		else:
			command = [command_path, '-i', song.filepath]
	elif isinstance(song, bytes):
		command = [command_path, '-i', '-']
		input_ = song
	elif isinstance(song, str):
		command = [command_path, '-i', song]
	elif isinstance(song, os.PathLike):
		command = [command_path, '-i', song.__fspath__()]
	else:
		raise ValueError(
			"'song' must be os.PathLike, filepath string, a file/bytes-like object, or binary data."
		)

	if slice_duration is not None:
		command.extend(['-t', str(slice_duration)])
	if slice_start is not None:
		command.extend(['-ss', str(slice_start)])

	if isinstance(quality, int):
		command.extend(['-q:a', str(quality)])
	elif isinstance(quality, str):
		command.extend(['-b:a', str(quality)])

	# Use 's16le' to not output id3 headers.
	command.extend(['-f', 's16le', '-c', 'libmp3lame', '-'])

	return _transcode(command, input_=input_)
