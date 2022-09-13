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
        print('mat_name', mat_name)
        return mat_name
    return None

selected_list = cmds.ls(sl=True)    


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
        if mat_name and validate_material(mat_name, all_materials):
            assign_material(mat_name)
    

if __name__ =='__main__':
    main()