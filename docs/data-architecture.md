Automatically gererated by Junie in PyCharm 01/02/26

Data Architecture and Access Guide

This document explains the data storage architecture of the Visual Analytics repository, the hierarchy and relationships between data entities, and examples on how to access the data via REST, GraphQL, and Django ORM.

High-level overview
- Core Django apps: common, cognition, motion, image, behavior, annotation, user
- Hierarchy: Event -> Game/Experiment -> Log -> Frames (cognition/motion) -> Images -> Annotations
- Access:
  - REST: /api/
  - GraphQL: /graphql/ (login required)
  - Django ORM: via models in django/*/models.py

Key entities
- common: Event, Game, Experiment, Log, LogStatus
- cognition: CognitionFrame + per-frame perception models (e.g., BallModel)
- motion: MotionFrame + per-frame motion models (e.g., IMUData)
- image: NaoImage (camera TOP/BOTTOM; type RAW/JPEG)
- annotation: Annotation attached to NaoImage
- behavior: BehaviorOption/State and per-frame BehaviorFrameOption

Examples
- REST: GET /api/cognitionframe/?log=<log_id>&ordering=frame_number
- REST: GET /api/cognition/ballmodel/?frame__log=<log_id>
- REST: GET /api/image/?frame__log=<log_id>&camera=TOP&type=JPEG

Notes
- Most endpoints require authentication (Token or session). Use Django admin or existing tokens.
- Use pagination for large logs and order by frame_number.


REST API endpoints (complete list)

Base prefix
- All REST endpoints are served under /api/ (see django/core/urls.py). Unless stated otherwise, each ViewSet provides standard list/detail endpoints and supports typical filters via query parameters.

Common (metadata)
- GET /api/                 – Scalar doc (simple API index)
- GET /api/health/          – Health check
- /api/events/              – Events (list, create); /api/events/{id}/ for detail
- /api/games/               – Games (list, create); /api/games/{id}/ for detail
- /api/experiments/         – Experiments (list, create); /api/experiments/{id}/ for detail
- /api/logs/                – Logs (list, create); /api/logs/{id}/ for detail
- /api/log-status/          – LogStatus (list, create); /api/log-status/{id}/ for detail

Cognition
- GET /api/cognitionframe/count/      – Total CognitionFrame count (supports ?log=<id>)
- POST /api/cognitionframe/update/    – Trigger/update hook (admin/auth required)
- /api/cognitionframe/                – CognitionFrame list/detail
- /api/cognition/<model_name>/        – Dynamic per-frame perception endpoints, for example:
  - /api/cognition/ballmodel/
  - /api/cognition/ballcandidates/
  - /api/cognition/ballcandidatestop/
  - /api/cognition/cameramatrix/
  - /api/cognition/cameramatrixtop/
  - /api/cognition/odometrydata/
  - /api/cognition/fieldpercept/
  - /api/cognition/fieldpercepttop/
  - /api/cognition/goalpercept/
  - /api/cognition/goalpercepttop/
  - /api/cognition/multiballpercept/
  - /api/cognition/ransaccirclepercept2018/
  - /api/cognition/ransaclinepercept/
  - /api/cognition/robotinfo/
  - /api/cognition/shortlinepercept/
  - /api/cognition/scanlineedgelpercept/
  - /api/cognition/scanlineedgelpercepttop/
  - /api/cognition/teammessagedecision/
  - /api/cognition/teamstate/
  - /api/cognition/whistlepercept/
- /api/frame-filter/                    – Saved frame filters per user/log

Motion
- GET /api/motionframe/count/          – Total MotionFrame count (supports ?log=<id>)
- POST /api/motionframe/update/        – Trigger/update hook (admin/auth required)
- /api/motionframe/                    – MotionFrame list/detail
- /api/motion/<model_name>/            – Dynamic motion endpoints, for example:
  - /api/motion/imudata/
  - /api/motion/fsrdata/
  - /api/motion/buttondata/
  - /api/motion/sensorjointdata/
  - /api/motion/accelerometerdata/
  - /api/motion/inertialsensordata/
  - /api/motion/motionstatus/
  - /api/motion/motorjointdata/
  - /api/motion/gyrometerdata/

Image
- GET /api/image-count/                – Total images count (supports ?log=<id>, ?camera, ?type)
- POST /api/image/update/              – Trigger/update hook (admin/auth required)
- /api/image/                          – NaoImage list/detail
- /api/image-list/                     – Paged image list (optimized for UI)

Annotation
- GET /api/annotation-count/           – Annotation count
- POST /api/annotation-task/           – Request a labeling task (server provides images to annotate)
- POST /api/annotation-task/border     – Border task variant
- POST /api/annotation-task/multiple   – Multiple-images task variant
- /api/annotations/                    – Annotation list/detail (attached to images)

Behavior
- GET /api/behavior/filter/            – Filter BehaviorFrameOption over frames
- GET /api/behavior/count/             – BehaviorFrame count
- GET /api/behavior/symbol/count/      – XABSL symbol frames count
- /api/behavior-option/                – BehaviorOption list/detail
- /api/behavior-option-state/          – BehaviorOptionState list/detail
- /api/behavior-frame-option/          – BehaviorFrameOption list/detail
- /api/behavior/symbol/complete/       – XabslSymbolComplete list/detail (one per log)
- /api/behavior/symbol/sparse/         – XabslSymbolSparse list/detail (per frame)

Users and auth (non-API root)
- POST /login                          – Login view (session)
- POST /logout                         – Logout
- POST /signup                         – Signup (may be disabled in production)

Other service endpoints
- /graphql/                            – GraphiQL IDE + GraphQL endpoint (authentication required)
- /schema/                             – OpenAPI schema (drf-spectacular)
- /admin/                              – Django Admin

Typical filters and ordering
- Most list endpoints support query parameters to filter and sort results. Common patterns:
  - ?log=<log_id> on frame-like endpoints
  - ?frame__log=<log_id> on per-frame representation endpoints
  - ?frame=<frame_id> or ?frame_number=<n>
  - ?camera=TOP|BOTTOM and ?type=RAW|JPEG for /api/image/
  - ?ordering=frame_number or ?ordering=-frame_number
  - Standard pagination: ?page=<n>&page_size=<k> (depends on server settings)

Example queries by goal
- All cognition frames of a log ordered by frame: GET /api/cognitionframe/?log=<LOG_ID>&ordering=frame_number
- Ball model estimates for a log: GET /api/cognition/ballmodel/?frame__log=<LOG_ID>
- Top camera JPEG images for a log: GET /api/image/?frame__log=<LOG_ID>&camera=TOP&type=JPEG
- Motion IMU data for a log: GET /api/motion/imudata/?frame__log=<LOG_ID>
- Behavior active options for a frame: GET /api/behavior-frame-option/?frame=<FRAME_ID>

GraphQL quick start
- POST /graphql/ with a query such as:
  query { images(logId: 123, camera: TOP, type: JPEG) { id imageUrl frameNumber } }
  Use the GraphiQL UI at /graphql/ to explore the schema.