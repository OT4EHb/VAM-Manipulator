import time
import traceback

from print_utils import *

from Agilebot.IR.A.arm import Arm
from Agilebot.IR.A.status_code import StatusCodeEnum
from Agilebot.IR.A.sdk_types import RobotStatusEnum, ParamType, CoordinateSystemType
from Agilebot.IR.A.motion import init_motion_instruction

arm = Arm()
ret = arm.connect("10.27.1.254")
try:
    assert ret == StatusCodeEnum.OK

    assert arm.motion.set_param(param_name=ParamType.UF, param_value=0) == StatusCodeEnum.OK
    assert arm.motion.set_param(param_name=ParamType.TF, param_value=0) == StatusCodeEnum.OK
    # текущее положение joint или декартовы
    pose, ret = arm.motion.get_current_pose(const.CART,0,0)
    assert ret == StatusCodeEnum.OK
    printPose(pose)
    pose.joint.j1 += 20
    pose.cartData.posture = None # posture
    position = pose.cartData.position
    position.x=0
    position.y-=10
    position.z+=20

    # position.x = 201.32422690155244
    # position.y = 801.3035379086845
    # position.z = 867.5966831987303
    # position.a = 54.65851646596859
    # position.b = 68.60407292110962
    # position.c = 60.045417745984444
    printPose(pose)
    ret = arm.motion.move_to_pose(pose, const.MOVE_JOINT)
    assert ret == StatusCodeEnum.OK
    while arm.get_robot_status()[1] != RobotStatusEnum.ROBOT_IDLE:
        time.sleep(0.5)
except AssertionError:
    print(f"{ret.code} {ret}")
    print(traceback.print_exc())
finally:
    arm.disconnect()
