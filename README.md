L'applicazione necessita di un planner numerico, con supporto specifico ai fluents. 
Nel caso di utilizzo del planner ENHSP, i file del dominio e del problema vanno inseriti nella stessa cartella del planner. L'esecuzione prevede due comandi principali, uno per la versione ottima e uno per la versione sub-ottima

Ottima: Java –jar enhsp.jar –o domain.pddl –f problem.pddl –planner opt-hrmax

Sub-Ottima: Java –jar enhsp.jar –o domain.pddl –f problem.pddl –planner sat-hadd

Per quanto riguarda l'interfaccia grafica, basta scaricare il codice python inserito qua nella repository
