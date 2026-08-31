# CARLA Data Collection Protocol

## Before capture

Record CARLA version, town, map hash, route, weather, traffic density, random seeds, synchronous fixed delta, sensor calibration, ROS distro, Autoware commit, DriveTDPA checkpoint and preference-selector configuration.

## During capture

1. Run CARLA in synchronous mode and retain `/clock`.
2. Record required ROS topics in one rosbag2 per scene or bounded segment.
3. Export one compact record using the CARLA frame number as `frame_id`.
4. Retain sensor references, dynamic BEV, Talk2BEV output, all DriveTDPA candidates, selector decision, published trajectory and control.
5. Record next-frame state, route progress, collision/lane-invasion events and timing.

## After capture

1. Close the bag cleanly and record duration and message counts.
2. Generate SHA256 for every artifact before upload.
3. Validate manifests and records with `scripts/validate_dataset.py`.
4. Upload large artifacts to object storage without embedded credentials.
5. Publish manifests, reports, figures and compact examples to GitHub.

## Coverage and splitting

Use multiple towns/routes, weather and lighting, varied traffic density, static obstacles, lead-vehicle braking, lane changes and intersections. Separate train, validation and test by scene, not frame, to prevent temporal leakage.
