#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias ll='ls -la --color=auto'
alias grep='grep --color=auto'
alias py="python3"

# gitgraph
alias gitg='git log --graph --oneline --color --all'
# tui file explorer
alias ex='yazi'

PS1='[\u@\h \W]\$ '
