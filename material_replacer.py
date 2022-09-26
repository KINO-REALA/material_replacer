from maya import cmds
import re

def get_all_materials():
    all_materials = cmds.ls(mat=True)
    print(all_materials)
    return all_materials

def validate_material(mat_name, all_materials):   
    if mat_name in all_materials:
        return True
    else:
        cmds.warning('Material not found: {}'.format(mat_name))
        return False

def get_material_name_from_object(obj):
    result = re.search('_\d{3}', obj)
    if result:
        num = result.group()
        mat = obj.split('_')[-2]
        mat_name = mat+num
        return mat_name
    return None

def get_current_material_name(obj):
    cmds.select(obj)
    # get shapes of selection:
    shapes =  cmds.ls(dag=True,o=True,s=True,sl=True)
    if len(shapes)>1:
        print('{} is group object'.format(obj))
        return None
    # get shading groups from shapes:
    shading_grps = cmds.listConnections(shapes,type='shadingEngine')
    # get the shaders:
    shaders = cmds.ls(cmds.listConnections(shading_grps), materials=True)
    if len(shaders)>1:
        cmds.warning('{} has more than one material.'.format(obj))
    if len(shaders)==1:
        return shaders[0]
    if len(shaders)==0:
        cmds.warning('{} has more than one shape.'.format(obj))
        return None

def assign_material(mat_name):
    if mat_name:
        cmds.hyperShade(a=mat_name)

def list_all_children(nodes):    
    result = set()
    children = set(cmds.listRelatives(nodes, fullPath=True) or [])
    while children:
        result.update(children)
        children = set(cmds.listRelatives(children, fullPath=True) or []) - result
        
    return list(result)

def main():
    all_materials = get_all_materials()
    parent = cmds.ls(sl=True)[0]
    objs = list_all_children(parent)
    for obj in objs:
        mat_name = get_material_name_from_object(obj)
        current_mat = get_current_material_name(obj)
        if mat_name and validate_material(mat_name, all_materials):
            if mat_name != current_mat:
                assign_material(mat_name)
                print('Object: {}, Material:{} >>> {}'.format(obj, current_mat, mat_name))
    

if __name__ =='__main__':
    main()

