import tftpy
import sys
from os import listdir
from os.path import isfile, join


def upload_files(client, path):
    files_to_upload = [f for f in listdir(path) if isfile(join(path, f))]
    print('Files that will be uploaded: {0}'.format(files_to_upload))

    for file in files_to_upload:
        try:
            print('Uploading "{0}"...'.format(file))
            client.upload(file, to_upload_path + file, timeout=10)
            print('Upload succesful.')
        except KeyboardInterrupt:
            print('Aborting...')
            exit(0)
        except tftpy.TftpTimeout:
            print('Timeout while uploading {0}, skipping it.'.format(file))


addr = sys.argv[1]
iterations = 1
if len(sys.argv) > 2:
    iterations = sys.argv[2]

    try:
        iterations = int(iterations)
    except ValueError:
        print('Invalid number of iterations provided.')
        exit(1)

client = tftpy.TftpClient(addr, 69, options={'blksize': 512, 'timeout': 10, 'tsize': 25495})

to_upload_path = './to_upload/'

if iterations < 0:
    while True:
        upload_files(client, to_upload_path)
else:
    for i in range(0, iterations):
        upload_files(client, to_upload_path)

