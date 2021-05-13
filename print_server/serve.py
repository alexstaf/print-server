#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Print server."""


import argparse
from io import BytesIO

from PIL import Image
from waitress import serve
from flask import Flask, render_template, request, send_from_directory

from .printer import Printer


printer = Printer()
app = Flask(__name__)


@app.route('/')
def index():
    """Route index page."""
    return render_template('index.html', message='Hello, World!')


@app.route('/upload', methods=['POST'])
def upload():
    """Route upload page."""
    byte_strings = []
    for part in request.files['image']:
        byte_strings.append(part)
    byte_string = b''.join(byte_strings)
    with BytesIO(byte_string) as b:
        image = Image.open(b)
        image.load()
    printer.print(image, request.files['image'].filename)
    return 'OK'


@app.route('/assets/<path:path>')
def send_assets(path):
    """Route assets."""
    return send_from_directory('assets', path)


def parse_args():
    """Create and parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.

    """
    parser = argparse.ArgumentParser(
        description=__doc__, add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-a', '--address', default='0.0.0.0',
                        help='Set address to use.')
    parser.add_argument('-p', '--port', type=int, default=8000,
                        help='Set server port.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Set debug mode.')

    args = parser.parse_args()
    return args


def main():
    """Application entry point."""
    args = parse_args()
    serve(app, host=args.address, port=args.port)


if __name__ == '__main__':
    main()
