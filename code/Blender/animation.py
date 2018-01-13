import os
import bpy
import json

context = bpy.context
data = bpy.data
ops = bpy.ops
origin = (0, 0, 0)

# Helper functions

def create_sphere(r, name):
    '''
    Creates a sphere in blender of a given radius with a given name

    r -- radius of sphere
    name -- name of sphere
    '''
    bpy.ops.mesh.primitive_uv_sphere_add(location = (0,0,r), size = r)
    bpy.data.objects['Sphere'].name = name
    #bpy.data.objects['ball'].active_material.diffuse_color = (1.0, 0.0, 0.0)
    
def create_plane(radius):
    '''
    Creates a plane of a given radius

    radius -- radius of plane
    '''
    loc = (radius,radius,0)
    bpy.ops.mesh.primitive_plane_add(radius = radius, location = loc)
    
def create_background(centerx, centery, r):
    me_background = data.meshes.new("BackgroundMesh")
    background = data.objects.new("background", me_background)
    scn = context.scene
    scn.objects.link(background)
    scn.objects.active = background
    background.select = True

    background_verts = [(centerx-r, centery-r, -1), (centerx-r, centery+r, -1), (centerx+r, centery+r, -1), (centerx+r, centery-r, -1)]
    background_faces = [[0, 1, 2, 3]]

    me_background.from_pydata(background_verts, [], background_faces)

    me_background.update()

def create_material(r, g, b):
    new_material = data.materials.new(name="MyNewMaterial")
    new_material.diffuse_color = (r, g, b)
    return new_material

def create_empty_material():
    new_material = data.materials.new(name="MyNewMaterial")
    return new_material

def assign_materials(ob, mat):
    if data.objects[ob].data.materials:
       data.objects[ob].data.materials[0] = mat
    else:
        data.objects[ob].data.materials.append(mat)     

# Main

def init():
    # Unpack json file for a given simulation
    simulation_data = json.load(open('simulation.json'))
    radius = simulation_data['config']['scene']/100.0
    # simulation_id = simulation_data['config']['id']

    #Camera Settings
    data.objects['Camera'].location.x = radius/2.0 #new_data['config']['med']
    data.objects['Camera'].location.y = radius/2.0 #new_data['config']['med']
    data.objects['Camera'].location.z = 20
    
    data.objects['Camera'].rotation_euler.x = 0
    data.objects['Camera'].rotation_euler.y = 0
    data.objects['Camera'].rotation_euler.z = 0
    
    #Lamp Settings
    data.objects['Lamp'].location.x = 0 #new_data['config']['med']
    data.objects['Lamp'].location.y = 0 #new_data['config']['med']
    data.objects['Lamp'].location.z = 5
    
    ball_r = 0.3 #new_data['config']['ball_radius']
    
    agent_mat = create_material(0, 0, 1)
    patient_mat = create_material(0, 1, 0)
    fireball_mat = create_material(1, 0, 0)
    plane_mat = create_empty_material()
    
    create_sphere(ball_r, 'agent')
    create_sphere(ball_r, 'patient')
    create_sphere(ball_r, 'fireball')
    create_plane(radius)
    
    context.scene.camera.data.clip_start = 0
    context.scene.camera.data.clip_end = 100
    
    assign_materials('agent', agent_mat)
    assign_materials('patient', patient_mat)
    assign_materials('fireball', fireball_mat)

    for idx in range(simulation_data['config']['ticks']): #range(len(new_data['data']['ball'])):
        data.scenes['Scene'].render.filepath = './images/image%d.jpg' %idx
        ops.render.render(write_still = True)
        
        data.objects['agent'].location.x = (simulation_data['objects']['agent'][idx]['x']/100.0)
        data.objects['agent'].location.y = ((simulation_data['objects']['agent'][idx]['y']/100.0) + 2)

        data.objects['patient'].location.x = (simulation_data['objects']['patient'][idx]['x']/100.0)
        data.objects['patient'].location.y = ((simulation_data['objects']['patient'][idx]['y']/100.0) + 2)

        data.objects['fireball'].location.x = (simulation_data['objects']['fireball'][idx]['x']/100.0)
        data.objects['fireball'].location.y = ((simulation_data['objects']['fireball'][idx]['y']/100.0) + 2)
        
    bpy.ops.view3d.camera_to_view_selected()
    
    
def clear_textures():
    for tex in data.textures:
        data.textures.remove(tex)

def kill_meshes():
    bpy.ops.object.select_by_type(type='MESH')
    # remove all selected.
    bpy.ops.object.delete()

    # remove the meshes, they have no users anymore.
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
        
clear_textures()
kill_meshes()
init()
