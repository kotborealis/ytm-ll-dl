# ytm-ll-dl

Python app to download 'Liked music' playlist from Youtube Music.

## Usage

For full help, run `ytm-ll-dl --help`.

Basic usage:
```sh
$ ytm-ll-dl
    --output ./data/ # Where to store downloaded music
    --limit INT      # Limit how much tracks to fetch from the beginning of playlist
    --skip INT       # Skip specified amount of tracks from the end of playlist
```

On first run, this will ask you to provide auth data from YTM.
See [ytmusicapi documentation](https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers)
for details.

`ytm-ll-dl` will download all liked tracks with thumbnails and some meta-info
(author, album, name).

You can interrupt `ytm-ll-dl` --- download state will be saved and restored on the next run.