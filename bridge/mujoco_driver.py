import mujoco
import numpy as np
from mujoco import viewer

class MuJoCoArmSim:
    def __init__(self, scene_path: str):
        self.model = mujoco.MjModel.from_xml_path(scene_path)
        self.data = mujoco.MjData(self.model)
        self.viewer = None

        # mapování pořadí kloubů na actuatory
        self.joint_names = [
            "shoulder_yaw",
            "shoulder_pitch",
            "elbow_pitch",
            "wrist_yaw"
        ]
        self.actuator_names = [
            "act_shoulder_yaw",
            "act_shoulder_pitch",
            "act_elbow_pitch",
            "act_wrist_yaw"
        ]

    def start_viewer(self):
        if self.viewer is None:
            self.viewer = viewer.launch_passive(self.model, self.data)

    def step(self, target_positions_rad: dict):
        """
        target_positions_rad je dict:
        {
          "shoulder_yaw":   float (radians),
          "shoulder_pitch": float,
          "elbow_pitch":    float,
          "wrist_yaw":      float
        }
        """
        # nastav cílovou pozici pro každý aktuátor
        for name, target in target_positions_rad.items():
            if name in self.joint_names:
                joint_id = self.joint_names.index(name)
                act_name = self.actuator_names[joint_id]
                act_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, act_name)
                self.data.ctrl[act_id] = target

        # posuň simulaci o jeden krok
        mujoco.mj_step(self.model, self.data)

        if self.viewer is not None:
            self.viewer.sync()

    def get_joint_positions(self):
        res = {}
        for jn in self.joint_names:
            jid = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, jn)
            res[jn] = self.data.qpos[jid].item()
        return res
