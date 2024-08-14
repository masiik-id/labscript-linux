echo "$(date "+%Y-%m-%d %H:%M:%SS") $(whoami)  ${SSH_CLIENT%% *} $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")"
