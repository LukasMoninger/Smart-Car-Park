(define (domain smart_car_park)
  (:requirements :strips :typing)
  (:types
    green_light red_light ultrasonic
  )
  (:predicates
    (on ?l - green_light)
    (on ?l - red_light)
    (detected ?u - ultrasonic)
  )
  (:action switch_light_green
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic)
    :precondition (and
      (on ?r)
      (not (on ?g))
      (not (detected ?u))
    )
    :effect (and
      (on ?g)
      (not (on ?r)
    )
  )
  (:action switch_light_red
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic)
    :precondition (and
      (on ?g)
      (not (on ?r))
      (detected ?u)
    )
    :effect (and
      (on ?r)
      (not (on ?g)
    )
  )
)