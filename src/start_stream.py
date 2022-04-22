#!/usr/bin/env python3
import os
import sys
import socket
import ffmpeg
import argparse
from rich import print
from rich.console import Console


# Custom class for handling errors
class VideoParseError(Exception):
    def __init__(self, videofile, error_msg="Videofile is corrupted"):
        self.videofile = videofile
        self.err_msg = error_msg
        super().__init__(self.err_msg)

    def __str__(self):
        return f"Error occured while parsing {self.videofile} -> {self.err_msg}"


# Function to check if video file is corrupted:
def check_corrupted_video_file(videofile):
    """Returns true if video file is OK otherwise raises VideoParseError"""
    if not os.path.isfile(videofile):
        raise VideoParseError(videofile, "[!] Videofile could not be found")
    try:
        (ffmpeg.input(videofile)
         .output("pipe:", f="null")
         .run(quiet=True)
        )
    except ffmpeg._run.Error:
        raise VideoParseError(videofile)
    return True


# Function to start streams
def start_stream(videofile,ip="127.0.0.1", port="2300"):
    """ Function to start video stream over UDP port"""
    console = Console()

    # Check if Video file is OK
    try:
        with console.status(f"[bold]Testing [magenta]{videofile}", spinner="monkey") as status:
            check_corrupted_video_file(videofile)
        print("[bold][[green]+[/green]] Videofile is [green]OK[/green]", ":white_check_mark:")
    except VideoParseError:
        print("[bold][[red]![/red]] Cannot start stream due to previous error",":x:", file=sys.stderr)
        return False

    # Check if port is valid:
    try:
        port = int(port)
        if port < 1 or port > 65535:
            raise ValueError
    except ValueError:
        print("[bold][[red]![/red]] Invalid Port Number:", port, ":x:", file=sys.stderr)
        return False

    # Check if IP is valid
    try:
        socket.inet_aton(ip)
    except socket.error:
        print("[bold][[red]![/red]] Invalid IP Address:", ip, ":x:", file=sys.stderr)
        return False

    stream_url = f"http://{ip}:{port}"
    print(f"[bold][[green]+[/green]] Streaming:", videofile)
    print(f"[bold][[green]+[/green]] Starting URL: {stream_url}", ":movie_camera:")

    video_to_stream = ffmpeg.input(videofile)
    process= lambda : (
    ffmpeg
    .input(videofile)
    .output(
        stream_url,
        codec="copy", 
        listen=1,
        f="flv")
    .run(quiet=True))

    try:
        with console.status(f"[bold]Streaming ▶️", spinner="runner") as status: 
            while True:
                process()

    except KeyboardInterrupt:
        print("[bold][[red]![/red]] Bye!")

    except Exception as e:
        print(f"[bold][[red]![/red]] Error occured as: {e}", ":face_with_thermometer:",file=sys.stderr)
        return False

# main function to handle cases when the file is invoked directly
def main():
    parser = argparse.ArgumentParser(description="[+] Video Streamer Over UDP using FFMPEG and VLC Client")
    parser.add_argument('VIDEO', help="Video File To Stream")
    parser.add_argument('-p', metavar="PORT", nargs='?', type=int, default=2300, const=2300, help="Port to stream UDP over")
    parser.add_argument('-i', metavar="IP", nargs='?', default="127.0.0.1", const="127.0.0.1", help="IP to stream UDP over")
    args = parser.parse_args()

    print("[bold][[green]![green]] [red]Network [cyan]Video [yellow]Streamer")
    start_stream(args.VIDEO, args.i, args.p)


if __name__=='__main__':
    main()

    
