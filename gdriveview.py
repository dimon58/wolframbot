from __future__ import print_function

import io
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class GDriveViewer(object):
    def __init__(self, mode='readonly'):
        """
        :param mode: Google drive access mode
        """

        if mode:
            SCOPES = [f'https://www.googleapis.com/auth/drive.{mode}']
        else:
            SCOPES = ['https://www.googleapis.com/auth/drive']

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

        self.drive_service = build('drive', 'v3', credentials=creds)

    def download_file(self, file_id, filename):
        request = self.drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with open(filename, 'wb') as file:
            file.write(fh.getvalue())

    def get_list_of_files_in_folder(self, folder_id):
        files = dict()
        page_token = None
        while True:
            response = self.drive_service.files().list(q=f"'{folder_id}' in parents",
                                                       spaces='drive',
                                                       fields='nextPageToken, files(id, name, mimeType)',
                                                       pageToken=page_token).execute()

            files.update(
                {file['name']: {'id': file['id'], 'mimeType': file['mimeType']}
                 for file in response.get('files', [])}
            )
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files

    @staticmethod
    def make_pretty_list(list_of_files:dict):
        result = []
        for file_name, file in list_of_files.items():
            file_type = file['mimeType']
            file_type = 'Folder' if file_type == 'application/vnd.google-apps.folder' else 'File'

            result.append(f"{file['mimeType']}: {file_name}")
        return result

    def find_folders(self, list_of_files):
        folders = dict()
        for folder in list_of_files:
            if folder['mimeType'] == 'application/vnd.google-apps.folder':
                folders[folder['name']] = folder['id']
        return folders
