#!/bin/bash
if [ -z "$BLENDER" ]; then
    export BLENDER="blender"
fi

"$BLENDER" --background --python render_off_txt.py -- --off examples/0.off --txt examples/0.txt --output examples/0.png
