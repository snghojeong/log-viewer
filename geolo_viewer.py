import geolo_view
import sys
import argparse

parser = argparse.ArgumentParser(description='Log reader')
parser.add_argument('--file', required=True, help='log file')
parser.add_argument('--cnt', required=True, help='the number of log line')
parser.add_argument('--page', required=True, help='the number of page')
parser.add_argument('--seq', required=False, help='seq number to filter')
parser.add_argument('--date', required=False, help='date to filter')
parser.add_argument('--lv', required=False, help='log level to filter')
parser.add_argument('--md', required=False, help='module name to filter')
parser.add_argument('--msg', required=False, help='message string to filter')

args = parser.parse_args()

prog_exit = 0
if args.md and args.lv:
    ret = geolo_view.read_log(args.file, 0, int(args.cnt), lv=args.lv, md=args.md)
elif args.md:
    ret = geolo_view.read_log(args.file, 0, int(args.cnt), md=args.md)
elif args.lv:
    ret = geolo_view.read_log(args.file, 0, int(args.cnt), lv=args.lv)
else:
    ret = geolo_view.read_log(args.file, 0, int(args.cnt))
print(ret["log"])
