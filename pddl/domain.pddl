(define (domain smart_car_park)
  (:requirements :strips :typing)
  (:types
    green_light red_light ultrasonic_entrance light_sensor co2_sensor ventilation signpost parking_space button
  )
  (:predicates
    (green_on ?g - green_light)
    (red_on ?r - red_light)
    (green_off ?g - green_light)
    (red_off ?r - red_light)
    (detected ?u - ultrasonic_entrance)
    (not_detected ?u - ultrasonic_entrance)
    (bright ?l - light_sensor)
    (dark ?l - light_sensor)
    (signpost_bright ?s - signpost)
    (signpost_dark ?s - signpost)
    (signpost_on ?s - signpost)
    (signpost_off ?s - signpost)
    (co2_high ?c - co2_sensor)
    (co2_low ?c - co2_sensor)
    (ventilation_on ?v - ventilation)
    (ventilation_off ?v - ventilation)
    (parking_occupied ?p - parking_space)
    (parking_free ?p - parking_space)
    (button_pressed ?b - button)
    (button_not_pressed ?b - button)
  )
  (:action switch_light_green
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic_entrance)
    :precondition (and
      (red_on ?r)
      (green_off ?g)
      (not_detected ?u)
    )
    :effect (and
      (green_on ?g)
      (not (green_off ?g))
      (not (red_on ?r))
      (red_off ?r)
    )
  )
  (:action switch_light_red
    :parameters (?g - green_light ?r - red_light ?u - ultrasonic_entrance)
    :precondition (and
      (green_on ?g)
      (red_off ?r)
      (detected ?u)
    )
    :effect (and
      (not (green_on ?g))
      (green_off ?g)
      (red_on ?r)
      (not (red_off ?r))
    )
  )
  (:action activate_ventilation
    :parameters (?v - ventilation ?c - co2_sensor)
    :precondition (and
      (co2_high ?c)
      (ventilation_off ?v)
    )
    :effect (and
      (ventilation_on ?v)
      (not (ventilation_off ?v))
    )
  )
  (:action deactivate_ventilation
    :parameters (?v - ventilation ?c - co2_sensor)
    :precondition (and
      (co2_low ?c)
      (ventilation_on ?v)
    )
    :effect (and
      (ventilation_off ?v)
      (not (ventilation_on ?v))
    )
  )
  (:action make_light_brighter
    :parameters (?l - light_sensor ?s - signpost)
    :precondition (and
      (bright ?l)
      (signpost_dark ?s)
    )
    :effect (and
      (signpost_bright ?s)
      (not (signpost_dark ?s))
      )
  )
  (:action make_light_darker
    :parameters (?l - light_sensor ?s - signpost)
    :precondition (and
      (dark ?l)
      (signpost_bright ?s)
    )
    :effect (and
      (signpost_dark ?s)
      (not (signpost_bright ?s))
    )
  )
  (:action activate_signpost
    :parameters (?s - signpost ?p - parking_space ?u - ultrasonic_entrance)
    :precondition (and
      (signpost_off ?s)
      (parking_free ?p)
      (detected ?u)
    )
    :effect (and
      (signpost_on ?s)
      (not (signpost_off ?s))
    )
  )
  (:action deactivate_signpost
    :parameters (?s - signpost ?p - parking_space ?u - ultrasonic_entrance)
    :precondition (and
      (signpost_on ?s)
      (parking_free ?p)
      (detected ?u)
    )
    :effect (and
      (signpost_on ?s)
      (not (signpost_off ?s))
    )
  )
)