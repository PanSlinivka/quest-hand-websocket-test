import time, yaml, math, signal, sys, os
from pathlib import Path

# ---- opravíme cesty k modulům ----
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bridge.safety import SafetyLimiter
from bridge.mujoco_driver import MuJoCoArmSim
from logger.session_logger import SessionLogger

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"
SCENE_PATH  = Path(__file__).resolve().parents[1] / "sim" / "mujoco_scene.xml"

def main():
    # načíst config
    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)

    rate_hz = cfg["teleop"]["control_rate_hz"]
    dt = 1.0 / rate_hz

    limiter = SafetyLimiter(
        joint_limits_deg = cfg["teleop"]["joint_limits_deg"],
        max_joint_speed  = cfg["teleop"]["max_joint_speed"]
    )

    sim = MuJoCoArmSim(str(SCENE_PATH))
    sim.start_viewer()

    logger = SessionLogger(log_dir="logs")

    def handle_exit(sig, frame):
        print("\n[teleop_bridge] stopping...")
        logger.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)

    print("[teleop_bridge] running loop at", rate_hz, "Hz")

    t0 = time.time()
    while True:
        now = time.time() - t0

        # fake trajektorie místo Questu
        shoulder_yaw   = 0.3 * math.sin(now * 0.5)
        shoulder_pitch = 0.2 * math.sin(now * 0.7)
        elbow_pitch    = 1.0 + 0.2 * math.sin(now * 0.9)
        wrist_yaw      = 0.0

        desired_cmd = {
            "shoulder_yaw": shoulder_yaw,
            "shoulder_pitch": shoulder_pitch,
            "elbow_pitch": elbow_pitch,
            "wrist_yaw": wrist_yaw
        }

        # bezpečnostní omezení
        desired_cmd = limiter.clamp_positions(desired_cmd)
        desired_cmd = limiter.clamp_speed(desired_cmd, dt)

        # poslat do simulace
        sim.step(desired_cmd)

        # přečíst aktuální stav kloubů
        joints = sim.get_joint_positions()

        # zapsat frame
        logger.log_step(joints, desired_cmd)

        # debug výpis
        print(f"[t={now:0.2f}] joints={joints}")

        time.sleep(dt)

if __name__ == "__main__":
    main()
EOF