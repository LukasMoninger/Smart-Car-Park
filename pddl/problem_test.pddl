(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    e1 - entrance
    l1 - light_sensor
    c1 - co2_sensor
    v1 - ventilation
    s1 - signpost
    s2 - signpost
    s3 - signpost
    p1 - parking_space
    p2 - parking_space
  )
  (:init
    (green_off g1)
    (red_on r1)
    (entrance_not_detected e1)
    (bright l1)
    (signpost_bright s1)
    (signpost_bright s2)
    (signpost_bright s3)
    (signpost_off s1)
    (signpost_off s2)
    (signpost_off s3)
    (parking_free p1)
    (parking_free p2)
    (parking_free p3)
    (ventilation_off v1)
    (co2_low c1)
    (connected s1 p1)
    (connected s2 p2)
    (connected s3 p3)
  )
  (:goal
    (and
      (green_off g1)
      (red_on r1)
      (signpost_bright s1)
      (signpost_bright s2)
      (signpost_bright s3)
      (ventilation_off v1)
    )
  )
)
