import json
import subprocess
from ._run import Error
from ._utils import convert_kwargs_to_cmd_line_args


def probe(filename, cmd='ffprobe', timeout=None, **kwargs):
    """Run ffprobe on the specified file and return a JSON representation of the output.

    Raises:
        :class:`ffmpeg.Error`: if ffprobe returns a non-zero exit code,
            an :class:`Error` is returned with a generic error message.
            The stderr output can be retrieved by accessing the
            ``stderr`` property of the exception.
    """
    args = [cmd, '-show_format', '-show_streams', '-of', 'json']
    args += convert_kwargs_to_cmd_line_args(kwargs)
    args += [filename]

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    communicate_kwargs = {}
    if timeout is not None:
        communicate_kwargs['timeout'] = timeout
    out, err = p.communicate(**communicate_kwargs)
    if p.returncode != 0:
        raise Error('ffprobe', out, err)
    return json.loads(out.decode('utf-8'))

def probe_key_frames(filename, cmd='ffprobe', **kwargs):
    """Run this ffprobe on the specified file with key frame options and return a csv representation of the key frames.

    Raises:
        :class:`ffmpeg.Error`: if ffprobe returns a non-zero exit code,
            an :class:`Error` is returned with a generic error message.
            The stderr output can be retrieved by accessing the
            ``stderr`` property of the exception.
    """
    args = [cmd, '-show_format', '-show_streams', '-of', 'csv']
    args += convert_kwargs_to_cmd_line_args(kwargs)
    args += [filename]

    p1 = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep','-n','I'], stdin=p1.stdout ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p2.communicate()
    if p2.returncode != 0:
        raise Error('ffprobe', out, err)
    return [int(x.split(':')[0]) for x in out.decode('utf-8').splitlines()]


__all__ = ['probe']
