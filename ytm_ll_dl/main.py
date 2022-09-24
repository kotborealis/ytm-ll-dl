from pathlib import Path
import re

from sh import cd, ErrorReturnCode
from ytmusicapi import YTMusic

from ytm_ll_dl.slugify import slugify
from ytm_ll_dl.index_helpers import Index, IndexStatus
from ytm_ll_dl.bash import bash
import click


@click.command()
@click.option(
    '--output',
    required=True,
    type=Path,
    help='Output directory.'
)
@click.option(
    '--limit',
    default=999999,
    type=int,
    help='Number of tracks to get from the top.'
)
@click.option(
    '--skip',
    default=0,
    type=int,
    help='Skip tracks from the bottom.'
)
def main(
    output: Path,
    limit: int,
    skip: int
):
    """Download liked music from YTM"""
    
    for bin in ["curl", "ffmpeg"]:
        if bash(f"command -v '{bin}' || echo 'None'").strip() == 'None':
            print(f"Program `{bin}` not found but required. Please install it.")
            exit(1)
    
    data_dir = output
    # Create data directory
    bash(f"mkdir -p {str(data_dir)}")
    
    index = Index(data_dir)

    auth_headers = data_dir / "./.headers_auth.json"

    if not auth_headers.exists():
        YTMusic.setup(filepath=str(auth_headers))

    ytm = YTMusic(str(auth_headers))

    print("Getting liked music...")
    tracks = ytm.get_liked_songs(limit)["tracks"]

    print(f"Got {len(tracks)} tracks")
    print("")

    i = 0
    for track in reversed(tracks):
        i += 1
        
        if skip > 0:
            skip -= 1
            continue

        with cd(data_dir):
            prefix = f"[{i}/{len(tracks)}] "
            log = lambda x: print(prefix + str(x))
            
            id = track['videoId']
            
            artist = track['artists'][0]['name']
            title = track['title']
            album = track['album']['name'] if track['album'] else None
            
            mp3 = f"{slugify(artist)}, {slugify(title)}.mp3"
            mp3_tmp = ".tmp.mp3"
            mp3_tmp2 = ".tmp2.mp3"
            
            status = index.get(id)
            if status is not None:
                log(f"Video {mp3} already in index ({status.value}), skipping...")
                continue
            else:
                log(f"Downloading {mp3}...")
                
            for file in [mp3, mp3_tmp, mp3_tmp2]:
                Path(file).unlink(missing_ok=True)
            
            try:
                output = bash(
                    "yt-dlp "
                    f"https://www.youtube.com/watch?v={id} "
                    f"-x -o '{mp3_tmp}'"
                )
            except ErrorReturnCode as e:
                log("yt-dlp failed")
                log(e)
                index.add(id, IndexStatus.failed)
                continue
        

            for line in output.splitlines():
                tag = "[ExtractAudio] Destination: "
                if line.startswith(tag):
                    new_dest = line[len(tag):]
                    bash(f"ffmpeg -i '{new_dest}' '{mp3_tmp}'")
                    bash(f"rm '{new_dest}'")
                    break
            
            thumbnail = "current.png"
            bash(f"curl '{track['thumbnails'][-1]['url']}' -o {thumbnail}")
            
            title = re.sub('\"', '\\"', title)
            artist = re.sub('\"', '\\"', artist)
            album = re.sub('\"', '\\"', album) if album else None
            
            title = re.sub('`', '\\`', title)
            artist = re.sub('`', '\\`', artist)
            album = re.sub('`', '\\`', album) if album else None
            
            bash(
                f"ffmpeg -y -i '{mp3_tmp}' -i {thumbnail} " +
                "-map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v " +
                "title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\" " +
                f"-metadata title=\"{title}\" " + 
                f"-metadata artist=\"{artist}\" " + 
                (f"-metadata album=\"{album}\" " if album else " ") +
                f"-c:a libmp3lame {mp3_tmp2}"
            )
            
            Path(thumbnail).unlink(missing_ok=True)
            Path(mp3_tmp2).rename(mp3)
            
            index.add(id, IndexStatus.ready)


if __name__ == '__main__':
    main()

