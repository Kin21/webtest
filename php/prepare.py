import argparse
import utils

parser = argparse.ArgumentParser()

parser.add_argument('script', help='Script where values will be replaced.', metavar='script.php')
parser.add_argument('-o', help='Name of the output file.', metavar='OUTPUT_FILE')
parser.add_argument('-l', '--list', action='store_const', const=True, dest='l')
parser.add_argument('--exif', help='Try to imitate signature of the allowed types.', choices=['png', 'jpg', 'pdf'])
#Values allowed for replacement: RFILE, TEXT
parser.add_argument('--rfile', help='Destination of the file to read on remote system.', metavar='RFILE')
parser.add_argument('--text', help='Text to echo in scripts.', metavar='TEXT')

#Available scripts
list_message = '''Scripts with arguments that are available:
read_file.php rfile
echo.php text
'''

args = parser.parse_args()



def get_output_filename(args):
    if args.o:
        return args.o
    else:
        return args.script + '.done'


def main():
    if args.l:
        print(list_message)
        exit(0)
    script_content = utils.get_file_content(args.script, 'r')
    if not script_content:
        exit(1)
    output_filename = get_output_filename(args)
    with open(output_filename, 'w') as f:
        for line in script_content:
            f.write(line.format(RFILE = args.rfile, TEXT = args.text))

    if args.exif:
        utils.impose_signatue(output_filename, args.exif)

    print('Done, result script: {}'.format(output_filename))

if __name__ == '__main__':
    main()