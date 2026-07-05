import time
import traceback
from typing import Optional, Tuple
from dataclasses import dataclass
import logging

from Agilebot.IR.A.arm import Arm
from Agilebot.IR.A.status_code import StatusCodeEnum
from Agilebot.IR.A.sdk_types import RobotStatusEnum, ParamType
from Agilebot.IR.A.motion import init_motion_instruction
from Agilebot.IR.A.sdk_classes import MotionPose
from Agilebot.IR.A.common.const import const
from pyDHgripper import RGD

logger = logging.getLogger(__name__)


@dataclass
class RobotConfig:
    ip: str = "10.27.1.254"
    gripper_port: str = "COM3"
    uf_param: int = 0  # User Frame
    tf_param: int = 0  # Tool Frame


class RobotController:
    def __init__(self, config: Optional[RobotConfig] = None):
        self.config = config or RobotConfig()
        self.arm: Optional[Arm] = None
        self.gripper: Optional[RGD] = None
        self.is_connected = False

    def connect(self) -> bool:
        try:
            logger.info(f"Подключение к роботу {self.config.ip}...")
            self.arm = Arm()
            ret = self.arm.connect(self.config.ip)

            if ret != StatusCodeEnum.OK:
                logger.error(f"Ошибка подключения к роботу: {ret}")
                return False

            logger.info("Подключение к захвату...")
            self.gripper = RGD(port=self.config.gripper_port)
            time.sleep(3)
            if not self._wait_for_gripper_ready():
                logger.warning("Захват не готов к работе")

            self._setup_motion_parameters()

            self.is_connected = True
            logger.info("Робот успешно подключен и готов к работе")
            return True

        except Exception as e:
            logger.error(f"Ошибка при подключении: {e}")
            logger.error(traceback.format_exc())
            return False

    def _setup_motion_parameters(self) -> bool:
        try:
            assert self.arm.motion.set_param(
                param_name=ParamType.UF,
                param_value=self.config.uf_param
            ) == StatusCodeEnum.OK

            assert self.arm.motion.set_param(
                param_name=ParamType.TF,
                param_value=self.config.tf_param
            ) == StatusCodeEnum.OK

            logger.info("Параметры движения настроены")
            return True

        except AssertionError:
            logger.error("Ошибка настройки параметров движения")
            return False

    def gripper_ready(self):
        return self.gripper.read_state() == 1

    def _wait_for_gripper_ready(self, timeout: float = 2.0) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if self.gripper_ready():
                    logger.info(f"Захват готов")
                    return True
                time.sleep(0.1)
            except:
                time.sleep(0.2)

        logger.warning(f"Захват не готов после {timeout} секунд")
        return False

    def get_current_pose(self, pose_type: str = const.JOINT) -> Tuple[Optional[MotionPose], bool]:
        try:
            pose, ret = self.arm.motion.get_current_pose(pose_type, 0, 0)
            if ret != StatusCodeEnum.OK:
                logger.error(f"Ошибка получения позиции: {ret}")
                return None, False

            logger.info(f"Текущая позиция получена (тип: {pose_type})")
            return pose, True

        except Exception as e:
            logger.error(f"Ошибка при получении позиции: {e}")
            return None, False

    def move_to_pose(self, pose: MotionPose, move_type: int = const.MOVE_JOINT) -> bool:
        try:
            logger.info(f"Движение к позиции (тип: {move_type})...")
            ret = self.arm.motion.move_to_pose(pose, move_type)

            if ret != StatusCodeEnum.OK:
                logger.error(f"Ошибка движения: {ret}")
                return False

            return self._wait_for_arm_ready()

        except Exception as e:
            logger.error(f"Ошибка при движении: {e}")
            return False

    def arm_ready(self):
        return self.arm.get_robot_status()[1] == RobotStatusEnum.ROBOT_IDLE

    def _wait_for_arm_ready(self, timeout: float = 30.0) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if self.arm_ready():
                    logger.info("Манипулятор готов")
                    return True
                time.sleep(0.5)
            except:
                time.sleep(0.5)

        logger.warning(f"Манипулятор не готов после {timeout} секунд")
        return False

    def gripper_set_position(self, position: int) -> bool:
        try:
            logger.info(f"Установка захвата в позицию {position}...")
            self.gripper.set_pos(val=position)
            prev = -1
            while True:
                current_position = self.gripper.read_pos()
                if current_position == prev:
                    break
                prev = current_position
                time.sleep(0.1)
            if not self._wait_for_gripper_ready():
                logger.warning("Захват не завершил движение")
                return False
            logger.info(f"Захват установлен в позицию {position}")
            return True

        except Exception as e:
            logger.error(f"Ошибка при установке позиции захвата: {e}")
            return False

    def open(self):
        return self.gripper_set_position(1000)

    def close(self):
        return self.gripper_set_position(0)

    def disconnect(self):
        try:
            if self.arm:
                self.arm.disconnect()
                logger.info("Робот отключен")

            self.is_connected = False

        except Exception as e:
            logger.error(f"Ошибка при отключении: {e}")
