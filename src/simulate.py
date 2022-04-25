#!/usr/bin/env python3
import os
import sys
import shutil
from rich import print

# main function to begin simulation
def main():
    # Check if tmux binary is available
    try:
        shutil.which("tmux")
    except shutil.Error:
        print("[bold][[red]![/red]] Could not find [red]Tmux[/red] in PATH", file=sys.stderr)
        sys.exit(-1)

    # Start video stream in tmux session
    streamer_program = os.path.abspath(os.path.dirname(__file__)) + "/start_stream.py"
    if not os.path.isfile(streamer_program):
        print(f"[bold][[red]![/red]] Could not find file:[red]{streamer_program}[/red]", file=sys.stderr)
        sys.exit(-1)

    os.system("tmux kill-session -t test 2>/dev/null")
    os.system(f'tmux new-session -d -s "test" \; send-keys "{streamer_program} -i 0.0.0.0 ~/Tools/Fake-Stream/test.mp4" C-m\; split-window -h \; send-keys \'top\' C-m \;')
    print ("Done")


if __name__=='__main__':
    main()
