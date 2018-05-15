#!/bin/bash
if [ -z "$BLENDER" ]; then
    export BLENDER="blender"
fi

"$BLENDER" --background --python render_binvox.py -- --binvox examples/0.binvox --output examples/0.png
