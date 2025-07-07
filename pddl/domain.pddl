(define (domain smart_car_park)
  (:requirements :strips :typing :adl)
  (:types
    green_light red_light ultrasonic
  )
  (:predicates
    (on_green ?l - green_light)
    (on_red ?l - red_light)
    (detected ?u - ultrasonic)
  )
  (:action switch_light_green
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic)
    :precondition (and
      (on_red ?r)
      (not (on_green ?g))
      (not (detected ?u))
    )
    :effect (and
      (on_green ?g)
      (not (on_red ?r))
    )
  )
  (:action switch_light_red
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic)
    :precondition (and
      (on_green ?g)
      (not (on_red ?r))
      (detected ?u)
    )
    :effect (and
      (on_red ?r)
      (not (on_green ?g))
    )
  )
)