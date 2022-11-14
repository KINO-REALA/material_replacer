from maya import cmds
import pymel.core as pm

obj_ls = cmds.ls(sl=True)
for obj in obj_ls:
    point_count = cmds.polyEvaluate(vertex=True)
    
    center_point = [0, 0, 0]
    for num in range(point_count):
        print(obj, num)
        pos = cmds.xform('{}.vtx[{}]'.format(obj, num), ws=True, q=True, t=True)
        center_point[0] = center_point[0] + pos[0]/(point_count)
        center_point[1] = center_point[1] + pos[1]/(point_count)
        center_point[2] = center_point[2] + pos[2]/(point_count)
        print(pos, center_point)
    
    cmds.move(center_point[0], center_point[1], center_point[2], obj + '.scalePivot', obj + '.rotatePivot', rpr=1)

    #target = cmds.group(n = 'aim_target', w=True, em=True)
    target = 'target'
    print(center_point)        
    normal_group = cmds.group(n = '{}_normal_grp'.format(obj), w=True, em=True)
    cmds.xform(normal_group, t=center_point, ws=True)
    const = cmds.aimConstraint(target, normal_group, aim=(0,0,1), u=(0,1,0))
    cmds.delete(const)
    #cmds.delete(target)

    cmds.select(normal_group)
    #cmds.makeIdentity(apply=True, t=True, r=False, s=False, n=False)
    
    cmds.parent(obj, normal_group)
    cmds.select(obj)
    cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)
