import logging

from src.robot import to_str, RobotController

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    ctr = RobotController()
    try:
        assert ctr.connect()
        pose, ret = ctr.get_current_pose()
        print(to_str(pose))
        assert ret
        pose.joint.j2 -= 3
        assert ctr.move_to_pose(pose)
        assert ctr.close()
        pose.joint.j2 += 3
        assert ctr.move_to_pose(pose)
        assert ctr.open()
    finally:
        ctr.disconnect()
