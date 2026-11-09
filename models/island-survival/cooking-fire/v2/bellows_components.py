"""Visible, editable bellows for the Cooking Fire, based on the supplied references.

Public API (angles in radians; all positions are local to ``parent``):
    build_hand_bellows(collection, parent, location=(0,0,0), yaw=0,
                       scale=1, animate=True)
    build_squeeze_bellows(collection, parent, location=(0,0,0), radius=.25,
                          height=.38, animate=True)

The hand bellows points down local -Y. Its body is .43 wide; with the nozzle
and handles its length is about 1.34. Its mounting underside is Z=0.
Use yaw=-pi/2 to point the nozzle in -X. A .75 scale gives an approximately
1.0-unit assembly from nozzle to handle ends.

The accordion bellows mounts on the Z=0 plane. ``height`` is the open total
wood-cap/body height; two narrow flexible hoses reach about .11 above this.
Both models have a 96-frame squeeze cycle, with frame 0 the resting open pose.
No inherited object, material or animation is edited.
"""
import math
import bpy
from mathutils import Vector


def _object(name, data, collection, parent, material=None):
    obj=bpy.data.objects.new(name,data)
    collection.objects.link(obj)
    obj.parent=parent
    if data is not None and material is not None:
        data.materials.append(material)
    obj['Cooking Fire bellows']=True
    return obj


def _root(name, collection, parent, location):
    obj=_object(name,None,collection,parent)
    obj.location=location
    obj.empty_display_type='PLAIN_AXES'
    obj.empty_display_size=.08
    return obj


def _material(name,low,high,roughness=.8,metallic=0,wood=False):
    material=bpy.data.materials.get(name)
    if material:
        return material
    material=bpy.data.materials.new(name)
    material.use_nodes=True
    n,l=material.node_tree.nodes,material.node_tree.links
    shader=n.get('Principled BSDF')
    shader.inputs['Roughness'].default_value=roughness
    shader.inputs['Metallic'].default_value=metallic
    tex=n.new('ShaderNodeTexCoord')
    mapping=n.new('ShaderNodeVectorMath')
    mapping.operation='MULTIPLY'
    mapping.inputs[1].default_value=(25,2,8) if wood else (20,20,20)
    l.new(tex.outputs['Generated'],mapping.inputs[0])
    noise=n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=2.5 if wood else 3
    noise.inputs['Detail'].default_value=3
    noise.inputs['Roughness'].default_value=.7
    l.new(mapping.outputs[0],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position=.18
    ramp.color_ramp.elements[0].color=(*low,1)
    ramp.color_ramp.elements[1].position=.82
    ramp.color_ramp.elements[1].color=(*high,1)
    l.new(noise.outputs['Fac'],ramp.inputs['Fac'])
    l.new(ramp.outputs['Color'],shader.inputs['Base Color'])
    bump=n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value=.24 if wood else .13
    bump.inputs['Distance'].default_value=.004 if wood else .003
    l.new(noise.outputs['Fac'],bump.inputs['Height'])
    l.new(bump.outputs['Normal'],shader.inputs['Normal'])
    return material


def materials():
    return {
        'wood':_material('Bellows | worn honey wood',(.13,.048,.013),(.44,.235,.075),wood=True),
        'leather':_material('Bellows | oxblood leather',(.055,.011,.006),(.20,.053,.019)),
        'accordion':_material('Bellows | folded brown leather',(.075,.032,.012),(.25,.13,.046)),
        'iron':_material('Bellows | aged iron',(.025,.028,.027),(.09,.09,.078),.69,.72),
        'brass':_material('Bellows | worn brass nozzle and studs',(.15,.071,.022),(.40,.23,.077),.55,.72),
    }


def _mesh(name,verts,faces,collection,parent,material,smooth=False):
    data=bpy.data.meshes.new(name)
    data.from_pydata(verts,[],faces)
    data.update()
    obj=_object(name,data,collection,parent,material)
    for poly in data.polygons:
        poly.use_smooth=smooth
    return obj


def _prism(name,outline,z,thickness,collection,parent,material,bevel=.008):
    count=len(outline)
    verts=[(x,y,z+d) for d in (-thickness/2,thickness/2) for x,y in outline]
    faces=[tuple(reversed(range(count))),tuple(range(count,2*count))]
    faces += [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
    obj=_mesh(name,verts,faces,collection,parent,material)
    if bevel:
        modifier=obj.modifiers.new('Soft worn edges','BEVEL')
        modifier.width=bevel
        modifier.segments=3
    return obj


def _box(name,center,size,collection,parent,material,bevel=.008):
    x,y,z=center
    sx,sy,sz=size
    return _prism(name,[(x-sx/2,y-sy/2),(x+sx/2,y-sy/2),(x+sx/2,y+sy/2),(x-sx/2,y+sy/2)],z,sz,collection,parent,material,bevel)


def _lathe(name,profile,collection,parent,material,segments=64):
    verts=[(r*math.cos(2*math.pi*i/segments),r*math.sin(2*math.pi*i/segments),z) for r,z in profile for i in range(segments)]
    faces=[(j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i) for j in range(len(profile)-1) for i in range(segments)]
    return _mesh(name,verts,faces,collection,parent,material,True)


def _cylinder(name,radius,height,z,collection,parent,material,segments=48):
    obj=_lathe(name,[(.001,z-height/2),(radius,z-height/2),(radius,z+height/2),(.001,z+height/2)],collection,parent,material,segments)
    bevel=obj.modifiers.new('Worn lip','BEVEL')
    bevel.width=min(.008,height*.16)
    bevel.segments=2
    return obj


def _driver(owner,prop,index,control,expression):
    curve=owner.driver_add(prop) if index is None else owner.driver_add(prop,index)
    driver=curve.driver
    driver.type='SCRIPTED'
    var=driver.variables.new()
    var.name='c'
    var.type='SINGLE_PROP'
    var.targets[0].id=control
    var.targets[0].data_path='["compression"]'
    driver.expression=expression
    return curve


def _control(root,animate):
    root['compression']=0.0
    root.id_properties_ui('compression').update(min=0,max=1,description='0 open; 1 squeezed; linked cap and leather deformation')
    if animate:
        for frame,value in [(0,0),(1,0),(25,.5),(49,1),(73,.5),(97,0)]:
            # ID properties may change type on assignment. Keep every authored
            # value floating-point so Blender does not mark this curve discrete.
            root['compression']=float(value)
            root.keyframe_insert(data_path='["compression"]',frame=frame)
        if root.animation_data and root.animation_data.action:
            for fc in root.animation_data.action.fcurves:
                fc.update_autoflags(root)
                for point in fc.keyframe_points:
                    point.interpolation='BEZIER'
                    point.handle_left_type=point.handle_right_type='AUTO_CLAMPED'
        root['compression']=0.0


def _shape_driver(obj,closed,root):
    obj.shape_key_add(name='Open')
    key=obj.shape_key_add(name='Compressed')
    for vertex,co in zip(key.data,closed):
        vertex.co=co
    _driver(key,'value',None,root,'c')
    return key


def _tube(name,points,radius,collection,parent,material):
    data=bpy.data.curves.new(name,'CURVE')
    data.dimensions='3D'
    data.resolution_u=12
    data.bevel_depth=radius
    data.bevel_resolution=3
    data.use_fill_caps=True
    spline=data.splines.new('BEZIER')
    spline.bezier_points.add(len(points)-1)
    for bp,p in zip(spline.bezier_points,points):
        bp.co=p
        bp.handle_left_type=bp.handle_right_type='AUTO'
    return _object(name,data,collection,parent,material)


def build_hand_bellows(collection,parent,location=(0,0,0),yaw=0,scale=1,animate=True):
    """Wood boards, an actual leather gusset, handles and a tapered hollow nozzle.

    Place the underside on a mounting support; the function does not invent a
    stand. Local nozzle plane is (0,-.66,.078), directed toward local -Y.
    """
    before=set(bpy.data.objects)
    m=materials()
    root=_root('Bellows | hand assembly',collection,parent,location)
    root.rotation_euler.z=yaw
    root.scale=(scale,scale,scale)
    root['Reference']='User wooden/leather hand-bellows photograph'
    _control(root,animate)
    right=[(0,-.43),(.053,-.405),(.093,-.30),(.151,-.12),(.203,.065),(.216,.18),(.184,.285),(.118,.36),(0,.39)]
    outline=right+[(-x,y) for x,y in reversed(right[1:-1])]
    # Mounting pads keep the lowest visible geometry exactly at Z=0.
    _box('Bellows | lower front mounting strip',(0,-.27,.013),(.15,.07,.026),collection,root,m['wood'])
    _box('Bellows | lower rear mounting strip',(0,.23,.013),(.31,.07,.026),collection,root,m['wood'])
    bottom_z=.044
    _prism('Bellows | lower wooden paddle',outline,bottom_z,.036,collection,root,m['wood'])
    _box('Bellows | lower handle',(0,.51,bottom_z),(.068,.40,.036),collection,root,m['wood'],.018)
    hinge_y=-.425
    hinge_z=.078
    top=_root('Bellows | moving upper paddle hinge',collection,root,(0,hinge_y,hinge_z))
    open_angle=math.radians(21)
    close_angle=math.radians(8)
    travel=open_angle-close_angle
    top.rotation_euler.x=open_angle
    _driver(top,'rotation_euler',0,root,f'{open_angle}-{travel}*c')
    top_outline=[(x,y-hinge_y) for x,y in outline]
    _prism('Bellows | upper wooden paddle',top_outline,0,.036,collection,top,m['wood'])
    _box('Bellows | upper handle',(0,.51-hinge_y,0),(.068,.40,.036),collection,top,m['wood'],.018)
    # One broad leather pouch follows both boards, including the changing Y
    # projection of the hinged top. This is not a flattened texture plane.
    def gusset_verts(angle):
        result=[]
        for fraction,bulge in [(0,0),(.20,.014),(.50,.028),(.80,.017),(1,0)]:
            for x,y in outline:
                top_y=hinge_y+(y-hinge_y)*math.cos(angle)+.018*math.sin(angle)
                top_z=hinge_z+(y-hinge_y)*math.sin(angle)-.018*math.cos(angle)
                low=Vector((x,y,.062))
                high=Vector((x,top_y,top_z))
                co=low.lerp(high,fraction)
                radial=Vector((x,y+.03,0))
                if radial.length:
                    co += radial.normalized()*bulge*max(0,min(1,(y+.43)/.25))
                result.append(tuple(co))
        return result
    count=len(outline)
    faces=[(j*count+i,j*count+(i+1)%count,(j+1)*count+(i+1)%count,(j+1)*count+i) for j in range(4) for i in range(count)]
    leather=_mesh('Bellows | folding leather pouch',gusset_verts(open_angle),faces,collection,root,m['leather'],True)
    _shape_driver(leather,gusset_verts(close_angle),root)
    # Small visible perimeter studs mirror the reference; no unrelated hardware.
    for i in (2,4,6,8,10,12,14):
        x,y=outline[i]
        x*=.91
        for label,par,px,py,pz in [('bottom',root,x,y,.063),('top',top,x,y-hinge_y,.019)]:
            stud=_lathe(f'Bellows | {label} leather stud {i}',[(.001,0),(.012,0),(.011,.006),(.006,.012),(.001,.013)],collection,par,m['brass'],segments=12)
            stud.location=(px,py,pz)
    nozzle=_lathe('Bellows | tapered hollow air nozzle',[(.052,0),(.050,.04),(.025,.235),(.018,.235),(.020,.21),(.035,.015),(.052,0)],collection,root,m['brass'],segments=48)
    nozzle.rotation_euler.x=math.pi/2
    nozzle.location=(0,-.425,.078)
    collar=_cylinder('Bellows | nozzle leather collar',.061,.054,0,collection,root,m['leather'])
    collar.rotation_euler.x=math.pi/2
    collar.location=(0,-.425,.078)
    root['Local nozzle plane']=[0,-.66,.078]
    return {'root':root,'objects':[o for o in bpy.data.objects if o not in before],
            'top_rig':top,'leather':leather,'nozzle_local':(0,-.66,.078),
            'nozzle_normal_local':(0,-1,0),'foot_z':0,'open_angle':open_angle,
            'compressed_angle':close_angle}


def build_squeeze_bellows(collection,parent,location=(0,0,0),radius=.25,height=.38,animate=True):
    """Six leather accordion folds between wood caps, plus two flexible top lines.

    The fixed base sits on Z=0. All visible hoses deform with the lid at their
    top ends and terminate at the fixed pump-box mounting plane.
    """
    before=set(bpy.data.objects)
    m=materials()
    root=_root('Bellows | accordion pump assembly',collection,parent,location)
    root['Reference']='User accordion/squeeze-bellows photograph; wood and leather adaptation'
    _control(root,animate)
    cap_thickness=.045
    z0=cap_thickness
    z1=height-cap_thickness
    travel=(z1-z0)*.40
    base=_cylinder('Bellows | fixed lower wood cap',radius*1.05,cap_thickness,cap_thickness/2,collection,root,m['wood'])
    # Each pleat has an actual wide crest, valley and sloping leather faces.
    profile=[(radius*.67,z0)]
    folds=6
    for fold in range(folds):
        pitch=(z1-z0)/folds
        z=z0+fold*pitch
        profile += [(radius*.94,z+.28*pitch),(radius,z+.48*pitch),(radius*.94,z+.68*pitch),(radius*.67,z+pitch)]
    shell=_lathe('Bellows | six compressible leather pleats',profile,collection,root,m['accordion'],segments=64)
    closed=[(v.co.x,v.co.y,z0+(v.co.z-z0)*(1-travel/(z1-z0))) for v in shell.data.vertices]
    _shape_driver(shell,closed,root)
    lid=_root('Bellows | moving upper wood cap',collection,root,(0,0,z1+cap_thickness/2))
    _driver(lid,'location',2,root,f'{z1+cap_thickness/2}-{travel}*c')
    _cylinder('Bellows | upper circular wood cap',radius*1.05,cap_thickness,0,collection,lid,m['wood'])
    # A narrow central push plate makes the compression direction readable.
    _cylinder('Bellows | small iron push plate',radius*.42,.016,cap_thickness/2+.008,collection,lid,m['iron'])
    ports=[]
    for sign in (-1,1):
        px=sign*radius*.36
        ferrule=_cylinder('Bellows | left top ferrule' if sign<0 else 'Bellows | right top ferrule',.025,.045,cap_thickness/2+.018,collection,lid,m['brass'])
        ferrule.location.x=px
        points=[(px,0,height+.035),(sign*radius*.54,.025,height+.11),(sign*radius*.93,.11,height+.045),(sign*radius*1.12,.13,height*.45),(sign*radius*1.12,.12,0)]
        line=_tube('Bellows | left flexible pump line' if sign<0 else 'Bellows | right flexible pump line',points,.019,collection,root,m['leather'])
        for bp,point,weight in zip(line.data.splines[0].bezier_points,points,(1,1,.8,.25,0)):
            _driver(bp,'co',2,root,f'{point[2]}-{travel*weight}*c')
        ports.append({'upper_local':(px,0,height+.035),'fixed_lower_local':points[-1]})
    root['Open height']=height
    root['Compression travel']=travel
    return {'root':root,'objects':[o for o in bpy.data.objects if o not in before],
            'top_cap':lid,'leather':shell,'ports':ports,'foot_z':0,
            'open_height':height,'compressed_height':height-travel,
            'outer_radius':radius*1.05,'fold_count':folds}
