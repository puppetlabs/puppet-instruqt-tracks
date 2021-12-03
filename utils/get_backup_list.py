#!/usr/bin/env python3
import requests
import re
import os


print("changing working directory to: " + os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("Removing backup.list")
os.remove("backup.list")

all_tracks_query = '''
query GetTracks {
  tracks(organizationSlug: "puppet"){
    id
    slug
    tags
    status
  }
}
'''

auth_token = os.environ['INSTRUQT_TOKEN']

headers = {"Authorization": auth_token}

all_tracks_request = requests.post('https://play.instruqt.com/graphql', json={'query': all_tracks_query}, headers=headers)

data = all_tracks_request.json()

searchString = "BACKUP"

with open('backup.list', 'a') as backupList:

  for i in range(len(data['data']['tracks'])):
    if re.search(searchString, str(data['data']['tracks'][i]['tags'])):
      print("Found BACKUP Tag for track: %s  - adding to backup.list file" % data['data']['tracks'][i]['slug'])
      print()
      backupList.write("puppet/" + data['data']['tracks'][i]['slug'] + '\n')

    else:
      print("BACKUP tag string not found in track: ")
      print(data['data']['tracks'][i]['slug'])
      print(data['data']['tracks'][i]['tags'])

backupList.close()
