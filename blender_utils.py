import sys
import os


class LogLevel:
    """
    Defines color of log message.
    """

    INFO = '\033[94m'
    """ (string) Blue. """
    WARNING = '\033[93m'
    """ (string) Yellow. """
    ERROR = '\033[91m\033[1m'
    """ (string) Red. """
    ENDC = '\033[0m'
    """ (string) End of color. """


def log(output,level=LogLevel.INFO):
    """
    Log message.

    :param output: message
    :param level: LogLevel
    """

    sys.stderr.write(level)
    sys.stderr.write(str(output))
    sys.stderr.write(LogLevel.ENDC)
    sys.stderr.write("\n")
    sys.stderr.flush()


# This makes sure that Blender's NumPy is loaded first.
# The path needs to be adapted before usage.
# Example:
#   blender_package_path = '~/blender-2.79-linux-glibc219-x86_64/2.79/python/lib/python3.5/site-packages/'
if not 'BLENDER_PACKAGE_PATH' in globals():
    BLENDER_PACKAGE_PATH = None
    BLENDER_PACKAGE_PATH = '/BS/dstutz/work/dev-box/blender-2.79-linux-glibc219-x86_64/2.79/python/lib/python3.5/site-packages/'
if BLENDER_PACKAGE_PATH is None:
    log('Open blender_utils.py and set BLENDER_PACKAGE_PATH before usage, check documentation!', LogLevel.ERROR)
    exit()
if not os.path.exists(BLENDER_PACKAGE_PATH):
    log('The set BLENDER_PACKAGE_PATH does not exist, check documentation!', LogLevel.ERROR)
    exit()

sys.path.insert(1, os.path.realpath(BLENDER_PACKAGE_PATH))

import bpy
import bmesh
import math
import numpy as np

import binvox_rw
import import_off
import_off.register()

sphere_base_mesh = None
cube_base_mesh = None


def initialize(width=512, height=448):
    """
    Setup scene, camer and lighting.

    :param width: width of rendered image
    :param height: height of rendered image
    :return: camera target
    """

    # First, the base meshes (sphere and cube) are set,
    # these are later used to display point clouds or occupancy grids.
    bpy.ops.mesh.primitive_ico_sphere_add()
    global sphere_base_mesh
    sphere_base_mesh = bpy.context.scene.objects.active.data.copy()
    for face in sphere_base_mesh.polygons:
        face.use_smooth = True

    bpy.ops.mesh.primitive_cube_add()
    global cube_base_mesh
    cube_base_mesh = bpy.context.scene.objects.active.data.copy()

    # Delete current scene, except for the camera and the lamp
    for obj in bpy.data.objects:
        if str(obj.name) in ['Camera']:
            continue
        obj.select = True
        bpy.ops.object.delete()

    scene = bpy.context.scene

    # Setup the camera, location can also be influenced later,
    # these are only defaults.
    cam = scene.objects['Camera']
    cam.location = (0, 3.0, 1.0)
    cam.data.lens = 35
    cam.data.sensor_width = 32
    cam.data.sensor_height = 32
    cam_constraint = cam.constraints.new(type='TRACK_TO')
    cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    cam_constraint.up_axis = 'UP_Y'

    def parent_obj_to_camera(b_camera):
        """
        Utility function defining the target of the camera as the origin.

        :param b_camera: camera object
        :return: origin object
        """

        origin = (0, 0, 0)
        b_empty = bpy.data.objects.new('Empty', None)
        b_empty.location = origin
        b_camera.parent = b_empty  # setup parenting

        scn = bpy.context.scene
        scn.objects.link(b_empty)
        scn.objects.active = b_empty
        return b_empty

    # Sets up the camera and defines its target.
    camera_target = parent_obj_to_camera(cam)
    cam_constraint.target = camera_target

    # For nicer visualization, several light locations are defined.
    # See the documentation for details, these should be edited based
    # on preferences.
    locations = [
        (-0.98382, 0.445997, 0.526505),
        (-0.421806, -0.870784, 0.524944),
        (0.075576, -0.960128, 0.816464),
        (0.493553, -0.57716, 0.928208),
        (0.787275, -0.256822, 0.635172),
        (1.01032, 0.148764, 0.335078)
    ]

    for i in range(len(locations)):
        # We only use point spot lamps centered at the given locations
        # and without any specific rotation (see euler angles below).
        lamp_data = bpy.data.lamps.new(name='Point Lamp ' + str(i), type='POINT')
        lamp_data.shadow_method = 'RAY_SHADOW'
        lamp_data.shadow_ray_sample_method = 'CONSTANT_QMC'
        lamp_data.use_shadow = True
        lamp_data.shadow_soft_size = 1e6
        lamp_data.distance = 2
        lamp_data.energy = 0.1
        lamp_data.use_diffuse = True
        lamp_data.use_specular = True
        lamp_data.falloff_type = 'CONSTANT'

        lamp_object = bpy.data.objects.new(name='Spot Lamp ' + str(i), object_data=lamp_data)
        scene.objects.link(lamp_object)
        lamp_object.location[0] = locations[i][0]
        lamp_object.location[1] = locations[i][1]
        lamp_object.location[2] = locations[i][2]
        lamp_object.rotation_euler[0] = 0
        lamp_object.rotation_euler[1] = 0
        lamp_object.rotation_euler[2] = 0
        lamp_object.parent = camera_target

    # This tries to use CUDA rendering if possible.
    try:
        if (2, 78, 0) <= bpy.app.version:
            # https://blender.stackexchange.com/questions/5281/blender-sets-compute-device-cuda-but-doesnt-use-it-for-actual-render-on-ec2
            bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
            bpy.context.user_preferences.addons['cycles'].preferences.devices[0].use = True
        else:
            bpy.context.user_preferences.system.compute_device_type = 'CUDA'
    except TypeError:
        pass

    scene.render.use_file_extension = False
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.use_antialiasing = True
    scene.render.use_shadows = True
    world = bpy.context.scene.world
    world.zenith_color = [1.0, 1.0, 1.0]
    world.horizon_color = [1.0, 1.0, 1.0]
    scene.render.alpha_mode = 'SKY'
    world.light_settings.use_environment_light = True
    world.light_settings.environment_color = 'PLAIN'
    world.light_settings.environment_energy = 0.5

    return camera_target


def make_material(name, diffuse, alpha, shadow=False):
    """
    Creates a material with the given diffuse and alpha. If shadow is true the
    object casts and receives shadows.

    :param name: name of material
    :param diffuse: diffuse color (in rgb)
    :param alpha: alpha (float in [0,1])
    :param shadow: whether to cast/receive shadows
    :return: material
    """

    material = bpy.data.materials.new(name)
    material.diffuse_color = diffuse
    material.diffuse_shader = 'LAMBERT'
    material.diffuse_intensity = 1
    material.specular_color = (1, 1, 1)
    material.specular_shader = 'COOKTORR'
    material.specular_intensity = 2
    material.alpha = alpha
    material.use_transparency = True
    material.ambient = 1.0

    material.use_cast_shadows = shadow
    material.use_shadows = shadow

    return material


def load_off(off_file, material, offset=(0, 0, 0), scale=1, axes='xyz'):
    """
    Loads a triangular mesh from an OFF file. For pre-processing, mesh.py can be used;
    the function still allows to define an offset (to translate the mesh) and a scale.

    The axes parameter defines the order of the axes. Using xzy, for example, assumes
    that the first coordinate is x, the second is z and the third is y.

    **Note that first, the axes are swapper, then the OFF is scaled and finally translated.**

    :param off_file: path to OFF file
    :param material: previously defined material
    :param offset: offset after scaling
    :param scale: scaling
    :param axes: axes definition
    """

    # This used import_off.py, see README for license.
    bpy.ops.import_mesh.off(filepath=off_file)

    assert len(offset) == 3
    assert scale > 0
    assert len(axes) == 3

    x_index = axes.find('x')
    y_index = axes.find('y')
    z_index = axes.find('z')

    assert x_index >= 0 and x_index < 3
    assert y_index >= 0 and y_index < 3
    assert z_index >= 0 and z_index < 3
    assert x_index != y_index and x_index != z_index and y_index != z_index

    for obj in bpy.context.scene.objects:

        # obj.name contains the group name of a group of faces, see http://paulbourke.net/dataformats/obj/
        # every mesh is of type 'MESH', this works not only for ShapeNet but also for 'simple'
        # obj files
        if obj.type == 'MESH' and not 'BRC' in obj.name:

            # change color
            # this is based on https://stackoverflow.com/questions/4644650/blender-how-do-i-add-a-color-to-an-object
            # but needed changing a lot of attributes according to documentation
            obj.data.materials.append(material)

            for vertex in obj.data.vertices:
                # make a copy, otherwise axes switching does not work
                vertex_copy = (vertex.co[0], vertex.co[1], vertex.co[2])

                # First, swap the axes, then scale and offset.
                vertex.co[0] = vertex_copy[x_index]
                vertex.co[1] = vertex_copy[y_index]
                vertex.co[2] = vertex_copy[z_index]

                vertex.co[0] = vertex.co[0] * scale + offset[0]
                vertex.co[1] = vertex.co[1] * scale + offset[1]
                vertex.co[2] = vertex.co[2] * scale + offset[2]

            obj.name = 'BRC_' + obj.name


def load_txt(txt_file, radius, material, offset=(0, 0, 0), scale=1, axes='xyz'):
    """
    Load a point cloud from txt file, see the documentation for the format.
    Additionally, the radius of the points, an offset and a scale can be defined, for details
    on the parameters also see load_off.

    :param txt_file: path to TXT file
    :param radius: radius of rendered points/spheres
    :param material: previously defined material
    :param offset: offset
    :param scale: scale
    :param axes: axes definition
    :return:
    """

    global sphere_base_mesh

    assert len(offset) == 3
    assert scale > 0
    assert len(axes) == 3

    x_index = axes.find('x')
    y_index = axes.find('y')
    z_index = axes.find('z')

    assert x_index >= 0 and x_index < 3
    assert y_index >= 0 and y_index < 3
    assert z_index >= 0 and z_index < 3
    assert x_index != y_index and x_index != z_index and y_index != z_index

    voxel_file = open(txt_file, 'r')
    voxel_lines = voxel_file.readlines()
    voxel_file.close()

    mesh = bmesh.new()
    for line in voxel_lines:
        vals = line.split(' ')
        if not line.startswith('#') and line.strip() != '' and len(vals) >= 3:
            location = (
                float(vals[x_index]) * scale + offset[0],
                float(vals[y_index]) * scale + offset[1],
                float(vals[z_index]) * scale + offset[2]
            )

            m = sphere_base_mesh.copy()
            for vertex in m.vertices:
                vertex.co[0] = vertex.co[0] * radius + location[0]
                vertex.co[1] = vertex.co[1] * radius + location[1]
                vertex.co[2] = vertex.co[2] * radius + location[2]

            mesh.from_mesh(m)

    mesh2 = bpy.data.meshes.new('Mesh')
    mesh.to_mesh(mesh2)

    obj = bpy.data.objects.new('BRC_Point_Cloud', mesh2)
    obj.data.materials.append(material)
    obj.active_material_index = 0
    obj.active_material = material

    bpy.context.scene.objects.link(obj)


def load_binvox(binvox_file, radius, material, offset, scale, axes):
    """
    Load a binvox file, see binvox_rw.py for format. Again, radius of the cubes, material, offset and scale
    can be defined as in load_off.

    :param binvox_file: path to binvox file
    :param radius: radius, i.e. side length, of cubes
    :param material: previously defined material
    :param offset: offset
    :param scale: scale
    :param axes: axes definition
    :return:
    """

    global cube_base_mesh

    assert len(offset) == 3
    assert len(scale) == 3
    assert len(axes) == 3

    x_index = axes.find("x")
    y_index = axes.find("y")
    z_index = axes.find("z")

    assert x_index >= 0 and x_index < 3
    assert y_index >= 0 and y_index < 3
    assert z_index >= 0 and z_index < 3
    assert x_index != y_index and x_index != z_index and y_index != z_index

    with open(binvox_file, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)

    points = np.where(model.data)
    locations = np.zeros((points[0].shape[0], 3), dtype=float)
    locations[:, 0] = (points[x_index][:] + 0.5) / model.data.shape[x_index]
    locations[:, 1] = (points[y_index][:] + 0.5) / model.data.shape[y_index]
    locations[:, 2] = (points[z_index][:] + 0.5) / model.data.shape[z_index]
    locations[:, 0] -= 0.5
    locations[:, 1] -= 0.5
    locations[:, 2] -= 0.5

    locations[:, 0] = locations[:, 0] * scale[0] + offset[0]
    locations[:, 1] = locations[:, 1] * scale[1] + offset[1]
    locations[:, 2] = locations[:, 2] * scale[2] + offset[2]

    mesh = bmesh.new()
    for i in range(locations.shape[0]):
            m = cube_base_mesh.copy()
            for vertex in m.vertices:
                vertex.co[0] = vertex.co[0] * radius + locations[i, 0]
                vertex.co[1] = vertex.co[1] * radius + locations[i, 1]
                vertex.co[2] = vertex.co[2] * radius + locations[i, 2]

            mesh.from_mesh(m)

    mesh2 = bpy.data.meshes.new('Mesh')
    mesh.to_mesh(mesh2)

    obj = bpy.data.objects.new('BRC_Occupancy', mesh2)
    obj.data.materials.append(material)
    obj.active_material_index = 0
    obj.active_material = material

    bpy.context.scene.objects.link(obj)


def render(camera_target, output_file, rotation, distance):
    """
    Render all loaded objects into the given object files. Additionally, the
    rotation of the camera around the origin and the distance can be defined.

    The first argument is the camera_target returned from initialize().

    :param camera_target: returned by initialize()
    :param output_file: path to output file
    :param rotation: rotation of camera
    :param distance: distance to target
    """

    bpy.context.scene.render.filepath = output_file

    camera_target.rotation_euler[0] = math.radians(rotation[0])
    camera_target.rotation_euler[1] = math.radians(rotation[1])
    camera_target.rotation_euler[2] = math.radians(rotation[2])

    cam = bpy.context.scene.objects['Camera']
    cam.location = (0, 3.0 * distance, 1.0 * distance)

    bpy.ops.render.render(animation=False, write_still=True)
