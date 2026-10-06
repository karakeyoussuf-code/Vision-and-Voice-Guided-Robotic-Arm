import math
import time

# Connecting to CoppeliaSim
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
client = RemoteAPIClient()
sim = client.require('sim')

# Connecting to each joint in the robotic arm
shoulder_yaw=sim.getObject('/joint_shoulder_yaw')
shoulder_pitch=sim.getObject('/joint_shoulder_pitch')
elbow=sim.getObject('/joint_elbow')
wrist_pitch=sim.getObject('/joint_wrist_pitch')
wrist_roll=sim.getObject('/joint_wrist_roll')

# connecting to the links of the robotic arm
Floor = sim.getObject('/Floor')
upper_arm = sim.getObject('/link_upper_arm')
forearm = sim.getObject('/link_forearm')
hand_palm = sim.getObject('/hand_palm')


FLOOR_CLEARANCE = 0.01   # Stop 1 cm before the Floor
MAX_SPEED = 200         # degrees per second
UPDATE_TIME = 0.02 

def move_joint(joint, angle):

    sim.setJointPosition(joint, math.radians(angle))

def move_arm(
    shoulder_yaw_angle,
    shoulder_pitch_angle,
    elbow_angle,
    wrist_roll_angle,
    wrist_pitch_angle
):
    joints = [
        shoulder_yaw,
        shoulder_pitch,
        elbow,
        wrist_roll,
        wrist_pitch
    ]

    target_angles = [
        shoulder_yaw_angle,
        shoulder_pitch_angle,
        elbow_angle,
        wrist_roll_angle,
        wrist_pitch_angle
    ]

    moving_parts = [
        upper_arm,
        forearm,
        hand_palm
    ]

    # Read the current position of all five joints
    current_angles = []

    for joint in joints:
        current_angle = math.degrees(sim.getJointPosition(joint))
        current_angles.append(current_angle)

    # Make cyclic joints use the shortest rotational path
    cyclic_joint_indices = [0, 3]   # shoulder_yaw, wrist_roll

    for i in cyclic_joint_indices:

        current = current_angles[i]
        target = target_angles[i]

        angle_difference = (target - current + 180) % 360 - 180

        target_angles[i] = current + angle_difference

    # Find which joint has the largest movement
    largest_movement = 0

    for current, target in zip(current_angles, target_angles):
        movement = abs(target - current)

        if movement > largest_movement:
            largest_movement = movement

    # Nothing needs to move
    if largest_movement < 0.001:
        return

    # Determine how long the movement should take
    duration = largest_movement / MAX_SPEED

    # Number of small intermediate poses
    steps = max(1, math.ceil(duration / UPDATE_TIME))

    last_safe_angles = current_angles.copy()

    for step in range(1, steps + 1):

        progress = step / steps

        new_angles = []

        # Calculate where every joint should be at this moment
        for current, target in zip(current_angles, target_angles):

            new_angle = current + (target - current) * progress

            new_angles.append(new_angle)

        # Move ALL five joints to this intermediate pose
        for joint, angle in zip(joints, new_angles):

            sim.setJointPosition(
                joint,
                math.radians(angle)
            )

        unsafe = False

        # Check the complete robot pose against the Floor
        for part in moving_parts:

            collision, _ = sim.checkCollision(part, Floor)

            if collision:
                unsafe = True
                break

            too_close, _, _ = sim.checkDistance(
                part,
                Floor,
                FLOOR_CLEARANCE
            )

            if too_close == 1:
                unsafe = True
                break

        # If this new pose is unsafe, go back to the previous safe pose
        if unsafe:

            for joint, angle in zip(joints, last_safe_angles):

                sim.setJointPosition(
                    joint,
                    math.radians(angle)
                )

            print("Movement stopped: Floor clearance reached.")

            return

        # This complete pose was safe
        last_safe_angles = new_angles.copy()

        # Controls how quickly the intermediate poses are sent
        time.sleep(UPDATE_TIME)


move_arm(
    300,      # shoulder yaw
    50,     # shoulder pitch
    20,      # elbow
    60,      # wrist roll
    90      # wrist pitch
)