%il drone parte STATO 0
stato(partenza, T) :- attivita(partenza), tempo(T), not batteria(low,T).


%la prima azione che svolge è iniziare a sorvolare area STATO 1
stato(sorvoloDellArea, V) :- stato(partenza, T), V = T+1.

%dallo stato 2 decide l'azione che vuole svolgere allo stato T
stato(gestioneIncendio,T)|stato(sorvoloDellArea,T):- stato(_,V), T=V+1, statiMassimi(S),T < S.


numeroDiAzione(N):-#count{V : stato(gestioneIncendio,V)} = N.
{ coodinateIncendiChePossiamoGestire(X,Y) : incendioPresenteAlleCoordinate(X,Y) } = N :- numeroDiAzione(N).
1 { azione(gestioneIncendio,V, X, Y) :  stato(gestioneIncendio,V) } 1 :- coodinateIncendiChePossiamoGestire(X,Y).
:- azione(gestioneIncendio,V, X, Y), azione(gestioneIncendio,V, X1, Y1), X1!=X, Y1!=Y.
:- azione(gestioneIncendio,V, X, Y), azione(gestioneIncendio,V, X, Y1), Y1!=Y.
:- azione(gestioneIncendio,V, X, Y), azione(gestioneIncendio,V, X1, Y), X1!=X.


%controlla se ci sono due incendi vicini se vicini svolgo prima quello con allerta alto se ne esiste solo uno
distanza(X,Y,X1,Y1,D) :- coodinateIncendiChePossiamoGestire(X,Y), coodinateIncendiChePossiamoGestire(X1,Y1), D = (X - X1)^2 + (Y1 - Y)^2, X!=X1,Y!=Y1 . 
distanzaQuadrata(X1,X2,X,Y, D1):-distanza(X1,X2,X,Y, D), D<0, D1 = D*-1. 
distanzaQuadrata(X1,X2,X,Y, D1):-distanza(X1,X2,X,Y, D), D>=0, D1 = D. 


hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D(X,Y,V,X1,Y1,V1,D):- azione(gestioneIncendio,V, X, Y), azione(gestioneIncendio,V1, X1, Y1),distanzaQuadrata(X1,Y1,X,Y, D), D<=320, statoDiAllerta(alto,X,Y,V), not statoDiAllerta(alto,X1,Y1,V1).

:- hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D(X,Y,V,X1,Y1,V1,D), statoDiAllerta(alto,X,Y,V), not statoDiAllerta(alto,X1,Y1,V1), V1<V.


%nel caso individua un incendio allo stato T svolge delle azioni per gestirlo
pianifica(invia_mezzi_spegnimento,X,Y) :- azione(gestioneIncendio,V, X, Y).

direzioneAcqua(X,Y,V,D):- azione(gestioneIncendio,V, X, Y),vento(X,Y,D,_).

direzioneAcquaFraDueORe(X,Y,V,D):-azione(gestioneIncendio,V, X, Y),vento(X,Y,D,_).

informazioniPerISoccorritori(X,Y,V,D,C,T,U) :- azione(gestioneIncendio,V,X,Y), direzioneAcqua(X,Y,V,D), condizioneMeterologica(X,Y,C), temperatura(X,Y,T), umiditaInPercentuale(X,Y,U).

informazioniPerISoccorritoriNelleDueOreSuccessive(X,Y,V,D2,C,T,U) :-azione(gestioneIncendio,V, X, Y),direzioneAcquaFraDueORe(X,Y,V,D2), condizioneMeterologicaNelle2OreSuccessive(X,Y,C), temperaturaNelle2OreSuccessive(X,Y,T), umiditaInPercentualeNelle2OreSuccessive(X,Y,U).

chiamataSoccorsoInoltrata(X,Y,V,N):- azione(gestioneIncendio,V, X, Y), presenzaUmaniNellAreaLimitrofaDellIncendio(X,Y,N),N>0 .

chiamataSoccorsoVeterinarioInoltrata(X,Y,V,N):- azione(gestioneIncendio,V, X, Y),  presenzaAnimaliNellAreaLimitrofaDellIncendio(X,Y,N), N>0.
statoDiAllerta(alto,X,Y,V) :- azione(gestioneIncendio,V, X, Y),vento(X,Y,_,N), temperatura(X,Y,T),  umiditaInPercentuale(X,Y,U), dimensioneDellIncendioInEttari(X,Y,D), N>19, T>28, U<7,D>70 .

statoDiAllertaFuturo(alto,X,Y,V) :- azione(gestioneIncendio,V, X, Y),ventoNelle2OreSuccessive(X,Y,_,N), temperaturaNelle2OreSuccessive(X,Y,T),  umiditaInPercentualeNelle2OreSuccessive(X,Y,U), dimensioneDellIncendioInEttari(X,Y,D), N>19, T>28, U<7, D>70.

richiestaDiCanadairInoltrata(X,Y,V) :- azione(gestioneIncendio,V, X, Y), statoDiAllerta(alto,X,Y,V).
richiestaDiCanadairInoltrata(X,Y,V) :- azione(gestioneIncendio,V, X, Y), statoDiAllertaFuturo(alto,X,Y,V).


%Regola che individua il numero di incendi presenti
numeroDiIncendiIndividuati(N):-#count{X,Y : incendioPresenteAlleCoordinate(X,Y)} = N.

%non voglio che ci siano due gestioniIncendi in due stati conscutivi perche per individuare l'incendio successivo deve prima sorvolare area
:- azione(gestioneIncendio,V, X, Y), azione(gestioneIncendio,T, X1, Y1), T=V+1, not hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D(X,Y,V,X1,Y1,T,_).

:- azione(gestioneIncendio,V, X, Y), stato(sorvoloDellArea,T), T=V+1, C>T, hoTrovatoDueIncendiViciniSoloUnoHaStatoDiAllertaAlto_X_Y_V_X1_Y1_V1_D(X,Y,V,X1,Y1,C,_).

 
%per esempio se ci sono 1000 incendi ma io ho a disposizione per esempio 10 stati non posso gestire tutti gli incendi perche la mia batteria si scarica prima, ma nello stesso tempo devo massimizzare il numero di incendi da poter gestire, e quindi gli dico che NON ACCETTO che se numero di incendi che ho gestito sia minore degli incendi individuati se per due tempi consecutivi ho sorvolato area
:- stato(sorvoloDellArea,T), stato(sorvoloDellArea,V), T=V+1, numeroDiAzione(N), N < NI, numeroDiIncendiIndividuati(NI).

invioVentilatoriManuali(X,Y,N):- richiestaDiVentilatori(X,Y,N), azione(gestioneIncendio,_, X, Y).
%la mia batteria di scarica al tempo T max e quindi tornerà alla base
durataBatteria(low,S):- stato(_,T),statiMassimi(S),T=S-1.
stato(ritornoAllaBase, S) :- durataBatteria(low,S).
