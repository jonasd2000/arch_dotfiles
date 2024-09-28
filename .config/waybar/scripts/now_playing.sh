if [[ "$(playerctl status)" == Paused ]]; then
    echo ""
    exit 1;
fi
echo "$(playerctl metadata artist) - $(playerctl metadata title)"
