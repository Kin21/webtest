import argparse

parser = argparse.ArgumentParser()

parser.add_argument('script', help='Script where values will be replaced.', metavar='script.php')
parser.add_argument('-o', help='Name of the output file.', metavar='OUTPUT_FILE')
parser.add_argument('--exif', help='Try to imitate signature of the allowed types.', choices=['png', 'jpg', 'pdf'])
#Values allowed for replacement: RFILE
parser.add_argument('--rfile', help='Destination of the file to read on remote system.', metavar='RFILE')

args = parser.parse_args()

def str_file__read_mode(args):
    return not bool(args.exif)

def get_output_filename(args):
    if args.o:
        return args.o
    else:
        return args.script + '.done'


if str_file__read_mode(args):
    try:
        with open(args.script, 'r') as f:
            script_content = f.readlines()
    except FileNotFoundError:
        print('Error: File {} not found !'.format(args.script))
        exit(1)
    output_filename = get_output_filename(args)
    with open(output_filename, 'w') as f:
        for line in script_content:
            f.write(line.format(RFILE = args.rfile))
    print('Done, result script: {}'.format(output_filename))
