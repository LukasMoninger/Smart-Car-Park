(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    u1 - ultrasonic_entrance
    l1 - light_sensor
  )
  (:init
    (off_green g1)
    (on_red r1)
    (not_detected u1)
    (bright l1)
  )
  (:goal
    (and
      (on_green g1)
      (off_red r1)
    )
  )
)