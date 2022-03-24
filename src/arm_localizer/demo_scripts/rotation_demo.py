from turtle import color

from arm_localizer.arm_localizer import Vector
import matplotlib.pyplot as plt
from math import radians, degrees

X_AXIS = Vector(1,0,0)
Y_AXIS = Vector(0,1,0)
Z_AXIS = Vector(0,0,1)

def show_gen_vectors(vectors):
    og = Vector(0,0,0)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x,y,z = og.as_point()

    for v in vectors:
        a,b,c = v.as_point()
        ax.plot([x,a],[y,b],[z,c], color='k')
        ax.scatter(a,b,c,marker="^", color='k')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([0,1])
    plt.show()    

def show_rotation(cam_vec, pos_vec, rot, og):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x,y,z = og.as_point()

    for pt,col in zip([cam_vec, pos_vec, rot],['b','r', 'k']):
        a,b,c = pt.as_point()
        ax.plot([x,a],[y,b],[z,c], color=col)
        ax.scatter(a,b,c,marker="^", color='k')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([0,1])
    plt.show()

def show_all_vectors(cam_claw_1, cam_claw_2, pos_claw_1, pos_claw_2, cam_obj, pos_obj, og, norm=None):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x,y,z = og.as_point()

    for pt,col in zip([cam_obj, pos_obj],['y','g']):
        a,b,c = pt.as_point()
        ax.plot([x,a],[y,b],[z,c], color=col)
        ax.scatter(a,b,c,marker="^", color='k')

    for pt,col in zip([cam_claw_1, cam_claw_2],['c','m']):
        a,b,c = pt.as_point()
        ax.plot([x,a],[y,b],[z,c], color='b')
        ax.scatter(a,b,c,marker="^", color=col)

    for pt,col in zip([pos_claw_1,pos_claw_2],["c","m"]):
        a,b,c = pt.as_point()
        ax.plot([x,a],[y,b],[z,c], color='r')
        ax.scatter(a,b,c,marker="^", color=col)

    if norm != None:
        a,b,c = norm.as_point()
        ax.plot([x,a],[y,b],[z,c], color='k')
        ax.scatter(a,b,c,marker="^", color='k')
    
    ax.scatter(x,y,z, marker="o")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([0,1])
    plt.show()

def apply_rotation(v:Vector,x,y,z):
    v = v.rotate_about_vector(X_AXIS,radians(x))
    v = v.rotate_about_vector(Y_AXIS,radians(y))
    v = v.rotate_about_vector(Z_AXIS,radians(z))
    return v


og = Vector(0,0,0)
cam_obj = Vector(.5, .65, .2)

cam_claw_1 = Vector(1,1,1)
cam_claw_2 = Vector(-.5, -.7, .8)

rx = 10
ry = -4
rz = 100


print(f"suppose camera is tilted up {rx} degrees, twisted {ry} degrees from level, and the robot",
    " arm is spun {rz} degrees. ")

print(f"the camera reads the positions of the claw and the object to be {cam_claw_1} and {cam_obj} respectively")

pos_claw_1 = apply_rotation(cam_claw_1, rx, ry, rz)
pos_claw_2 = apply_rotation(cam_claw_2, rx, ry, rz)
pos_obj = apply_rotation(cam_obj, rx, ry, rz)

print(f"the positioning system gives a different claw position: {pos_claw_1}. it's magnitude is equal and",
    " probably most importantly, it's angle of incidence with the object is the same, however,",
    " there are infinitely many rotations to fix resolve the two coordinate systems")
show_gen_vectors([cam_claw_1,cam_obj])


print(f"")
# pos_obj = cam_obj.rotate_about_vector(Vector(0,1,0), radians(45))
# pos_claw_1 = cam_claw_1.rotate_about_vector(Vector(0,1,0), radians(45))
# pos_claw_2 = cam_claw_2.rotate_about_vector(Vector(0,1,0), radians(45))

print(cam_claw_1, cam_claw_2)

print("Red lines are vectors from pos system, blue are from camera;\n",
        "cyan marker is claw position1, magenta marker is claw position2,",
        " green marker is object position")

show_all_vectors(cam_claw_1=cam_claw_1, cam_claw_2=cam_claw_2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)

f_rot_vector = cam_claw_1.cross(pos_claw_1)
f_rot_rads = cam_claw_1.angle_between(pos_claw_1)

print(f"spin vector camera claw position 1 about vector: {f_rot_vector}, {degrees(f_rot_rads)} degrees",
"to line up with positioning system claw position 1")

show_rotation(cam_claw_1, pos_claw_1, f_rot_vector, og)

cam_claw_1 = cam_claw_1.rotate_about_vector(f_rot_vector.unit(),f_rot_rads)

print(cam_claw_1)
print("note that now, both claw one vectors are now aligned")
show_all_vectors(cam_claw_1=cam_claw_1, cam_claw_2=cam_claw_2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)
print("now apply that rotation to the cam_claw_2 vector. After applying it, we get this:")
cam_claw_2 = cam_claw_2.rotate_about_vector(f_rot_vector.unit(),f_rot_rads)
show_all_vectors(cam_claw_1=cam_claw_1, cam_claw_2=cam_claw_2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)
print("now we will rotate cam_claw_2 about the colinear claw_1 vectors to line it up with\n",
        "pos_claw_2")
print("this requires some math")
#perpendicular to c1 ie the now colinear claw 1 vectors
#to find the angle of rotation, we don't want the angle beween cam_claw2 and pos_claw2 anymore,
# we want the angle between their components which are orthogonal to colinear claw1 vectors so...
#***after it has undergone the first rotation
s_rot_vector = cam_claw_1
cc2_perp = cam_claw_2 - cam_claw_2.project(s_rot_vector)
pc2_perp = pos_claw_2 - pos_claw_2.project(s_rot_vector)
s_rot_rads = cc2_perp.angle_between(pc2_perp)

print("so we will spin the rotated camera claw position 2 vector ",
    f"about the colinear claw position1 vector {degrees(s_rot_rads)} degrees")
show_rotation(cam_claw_2, pos_claw_2,s_rot_vector,og)

cam_claw_2 = cam_claw_2.rotate_about_vector(s_rot_vector.unit(), s_rot_rads)

show_all_vectors(cam_claw_1=cam_claw_1, cam_claw_2=cam_claw_2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)

print("now applying both of those rotations to the object vector from the camera system will \n",
    "tell us the position of the object relative to the positioning system")

cam_obj=cam_obj.rotate_about_vector(f_rot_vector,f_rot_rads)
cam_obj=cam_obj.rotate_about_vector(s_rot_vector,s_rot_rads)

show_all_vectors(cam_claw_1=cam_claw_1, cam_claw_2=cam_claw_2, pos_claw_1=pos_claw_1, pos_claw_2=pos_claw_2, cam_obj=cam_obj, pos_obj=pos_obj, og=og)
