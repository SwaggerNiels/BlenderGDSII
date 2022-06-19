r'''blender execute:
cd "C:\Program Files\Blender Foundation\Blender 3.1"
.\blender.exe --factory-startup -P "<PATH>\bpy_import_stls.py"
'''

import bpy
import glob
import mathutils
import sys
from random import random
import os

RANDOM_MAT = 0
STD_thickness = 100 #[nm]

try:
    index = sys.argv.index('--') + 1
except ValueError:
    index = len(sys.argv)
argv = sys.argv[index:]

print(argv)

if len(argv) < 2:
    print("Error: Need path of the stl files")
    sys.exit(0)
stl_folder_path = argv[0]
material_blend_path = argv[1]
check_stack = argv[2]
layer_stack = argv[3]
material_stack = argv[4]
dimension_stack = argv[5]

glob_search = stl_folder_path + r'\*.stl'
print(f'Looking for stl files:\n{glob_search}')
stl_files = glob.glob(glob_search)
print(f'found: {stl_files}')

stl_checks = check_stack.split(',')
stl_checks = [0 if check=='' else 1 for check in stl_checks]
stl_layers = layer_stack.split(',')
stl_materials = material_stack.split(',')
stl_dimensions = dimension_stack.split(',')
stl_dimensions = [tuple(map(int,pair[1:-1].split(';'))) if pair!='(;)' else (0,STD_thickness) for pair in stl_dimensions]

#import materials
with bpy.data.libraries.load(material_blend_path, link=False) as (data_from, data_to):
    data_to.materials = data_from.materials
print('Materials imported')

def update_camera(camera, focus_point=mathutils.Vector((0.0, 0.0, 0.0)), distance=10.0):
    """
    Focus the camera to a focus point and place the camera at a specific distance from that
    focus point. The camera stays in a direct line with the focus point.

    :param camera: the camera object
    :type camera: bpy.types.object
    :param focus_point: the point to focus on (default=``mathutils.Vector((0.0, 0.0, 0.0))``)
    :type focus_point: mathutils.Vector
    :param distance: the distance to keep to the focus point (default=``10.0``)
    :type distance: float
    """
    looking_direction = camera.location - focus_point
    rot_quat = looking_direction.to_track_quat('Z', 'Y')

    camera.rotation_euler = rot_quat.to_euler()
    # Use * instead of @ for Blender <2.8
    camera.location = rot_quat @ mathutils.Vector((0.0, 0.0, distance))

bpy.data.objects['Cube'].select_set(True)
bpy.data.objects['Light'].select_set(True)
bpy.ops.object.delete(use_global=False)

for stl_check,stl_layer,stl_material,stl_dimension in zip(stl_checks,stl_layers,stl_materials,stl_dimensions):
    if stl_check:
        #find file
        filename = ''
        for f in [f for f in stl_files if f.endswith(f'_{stl_layer}.stl')]:
            filename = f
        
        if filename != '':
            print(f'Blender - Importing {filename}')
            obj = bpy.ops.import_mesh.stl(filepath=filename)
            obj_name = filename.split('\\')[-1][:-4]
            mat_name = obj_name + '_material'

            bpy.data.objects[obj_name].select_set(True)
            ob = bpy.context.active_object
            
            #apply material
            if RANDOM_MAT:
                # Get material
                mat = bpy.data.materials.new(name=mat_name)
                mat.diffuse_color = random(), random(), random(), 1

                # Assign it to object
                if ob.data.materials:
                    # assign to 1st material slot
                    ob.data.materials[0] = mat
                else:
                    # no slots
                    ob.data.materials.append(mat)
            else:
                mat = bpy.data.materials[stl_material]
                
                if ob.data.materials:
                    # assign to 1st material slot
                    ob.data.materials[0] = mat
                else:
                    # no slots
                    ob.data.materials.append(mat)

            #apply dimensions
            lbound, ubound = stl_dimension #lower and upper bound
            desired_thickness = ubound-lbound

            factor_z = desired_thickness/STD_thickness
            bpy.ops.transform.resize(value=(1, 1, factor_z))
            bpy.ops.transform.translate(value=(0, 0, lbound))

            bpy.data.objects[obj_name].select_set(False)
        else:
            print(f'Layer {stl_layer} not made yet, cant be used...')
    else:
        print(f'Layer {stl_layer} not imported')

bpy.ops.object.select_all(action='SELECT')
bpy.data.objects['Camera'].select_set(False)

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        ctx = bpy.context.copy()
        ctx['area'] = area
        ctx['region'] = area.regions[-1]
        
        clip_start_value = 10
        clip_end_value = 1e6
        for s in area.spaces:
            if s.type == 'VIEW_3D':
                s.clip_start = clip_start_value
                s.clip_end = clip_end_value
                s.shading.type = 'MATERIAL'
                # bpy.ops.image.open(filepath="C:\\Program Files\\Blender Foundation\\Blender 3.1\\3.1\\datafiles\\studiolights\\world\\forest.exr", directory="C:\\Program Files\\Blender Foundation\\Blender 3.1\\3.1\\datafiles\\studiolights\\world\\", files=[{"name":"forest.exr", "name":"forest.exr"}], show_multiview=False)

        bpy.data.objects['Camera'].data.clip_start = clip_start_value
        bpy.data.objects['Camera'].data.clip_end = clip_end_value

        bpy.ops.view3d.view_selected(ctx)            # points view
        bpy.ops.view3d.camera_to_view_selected(ctx)   # points camera

bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0), rotation=(0.261799, 0.261799*2, 0), scale=(1, 1, 1))
bpy.data.objects["Sun"].select_set(True)
ob = bpy.context.active_object
ob.data.energy = 5000
bpy.data.objects["Sun"].select_set(False)

bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_ssr_refraction = True
bpy.context.scene.render.film_transparent = True


bpy.ops.object.select_all(action='DESELECT')
