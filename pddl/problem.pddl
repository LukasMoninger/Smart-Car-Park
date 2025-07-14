(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    u1 - ultrasonic_entrance
    l1 - light_sensor
  )
  (:init
    (green_off g1)
    (red_on r1)
    (not_detected u1)
    (bright l1)
  )
  (:goal
    (and
      (green_on g1)
      (red_off r1)
    )
  )
)