__all__ = [
	'generate_client_id', 'get_album_art', 'get_transcoder', 'transcode_to_mp3'
]

import os
import shutil
import subprocess
from base64 import b64encode
from binascii import unhexlify
from hashlib import md5

import audio_metadata


# The id is found by: getting md5sum of audio, base64 encode md5sum, removing trailing '='.
def generate_client_id(song):
	if not isinstance(song, audio_metadata.Format):
		song = audio_metadata.load(song)

	md5sum = None
	if isinstance(song, audio_metadata.FLAC):
		md5sum = unhexlify(song.streaminfo.md5)
	else:
		m = md5()
		with open(song.filepath, 'rb') as f:
			f.seek(song.streaminfo._start)
			m.update(f.read(song.streaminfo._size))  # TODO: Speed up by reading in chunks

		md5sum = m.digest()

	client_id = b64encode(md5sum).rstrip(b'=')

	return client_id


def get_album_art(song):
	if not isinstance(song, audio_metadata.Format):
		song = audio_metadata.load(song)

	album_art = next((picture.data for picture in song.pictures if picture.type == 3), None)

	return album_art


def get_transcoder():
	"""Return the path to a transcoder (ffmpeg or avconv) with MP3 support."""

	transcoders = ['ffmpeg', 'avconv']
	transcoder_details = {}

	for transcoder in transcoders:
		command_path = shutil.which(transcoder)
		if command_path is None:
			transcoder_details[transcoder] = 'Not installed.'
			continue

		stdout = subprocess.run([command_path, '-codecs'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True).stdout
		mp3_encoding_support = ('libmp3lame' in stdout and 'disable-libmp3lame' not in stdout)
		if mp3_encoding_support:
			transcoder_details[transcoder] = "MP3 encoding support."
			break
		else:
			transcoder_details[transcoder] = "No MP3 encoding support."
	else:
		raise ValueError(
			f"ffmpeg or avconv must be in the path and support mp3 encoding."
			"\nDetails: {transcoder_details}"
		)

	return command_path


def _transcode(command, input_=None):
	try:
		transcode = subprocess.run(command, input=input_, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
		if hasattr(song.filepath, 'read'):
			raise ValueError("Audio metadata must be from a file.")
			# command = [command_path, '-i', '-']
			# input_ = song.filepath.read()
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
		raise ValueError("'song' must be os.PathLike, filepath string, a file/bytes-like object, or binary data.")

	if slice_duration is not None:
		command.extend(['-t', str(slice_duration)])
	if slice_start is not None:
		command.extend(['-ss', str(slice_start)])

	command.extend(['-q:a', str(quality)])

	# Use 's16le' to not output id3 headers.
	command.extend(['-f', 's16le', '-c', 'libmp3lame', '-'])

	return _transcode(command, input_=input_)
