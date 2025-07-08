(define (domain smart_car_park)
  (:requirements :strips :typing)
  (:types
    green_light red_light ultrasonic_entrance
  )
  (:predicates
    (on_green ?l - green_light)
    (on_red ?l - red_light)
    (off_green ?l - green_light)
    (off_red ?l - red_light)
    (detected ?u - ultrasonic_entrance)
    (not_detected ?u - ultrasonic_entrance)
  )
  (:action switch_light_green
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic_entrance)
    :precondition (and
      (on_red ?r)
      (off_green ?g)
      (not_detected ?u)
    )
    :effect (and
      (on_green ?g)
      (not (off_green ?g))
      (not (on_red ?r))
      (off_red ?r)
    )
  )
  (:action switch_light_red
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic_entrance)
    :precondition (and
      (on_green ?g)
      (off_red ?r)
      (detected ?u)
    )
    :effect (and
      (on_red ?r)
      (not (off_red ?r))
      (not (on_green ?g))
      (off_green ?g)
    )
  )
)