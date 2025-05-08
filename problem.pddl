(define (problem RPS)
  (:domain letseat)

  (:objects
    A B C - location
    a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 - articolo
    s1 s2 - sacchetto
    r1 - robot
    battery-0 battery-1 battery-2 battery-3 - battery-level
    capacita-0 capacita-1 capacita-2 capacita-3 capacita-4 capacita-5 - capacita-level
  )

  (:init
    ;; Posizione iniziale
    (on r1 A)
    (on a1 A) (on a2 A) (on a3 A) (on a4 A) (on a5 A)
    (on a6 A) (on a7 A) (on a8 A) (on a9 A) (on a10 A)
    (on s1 B)
    (on s2 B)

    ;; Etichette location
    (is-A A)
    (is-B B)
    (is-C C)

    ;; Connessioni
    (path A B)
    (path B A)
    (path B C)
    (path C B)

    ;; Stato iniziale robot
    (arm-empty)
    (current-battery battery-3)
    (next-battery battery-3 battery-2)
    (next-battery battery-2 battery-1)
    (next-battery battery-1 battery-0)

    ;; Capacità dei sacchetti
    (current-capacita s1 capacita-5)
    (current-capacita s2 capacita-5)
    (next-capacita capacita-5 capacita-4)
    (next-capacita capacita-4 capacita-3)
    (next-capacita capacita-3 capacita-2)
    (next-capacita capacita-2 capacita-1)
    (next-capacita capacita-1 capacita-0)

    ;; Pesi articoli
    (= (peso a1) 1) (= (peso a2) 1) (= (peso a3) 1)
    (= (peso a4) 1) (= (peso a5) 1) (= (peso a6) 1)
    (= (peso a7) 1) (= (peso a8) 1) (= (peso a9) 1)
    (= (peso a10) 1)

    ;; Conteggio articoli nei sacchetti
    (= (num-articoli-sacchetto s1) 0)
    (= (num-articoli-sacchetto s2) 0)
  )

  (:goal
    (and
      (on-sacchetto a1 s1)
      (on-sacchetto a2 s1)
      (on-sacchetto a3 s1)
      (on-sacchetto a4 s1)
      (on-sacchetto a5 s1)

      (on-sacchetto a6 s2)
      (on-sacchetto a7 s2)
      (on-sacchetto a8 s2)
      (on-sacchetto a9 s2)
      (on-sacchetto a10 s2)

      (sacchetto-pieno s1)
      (sacchetto-pieno s2)

      (on s1 C)
      (on s2 C)
    )
  )
)

  