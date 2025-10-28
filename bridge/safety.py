import numpy as np

class SafetyLimiter:
    def __init__(self, joint_limits_deg, max_joint_speed):
        # joint_limits_deg = dict("joint_name": [min_deg, max_deg])
        self.joint_limits_rad = {
            j: [np.deg2rad(v[0]), np.deg2rad(v[1])]
            for j, v in joint_limits_deg.items()
        }
        self.max_joint_speed = max_joint_speed  # rad/s
        self.last_cmd = {}

    def clamp_positions(self, desired_cmd):
        """
        desired_cmd: dict("joint_name": rad)
        vrátí bezpečně omezenou verzi
        """
        safe = {}
        for j, val in desired_cmd.items():
            if j in self.joint_limits_rad:
                lo, hi = self.joint_limits_rad[j]
                safe[j] = np.clip(val, lo, hi)
            else:
                safe[j] = val
        return safe

    def clamp_speed(self, desired_cmd, dt):
        """
        Omezí skok mezi posledním příkazem a novým příkazem,
        aby rychlost nebyla víc než max_joint_speed.
        """
        if not self.last_cmd:
            self.last_cmd = desired_cmd.copy()
            return desired_cmd

        safe = {}
        for j, new_val in desired_cmd.items():
            old_val = self.last_cmd.get(j, new_val)
            max_delta = self.max_joint_speed * dt
            lo = old_val - max_delta
            hi = old_val + max_delta
            safe[j] = float(np.clip(new_val, lo, hi))
        self.last_cmd = safe.copy()
        return safe
