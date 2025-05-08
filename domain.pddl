(define (domain RPS)
  (:requirements :typing :numeric-fluents)

  (:types
    location
    locatable - object
    bot articolo sacchetto - locatable
    robot - bot
    battery-level
    capacita-level)

  (:predicates
    (on ?obj - locatable ?loc - location)
    (holding ?arm - bot ?articolo - articolo)
    (holding-sacchetto ?arm - bot ?sacchetto - sacchetto)
    (arm-empty)
    (path ?from - location ?to - location)
    (on-sacchetto ?articolo - articolo ?sacchetto - sacchetto)
    (is-A ?loc - location)
    (is-B ?loc - location)
    (is-C ?loc - location)
    (current-battery ?level - battery-level)
    (next-battery ?from - battery-level ?to - battery-level)
    (sacchetto-pieno ?s - sacchetto)
    (current-capacita ?s - sacchetto ?level - capacita-level)
    (next-capacita ?from - capacita-level ?to - capacita-level)
  )

  (:functions
    (peso ?a - articolo)
    (num-articoli-sacchetto ?s - sacchetto)
  )

  (:action pick-up
    :parameters (?arm - bot ?articolo - articolo ?loc - location)
    :precondition (and
      (on ?arm ?loc)
      (on ?articolo ?loc)
      (arm-empty)
      (= (peso ?articolo) 1))
    :effect (and
      (not (on ?articolo ?loc))
      (holding ?arm ?articolo)
      (not (arm-empty)))
  )

  (:action drop-onto-sacchetto
    :parameters (?arm - bot ?articolo - articolo ?sacchetto - sacchetto ?loc - location ?b1 - battery-level ?b2 - battery-level ?c1 - capacita-level ?c2 - capacita-level)
    :precondition (and
      (on ?arm ?loc)
      (on ?sacchetto ?loc)
      (holding ?arm ?articolo)
      (is-B ?loc)
      (current-battery ?b1)
      (next-battery ?b1 ?b2)
      (current-capacita ?sacchetto ?c1)
      (next-capacita ?c1 ?c2)
      (< (num-articoli-sacchetto ?sacchetto) 5))
    :effect (and
      (on-sacchetto ?articolo ?sacchetto)
      (arm-empty)
      (not (holding ?arm ?articolo))
      (not (current-battery ?b1))
      (current-battery ?b2)
      (not (current-capacita ?sacchetto ?c1))
      (current-capacita ?sacchetto ?c2)
      (increase (num-articoli-sacchetto ?sacchetto) 1))
  )

  (:action move-sacchetto-to-C
    :parameters (?arm - bot ?sacchetto - sacchetto ?loc - location)
    :precondition (and
      (on ?arm ?loc)
      (on ?sacchetto ?loc)
      (is-B ?loc)
      (sacchetto-pieno ?sacchetto))
    :effect (and
      (on ?sacchetto C)
      (not (on ?sacchetto B)))
  )

  (:action segna-e-consegna-sacchetto
    :parameters (?arm - bot ?sacchetto - sacchetto ?loc - location)
    :precondition (and
      (on ?arm ?loc)
      (holding-sacchetto ?arm ?sacchetto)
      (is-C ?loc)
      (= (num-articoli-sacchetto ?sacchetto) 5))
    :effect (and
      (sacchetto-pieno ?sacchetto)
      (on ?sacchetto C)
      (not (holding-sacchetto ?arm ?sacchetto))
      (arm-empty))
  )

  (:action move
    :parameters (?arm - bot ?from - location ?to - location)
    :precondition (and
      (on ?arm ?from)
      (path ?from ?to))
    :effect (and
      (not (on ?arm ?from))
      (on ?arm ?to))
  )

  (:action pick-up-sacchetto
    :parameters (?arm - bot ?sacchetto - sacchetto ?loc - location)
    :precondition (and
      (on ?arm ?loc)
      (on ?sacchetto ?loc)
      (arm-empty))
    :effect (and
      (holding-sacchetto ?arm ?sacchetto)
      (not (on ?sacchetto ?loc))
      (not (arm-empty)))
  )

  (:action move-with-sacchetto
    :parameters (?arm - bot ?sacchetto - sacchetto ?from - location ?to - location)
    :precondition (and
      (on ?arm ?from)
      (holding-sacchetto ?arm ?sacchetto)
      (path ?from ?to))
    :effect (and
      (not (on ?arm ?from))
      (on ?arm ?to)
      (not (on ?sacchetto ?from))
      (on ?sacchetto ?to))
  )

  (:action drop-sacchetto
    :parameters (?arm - bot ?sacchetto - sacchetto ?loc - location)
    :precondition (and
      (on ?arm ?loc)
      (holding-sacchetto ?arm ?sacchetto)
      (is-C ?loc)
      (sacchetto-pieno ?sacchetto))
    :effect (and
      (on ?sacchetto ?loc)
      (arm-empty)
      (not (holding-sacchetto ?arm ?sacchetto)))
  )

  (:action recharge
    :parameters (?arm - bot ?loc - location)
    :precondition (and
      (on ?arm ?loc)
      (is-B ?loc)
      (current-battery battery-0))
    :effect (and
      (not (current-battery battery-0))
      (current-battery battery-3))
  )

  (:action start-sacchetto-2
    :parameters (?arm - bot ?sacchetto - sacchetto)
    :precondition (and
      (sacchetto-pieno s1)
      (not (sacchetto-pieno s2)))
    :effect (and
      (not (sacchetto-pieno s1))
      (sacchetto-pieno s2))
  )
)
