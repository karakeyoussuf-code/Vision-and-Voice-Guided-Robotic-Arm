import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

#shoulder yaw joint 
shoulder_yaw=sim.getObject('/joint_shoulder_yaw')
print(shoulder_yaw)
shoulder_yaw_angle=math.degrees(sim.getJointPosition(shoulder_yaw))
print(f"Shoulder yaw angle: {shoulder_yaw_angle}")
sim.setJointPosition(shoulder_yaw, math.radians(150))
new_shoulder_angle=math.degrees(sim.getJointPosition(shoulder_yaw))
print(f"New shoulder angle: {new_shoulder_angle}")

#shoulder pitch joint
shoulder_pitch=sim.getObject('/joint_shoulder_pitch')
print(shoulder_pitch)
shoulder_pitch_angle=math.degrees(sim.getJointPosition(shoulder_pitch))
print(f"Shoulder pitch angle: {shoulder_pitch_angle}")
sim.setJointPosition(shoulder_pitch, math.radians(30))
new_shoulder_pitch_angle=math.degrees(sim.getJointPosition(shoulder_pitch))
print(f"New shoulder pitch angle: {new_shoulder_pitch_angle}")

#elbow joint
elbow=sim.getObject('/joint_elbow')
print(elbow)
elbow_angle=math.degrees(sim.getJointPosition(elbow))
print(f"Elbow angle: {elbow_angle}")
sim.setJointPosition(elbow, math.radians(60))
new_elbow_angle=math.degrees(sim.getJointPosition(elbow))
print(f"New elbow angle: {new_elbow_angle}")

#wrist pitch joint
wrist_pitch=sim.getObject('/joint_wrist_pitch')
print(wrist_pitch)
wrist_pitch_angle=math.degrees(sim.getJointPosition(wrist_pitch))
print(f"Wrist pitch ang-le: {wrist_pitch_angle}")
sim.setJointPosition(wrist_pitch, math.radians(100))
new_wrist_pitch_angle=math.degrees(sim.getJointPosition(wrist_pitch))
print(f"New wrist pitch angle: {new_wrist_pitch_angle}")

#wrist roll joint
wrist_roll=sim.getObject('/joint_wrist_roll')
print(wrist_roll)
wrist_roll_angle=math.degrees(sim.getJointPosition(wrist_roll))
print(f"Wrist roll angle: {wrist_roll_angle}")
sim.setJointPosition(wrist_roll, math.radians(90))
new_wrist_roll_angle=math.degrees(sim.getJointPosition(wrist_roll))
print(f"New wrist roll angle: {new_wrist_roll_angle}")

print("Connected to CoppeliaSim successfully!")

