import Agilebot.IR.A.sdk_classes as classes
from Agilebot.IR.A.common.const import const


def printPosture(posture: classes.Posture):
    print("Posture:")
    if not isinstance(posture, classes.Posture):
        print(None)
        return
    print(f"turenCircle: {posture.turnCircle}")
    print(f"wrist_flip: {posture.wrist_flip}")
    print(f"arm_up_down: {posture.arm_up_down}")
    print(f"arm_back_front: {posture.arm_back_front}")
    print(f"arm_left_right: {posture.arm_left_right}")


def printPosition(position: classes.Position):
    print("Position:")
    print(f"x: {position.x}")
    print(f"y: {position.y}")
    print(f"z: {position.z}")
    print(f"a: {position.a}")
    print(f"b: {position.b}")
    print(f"c: {position.c}")


def printCart(cartData: classes.BaseCartData):
    print("CartData:")
    printPosture(cartData.posture)
    printPosition(cartData.position)


def printJoint(joint: classes.Joint):
    print("Joint:")
    print(f"j1: {joint.j1}")
    print(f"j2: {joint.j2}")
    print(f"j3: {joint.j3}")
    print(f"j4: {joint.j4}")
    print(f"j5: {joint.j5}")
    print(f"j6: {joint.j6}")


def printPose(pose: classes.MotionPose):
    print("MotionPose:")
    print(f"pt: {pose.pt}")
    if pose.pt != const.JOINT:
        printCart(pose.cartData)
    elif pose.pt != const.CART:
        printJoint(pose.joint)
