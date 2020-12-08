import os
import zipfile


from pymongo import MongoClient
import gridfs
db = MongoClient().gridfs
fs = gridfs.GridFS(db)


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


# def fill_folder():
#     files = [fs.get_last_version(file) for file in fs.list()]
#     for file in files:
#         with open(f'zip/{file.name}', 'w') as f:
#             f.write(file.read().decode())
#     print(files)

if __name__ == '__main__':
    # fill_folder()
    zipf = zipfile.ZipFile('files.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('zip/', zipf)
    zipf.close()
