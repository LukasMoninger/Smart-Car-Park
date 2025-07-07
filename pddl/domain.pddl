(define (domain smart_car_park)
  (:requirements :strips :typing)
  (:types
    green_light red_light
  )
  (:predicates
    (on ?l - green_light)
    (on ?l - red_light)
  )
  (:action switch_light_green
    :parameters (?g - green_light ?r - red_light)
    :precondition (and
      (on ?r)
      (not (on ?g))
    :effect (and
      (on ?g)
      (not (on ?r)
    )
  )
  (:action switch_light_red
    :parameters (?g - green_light ?r - red_light)
    :precondition (and
      (on ?g)
      (not (on ?r))
    :effect (and
      (on ?r)
      (not (on ?g)
    )
  )
)