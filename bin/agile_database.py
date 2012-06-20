import argparse, signal, sys

from mysql.baseline import baseline
from mysql.patch import patch
from mysql.rollback import rollback

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def parse_arguments():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='commands', dest='command')

    baseline_parser = subparsers.add_parser('baseline', help='Baseline database')
    baseline_parser.add_argument('env', action='store', help='Database environment')
    baseline_parser.add_argument('base_dir', action='store', help='Script base dir')

    patch_parser = subparsers.add_parser('patch', help='Patch database')
    patch_parser.add_argument('env', action='store', help='Database environment')
    patch_parser.add_argument('base_dir', action='store', help='Script base dir')

    rollback_parser = subparsers.add_parser('rollback', help='Rollback database')
    rollback_parser.add_argument('env', action='store', help='Database environment')
    rollback_parser.add_argument('base_dir', action='store', help='Script base dir')

    args = parser.parse_args()

    if args.command == 'baseline':
        baseline(args.env, args.base_dir)
    elif args.command == 'patch':
        patch(args.env, args.base_dir)
    elif args.command == 'rollback':
        rollback(args.env, args.base_dir)

parse_arguments()
