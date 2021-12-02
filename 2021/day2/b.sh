#!/bin/bash

position=0
depth=0
aim=0

while read direction n; do
    case $direction in
        forward)
            (( position += n ))
            (( depth += aim * n ))
            ;;
        up)
            (( aim -= n ))
            ;;
        down)
            (( aim += n ))
            ;;
        *)
            echo "Unexpected input!" >&2
            exit 1
    esac
done

echo $(( depth * position ))
