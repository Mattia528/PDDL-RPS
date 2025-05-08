L'applicazione necessita di un planner numerico, con supporto specifico ai fluents. 
Nel caso di utilizzo del planner ENHSP, i file del dominio e del problema vanno inseriti nella stessa cartella del planner. L'esecuzione prevede due comandi principali, uno per la versione ottima e uno per la versione sub-ottima

Ottima: Java –jar enhsp.jar –o Barbot_dom.pddl –f Barbot_prob.pddl –planner opt-hrmax

Sub-Ottima: Java –jar enhsp.jar –o Barbot_dom.pddl –f Barbot_prob.pddl –planner sat-hadd
