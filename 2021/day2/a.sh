#!/bin/bash

position=0
depth=0

while read direction distance; do
    case $direction in
        forward)
            (( position += distance ))
            ;;
        up)
            (( depth -= distance ))
            ;;
        down)
            (( depth += distance ))
            ;;
        *)
            echo "Unexpected input!" >&2
            exit 1
    esac
done

echo $(( depth * position ))
