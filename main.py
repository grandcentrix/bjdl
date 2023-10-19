import requests
from requests.auth import AuthBase
import getpass
import json

"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>.

@author René Beckmann
@copyright 2023, grandcentrix GmbH
"""

BASE_URL = "https://api.bluejeans.com"


class BlueJeansAuth(AuthBase):
    def __init__(self, token):
        # setup any auth-related data here
        self.token = token

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = f"Bearer {self.token}"
        return r


def authenticate(name, pw):
    url = BASE_URL + "/oauth2/token#User"
    body = {
        "grant_type": "password",
        "username": name,
        "password": pw
    }
    resp = requests.post(url, json=body)
    resp.raise_for_status()
    result = resp.json()
    return result["access_token"], result["scope"]["user"]


def list_meeting_recordings(session, user_id):
    url = BASE_URL + f"/v1/user/{user_id}/meeting_history/recordings"
    params = {"pageSize": 100}
    resp = session.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def get_recording(session, user_id, rec_id):
    url = BASE_URL + f"/v1/user/{user_id}/meeting_history/recordings/{rec_id}"
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json()


def get_recording_download_link(session, user_id, content_id):
    url = BASE_URL + f"/v1/user/{user_id}/cms/{content_id}"
    params = {
        "isDownloadable": True,
        "expiry": 10
    }
    resp = session.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def get_dl_links(session, user_id, recordings):
    result = list()
    for rec in recordings:
        rec_id = rec["recordingEntityId"]
        recording = get_recording(session, user_id, rec_id)
        for chapter in recording["recordingChapters"]:
            print(".", end='', flush=True)
            content_id = chapter["compositeContentId"]
            chapter_name = chapter["chapterName"]
            start = chapter["startTimeOffset"]
            end = chapter["endTimeOffset"]
            dl_info = get_recording_download_link(session, user_id, content_id)
            for level in dl_info["contentProperties"]["levels"]:
                if int(level["height"]) == 720:
                    result.append({
                        "name": chapter_name,
                        "link": level["file"],
                        "start": start,
                        "end": end
                    })
        print()
    return result


def main():
    name = input("BlueJeans username (email):")
    pw = getpass.getpass("BlueJeans password:")
    print("Accessing recordings...")
    session = requests.session()
    token, user_id = authenticate(name, pw)
    session.auth = BlueJeansAuth(token)
    recordings = list_meeting_recordings(session, user_id)
    print(f"Found {len(recordings)} recordings")
    links = get_dl_links(session, user_id, recordings)
    print("Writing recordings to recordings.json")
    with open("recordings.json", "w") as f:
        json.dump(links, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()