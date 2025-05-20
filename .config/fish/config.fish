set -gx EDITOR nvim

fish_add_path ".local/bin/"

abbr --add py python3
abbr --add spt spotify_player
abbr --add nv nvim
abbr --add inv fzf --bind '"enter:become(nvim {})"' --preview '"cat {}"'

if status is-interactive
    # Commands to run in interactive sessions can go here
end
