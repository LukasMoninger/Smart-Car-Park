(define (domain smart_car_park)
  (:requirements :strips :typing)
  (:types
    green_light red_light entrance light_sensor co2_sensor ventilation signpost parking_space button timer
  )
  (:predicates
    (green_on ?g - green_light)
    (red_on ?r - red_light)
    (green_off ?g - green_light)
    (red_off ?r - red_light)
    (entrance_detected ?e - entrance)
    (entrance_not_detected ?e - entrance)
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
    (timer_expired ?t - timer)
    (connected ?s - signpost ?p - parking_space)
  )
  (:action switch_light_green
    :parameters (?g - green_light ?r - red_light ?e - entrance ?p - parking_space)
    :precondition (and
      (green_off ?g)
      (red_on ?r)
      (entrance_detected ?e)
      (parking_free ?p)
    )
    :effect (and
      (green_on ?g)
      (not (green_off ?g))
      (red_off ?r)
      (not (red_on ?r))
    )
  )
  (:action switch_light_red
    :parameters (?g - green_light ?r - red_light ?e - entrance)
    :precondition (and
      (red_off ?r)
      (green_on ?g)
      (entrance_not_detected ?e)
    )
    :effect (and
      (red_on ?r)
      (not (red_off ?r))
      (green_off ?g)
      (not (green_on ?g))
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
  (:action make_signpost_brighter
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
  (:action make_signpost_darker
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
    :parameters (?g - green_light ?r - red_light ?s - signpost ?p - parking_space)
    :precondition (and
      (green_on ?g)
      (red_off ?r)
      (signpost_off ?s)
      (parking_free ?p)
      (connected ?s ?p)
    )
    :effect (and
      (signpost_on ?s)
      (not (signpost_off ?s))
    )
  )
  (:action deactivate_signpost
    :parameters (?s - signpost ?p - parking_space ?e - entrance)
    :precondition (and
      (signpost_on ?s)
      (parking_free ?p)
      (entrance_detected ?e)
    )
    :effect (and
      (signpost_off ?s)
      (not (signpost_on ?s))
    )
  )
  (:action send_notification
    :parameters (?t - timer)
    :precondition (timer_expired ?t)
    :effect (not (timer_expired ?t))
  )
)