#!/bin/sh

python_cmd="$1 $2 $3 $4"

osascript -e 'tell app "Terminal"
  do script ('\""$python_cmd"\"')
end tell'