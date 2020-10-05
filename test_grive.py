from pprint import pprint

from gdriveview import GDriveViewer

zadaval_id = "1K3tt3NfW1IR1eTe7nJezzu-KSMO0suYU"

viewer = GDriveViewer()

r = viewer.get_list_of_files_in_folder(zadaval_id)
pprint(r)

while True:
    print('\n'.join(viewer.make_pretty_list(r)))
    while True:
        try:
            file_name = input('Что дальше?')
            next_file = r[file_name]
            break
        except KeyError:
            print('Такой файл не существует')
    if next_file['mimeType'] == 'application/vnd.google-apps.folder':
        r = viewer.get_list_of_files_in_folder(next_file['id'])
    else:
        viewer.download_file(next_file['id'], file_name)

# def hello(func):
#     def wrapper(*args, **kwargs):
#         print('Hello !')
#         result = func(*args, **kwargs)
#         print('Fuck you')
#
#     return wrapper
#
#
# @hello
# def func(n):
#     [print(i) for i in range(n)]
#
#
# func(10)
