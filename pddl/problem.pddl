(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    u1 - ultrasonic_entrance
    l1 - light_sensor
    c1 - co2_sensor
    v1 - ventilation
    s1 - signpost
    p1 - parking_space
    p2 - parking_space
    p3 - parking_space
  )
  (:init
    (green_off g1)
    (red_on r1)
    (not_detected u1)
    (dark l1)
    (signpost_bright s1)
    (ventilation_off v1)
    (co2_low c1)
    (parking_free p1)
  )
  (:goal
    (and
      (green_on g1)
      (red_off r1)
      (signpost_dark s1)
    )
  )
)