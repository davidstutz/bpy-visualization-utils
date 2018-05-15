#!/bin/bash
if [ -z "$BLENDER" ]; then
    export BLENDER="blender"
fi

"$BLENDER" --background --python render_txt.py -- --txt examples/0.txt --output examples/0.png