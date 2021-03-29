# Spotify Playlist Archiver

AWS Lambda Function that will manage the length of collaborative Spotify playlists. Whenever playlist exceeds length old tracks will be moved to an archive playlist. 
## Pre-Reqs

[Terraform v0.12.10](https://releases.hashicorp.com/terraform/0.12.10/)

[Python 3.8](https://www.python.org/downloads/release/python-380/)

[Spotify App Credentials](https://developer.spotify.com/documentation/general/guides/app-settings/) - Redirect URI can be anything e.g http://127.0.0.1:10888

[Playlist IDs](https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html) - You must be Owner of collaborative playlists

[AWS CLI credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) - for terraform deployment

## Deployment

Fill secrets terraform.tfvars, set playlist lengths in app.py, add multiple playlists if required.

Get .cache file - see Spotify Auth section

Copy .cache file into src/ folder

Run "pip3 install spotipy -t ./"

terraform init && terraform plan

terraform apply
## Spotify Auth

1. Run the script locally so the user can sign in once - create auth.py script
2. In the local project folder, you will find a file .cache
3. Copy this file to your project folder on AWS
4. It should work (check Token expiry date, adjust schedule accordingly)