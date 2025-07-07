(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    u1 - ultrasonic
  )
  (:init
    (on r1)
    (not (on g1))
    (not (detected u1))
  )
  (:goal
    (and
      (on g1)
      (not (on r1))
    )
  )
)