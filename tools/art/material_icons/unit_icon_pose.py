"""Item presentation in camera coordinates; FMPL optics remain fixed."""
import math
from mathutils import Matrix,Vector
PRESETS={'A':dict(end_view=5,top_view=8),'B':dict(end_view=8,top_view=12),'C':dict(end_view=12,top_view=18)}
def pose_matrix(diagonal=35,end_view=8,top_view=12):
    diagonal=math.radians(diagonal);depth=math.sin(math.radians(end_view))
    right=Vector((1,0,0));up=Vector((0,math.sqrt(.5),math.sqrt(.5)))
    view=Vector((0,-math.sqrt(.5),math.sqrt(.5)))
    forward=(right*math.cos(diagonal)+up*math.sin(diagonal))*math.sqrt(1-depth*depth)-view*depth
    side=(view-forward*view.dot(forward)).normalized()
    model_y=-side;model_up=forward.cross(model_y).normalized()
    roll=math.radians(top_view)
    y=model_y*math.cos(roll)+model_up*math.sin(roll)
    z=model_up*math.cos(roll)-model_y*math.sin(roll)
    return Matrix((forward,y,z)).transposed().to_4x4()
