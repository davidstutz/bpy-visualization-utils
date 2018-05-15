#!/bin/bash
if [ -z "$BLENDER" ]; then
    export BLENDER="blender"
fi

"$BLENDER" --background --python render_off.py -- --off examples/0.off --output examples/0.png
