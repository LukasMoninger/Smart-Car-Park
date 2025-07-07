(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    u1 - ultrasonic
  )
  (:init
    (on_red r1)
    (not (on_green g1))
    (not (detected u1))
  )
  (:goal
    (and
      (on_green g1)
      (not (on_red r1))
    )
  )
)