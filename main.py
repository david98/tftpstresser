import tftpy
import sys
from os import listdir
from os.path import isfile, join, getsize
from time import sleep


def upload_files(path):
    files_to_upload = [f for f in listdir(path) if isfile(join(path, f)) and f != '.gitkeep']
    print('Files that will be uploaded: {0}'.format(files_to_upload))

    for file in files_to_upload:
        try:
            print('Uploading "{0}"...'.format(file))
            client = tftpy.TftpClient(addr, 69, options={'blksize': 512, 'timeout': 10,
                                                         'tsize': getsize(to_upload_path + file)})
            client.upload(file, to_upload_path + file, timeout=10)
            print('Upload succesful.')
            print('Waiting {0} seconds before initiating next transfer...'.format(secs_between_transfers))
            sleep(secs_between_transfers)
        except KeyboardInterrupt:
            print('Aborting...')
            exit(0)
        except tftpy.TftpTimeout:
            print('Timeout while uploading {0}, skipping it.'.format(file))


addr = sys.argv[1]
iterations = 1
secs_between_transfers = 0
secs_between_iterations = 0
if len(sys.argv) > 2:
    iterations = sys.argv[2]

    try:
        iterations = int(iterations)
    except ValueError:
        print('Invalid number of iterations provided.')
        exit(1)

if len(sys.argv) > 3:
    secs_between_transfers = sys.argv[3]

    try:
        secs_between_transfers = int(secs_between_transfers)
    except ValueError:
        print('Invalid seconds between transfers.')
        exit(1)

if len(sys.argv) > 4:
    secs_between_iterations = sys.argv[4]

    try:
        secs_between_iterations = int(secs_between_iterations)
    except ValueError:
        print('Invalid seconds between iterations.')
        exit(1)

to_upload_path = './to_upload/'

if iterations < 0:
    while True:
        upload_files(to_upload_path)
        print('Waiting {0} seconds before next iteration...'.format(secs_between_iterations))
        sleep(secs_between_iterations)
else:
    for i in range(0, iterations):
        upload_files(to_upload_path)
        if i < iterations:
            print('Waiting {0} seconds before next iteration...'.format(secs_between_iterations))
            sleep(secs_between_iterations)
