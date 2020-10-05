from __future__ import print_function

import io
import json
import os.path
import pickle
from pprint import pprint

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# from pprint import pprint as print
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def saveJSON(obj, fp):
    with open(fp, 'w') as file:
        json.dump(obj, file, indent=2)


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    # results = drive_service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])
    #
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

    def download_file(file_id, filename):
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        print(fh)
        print(request)
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with open(filename, 'wb') as file:
            file.write(fh.getvalue())

    def get_list_of_files_in_folder(folder_id):
        files = []
        page_token = None
        while True:
            response = drive_service.files().list(q=f"'{folder_id}' in parents",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name, mimeType)',
                                                  pageToken=page_token).execute()
            files.extend([file for file in response.get('files', [])])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files


    def parse_solutions():
        zadaval_id = "1K3tt3NfW1IR1eTe7nJezzu-KSMO0suYU"
        return get_list_of_files_in_folder(zadaval_id)

    def find_folders(list_of_files):
        folders = dict()
        for folder in list_of_files:
            if folder['mimeType'] == 'application/vnd.google-apps.folder':
                folders[folder['name']] = folder['id']
        return folders

    # res = parse_solutions()
    # saveJSON(res, 'res.json')
    get_list_of_files_in_folder("1K3tt3NfW1IR1eTe7nJezzu-KSMO0suYU")
    with open('res.json') as file:
        res = json.load(file)
    pprint(res)

    folders = find_folders(res)

    weeks = get_list_of_files_in_folder(folders['Ангем'])

    week3 = get_list_of_files_in_folder(find_folders(weeks)['3 неделя'])

    pprint(week3)

    f = download_file(week3[0]['id'], week3[0]['name'])

    print(f)


if __name__ == '__main__':
    main()
