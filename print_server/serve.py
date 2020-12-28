#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Print server."""


import argparse

from flask import Flask, render_template, request, send_from_directory


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', message='Hello, World!')


@app.route('/assets/<path:path>')
def send_assets(path):
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
    parser.add_argument('-p', '--port', type=int, default=8000,
                        help='Set server port.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Set debug mode.')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    app.run(host='127.0.0.1', port=args.port, debug=True)
