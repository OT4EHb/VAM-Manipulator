import time
import traceback

from Agilebot.IR.A.arm import Arm
from Agilebot.IR.A.status_code import StatusCodeEnum
from Agilebot.IR.A.sdk_types import RobotStatusEnum, ParamType, CoordinateSystemType
from Agilebot.IR.A.motion import init_motion_instruction

import Agilebot.IR.A.sdk_classes as classes
from Agilebot.IR.A.common.const import const

from pyDHgripper import RGD
import time

def main():
    arm = Arm()
    ret = arm.connect("10.27.1.254")
    
    gripper = RGD(port='COM3')
    time.sleep(3)

    # print(gripper.read_state())
    # while gripper.read_state() != 1:
    #     print(gripper.read_state())
    #     time.sleep(0.05)
    
    try:
        assert ret == StatusCodeEnum.OK

        assert arm.motion.set_param(param_name=ParamType.UF, param_value=0) == StatusCodeEnum.OK
        assert arm.motion.set_param(param_name=ParamType.TF, param_value=0) == StatusCodeEnum.OK
        # текущее положение joint или декартовы
        pose, ret = arm.motion.get_current_pose(const.JOINT,0,0)
        assert ret == StatusCodeEnum.OK
        printPose(pose)

        # pose.joint.j1 += 2
        # pose.joint.j2 -= 1

        pose.cartData.posture = None # posture
        # position = pose.cartData.position
        # position.x=0
        # position.y-=10
        # position.z+=20

        # position.x = 201.32422690155244
        # position.y = 801.3035379086845
        # position.z = 867.5966831987303
        # position.a = 54.65851646596859
        # position.b = 68.60407292110962
        # position.c = 60.045417745984444
        printPose(pose)

        while gripper.read_state() != 1:
            time.sleep(0.05)

        pose.joint.j2 -= 3
        ret = arm.motion.move_to_pose(pose, const.MOVE_JOINT)
        assert ret == StatusCodeEnum.OK
        while arm.get_robot_status()[1] != RobotStatusEnum.ROBOT_IDLE:
            time.sleep(0.5)

        gripper.set_pos(val=0, blocking=False)
        # while gripper.read_state() != 1:
        #     time.sleep(0.05)

        pose.joint.j2 += 3
        ret = arm.motion.move_to_pose(pose, const.MOVE_JOINT)
        assert ret == StatusCodeEnum.OK
        while arm.get_robot_status()[1] != RobotStatusEnum.ROBOT_IDLE:
            time.sleep(0.5)

        gripper.set_pos(val=1000, blocking=True)
        # while gripper.read_state() != 1:
        #     time.sleep(0.05)


    except AssertionError:
        print(f"{ret.code} {ret}")
        print(traceback.print_exc())
    finally:
        arm.disconnect()

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

if __name__ == "__main__":
    main()