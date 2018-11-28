# Visualizing 3D Data with Blender in Python

This repository contains various Python scripts for visualizing 3D data,
in the form of triangular meshes, point clouds or occupancy grids,
using [Blender](https://www.blender.org/)'s [Python API](https://docs.blender.org/api/current/).

**Acknowledgement: The code is based in some parts on work by
[Simon Donné](https://avg.is.tuebingen.mpg.de/person/sdonne).**

If you use this code, consider citing:

    @inproceedings{Stutz2018CVPR,
        title = {Learning 3D Shape Completion from Laser Scan Data with Weak Supervision },
        author = {Stutz, David and Geiger, Andreas},
        booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
        publisher = {IEEE Computer Society},
        year = {2018}
    }
    @misc{Stutz2017,
        author = {David Stutz},
        title = {Learning Shape Completion from Bounding Boxes with CAD Shape Priors},
        month = {September},
        year = {2017},
        institution = {RWTH Aachen University},
        address = {Aachen, Germany},
        howpublished = {http://davidstutz.de/},
    }

![Example of visualizations.](screenshot.jpg?raw=true "Example of visualizations.")

## Requirements

The code was tested with [Blender](https://www.blender.org/) 2.78 or higher.
Python should be installed locally and should also ship Python 3.5 with
a custom NumPy installation.

All remaining requirements, essentially [dimatura/binvox-rw-py](https://github.com/dimatura/binvox-rw-py)
and [alextsui05/blender-off-addon](https://github.com/alextsui05/blender-off-addon)
are included.

## File Formats

The following file formats are assumed:

* [OFF](https://en.wikipedia.org/wiki/OFF_(file_format)): file format for triangular meshes.
* [BINVOX](http://www.patrickmin.com/binvox/): file format for occupancy grids.
* A custom TXT format for point clouds.

The provided OFF files can be visualized using [MeshLab](http://www.meshlab.net/).
Scripts for converting OBJ files to OFF files as well as writing BINVOX and TXT files
are provided.

The custom TXT file format looks as follows:

    n_points
    p1_x p1_y p2_z
    p2_x p2_y p2_z
    ...

Use the following Python scripts for conversion:

* `off_to_obj.py` and `obj_to_off.py` to conversion between OFF and OBJ.
* `txt_to_ply.py` to convert a TXT point cloud to PLY format.

Examples of using the included Python code for writing TXT or BINVOX files
are provided in `write_txt.py` and `write_binvox.py`.

## Examples

`examples/` includes some examples; these should be rune out of the root folder:

    ./examples/render_off.sh
    ./examples/render_binvox.sh
    ./examples/render_txt.sh

All examples create `examples/0.png`.

## Usage

The provided examples essentially use the functionality provided in `blender_utils.py`;
the general approach is as follows:

    # Import utils.
    from blender_utils import *
    
    # Initialize and set camera target.
    # Check the function to adapt the light sources or camera(s).
    camera_target = initialize()
    
    # Create a material.
    # First parameter is the name, second is the diffuse color in rgb,
    # third argument is the alpha channel and last whether to cast/receive shadow.
    off_material = make_material('BRC_Material_Mesh', (0.66, 0.45, 0.23), 0.8, True)

    # Load an OFF file, alternatively, use load_binvox or load_txt.
    # In any case, we need the previously defined material.
    # The mesh provided in examples/0.off is scaled to [0,32]^3,
    # so we scale it by 1/32 = 0.03125 and then translate it to the
    # origin using (-0.5, -0.5, -0.5).
    # Finally we switch y and z axes.
    load_off(args.off, off_material, (-0.5, -0.5, -0.5), 0.03125, 'xzy')

    # Set rotation of camera around the origin, implicitly defines the locatio
    # together with the distance.
    rotation = (5, 0, -55)
    distance = 0.5
    
    # Render all loaded objects using the camera_target obtained above and
    # the output file.
    render(camera_target, output_file, rotation, distance)

## License

License for source code corresponding to:

D. Stutz, A. Geiger. **Learning 3D Shape Completion from Laser Scan Data with Weak Supervision.** IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018.

Note that the source code is based on the following projects for which separate licenses apply:

* [ModelNet](http://modelnet.cs.princeton.edu/)
* [alextsui05/blender-off-addon](https://github.com/alextsui05/blender-off-addon)
* [dimatura/binvox-rw-py](https://github.com/dimatura/binvox-rw-py)

Copyright (c) 2018 David Stutz, Max-Planck-Gesellschaft

**Please read carefully the following terms and conditions and any accompanying documentation before you download and/or use this software and associated documentation files (the "Software").**

The authors hereby grant you a non-exclusive, non-transferable, free of charge right to copy, modify, merge, publish, distribute, and sublicense the Software for the sole purpose of performing non-commercial scientific research, non-commercial education, or non-commercial artistic projects.

Any other use, in particular any use for commercial purposes, is prohibited. This includes, without limitation, incorporation in a commercial product, use in a commercial service, or production of other artefacts for commercial purposes.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

You understand and agree that the authors are under no obligation to provide either maintenance services, update services, notices of latent defects, or corrections of defects with regard to the Software. The authors nevertheless reserve the right to update, modify, or discontinue the Software at any time.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. You agree to cite the corresponding papers (see above) in documents and papers that report on research using the Software.
