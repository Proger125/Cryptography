import argparse

from src.api import NotepadApi
from src.managers import FileManager, SessionManager


def start_notepad_server(host, port):
    server = NotepadApi(
        fm_cls=FileManager,
        sm_cls=SessionManager,
    )
    server.run(host, port)


def main(args):
    if args.type == 'notepad':
        start_notepad_server(args.address, args.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        dest='address',
        default='127.0.0.1',
        help='Server address',
    )
    parser.add_argument(
        '-p',
        dest='port',
        default=9203,
        help='Server port',
        type=int,
    )
    parser.add_argument(
        '-t',
        dest='type',
        default='notepad',
        choices=['notepad', 'mitm'],
        help='Server type (default=notepad, mitm)',
    )
    main(parser.parse_args())
