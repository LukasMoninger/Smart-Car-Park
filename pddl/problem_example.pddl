(define (problem p1)
  (:domain example)
  (:objects
     r1 - robot
     a b c - location
  )
  (:init
     (at r1 a)
  )
  (:goal
     (at r1 c)
  )
)