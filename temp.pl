homme(andre). 
homme(bernard). 
homme(babar). 
homme(clement). 
homme(dudulle). 
homme(damien). 
homme(baptiste). 
homme(cedric). 
homme(didier). 
homme(dagobert).
femme(augustine). 
femme(becassine). 
femme(brigitte). 
femme(chantal). 
femme(celestine). 
femme(caroline). 
femme(charlotte). 
femme(daniela). 
femme(dominique).
enfant(bernard,andre).
enfant(bernard,augustine).
enfant(babar,andre).
enfant(babar,augustine). 
enfant(brigitte,andre). 
enfant(brigitte,augustine). 
enfant(clement,bernard). 
enfant(clement,becassine). 
enfant(celestine,babar). 
enfant(caroline,brigitte). 
enfant(caroline,baptiste). 
enfant(cedric,brigitte). 
enfant(cedric,baptiste). 
enfant(dudulle,clement). 
enfant(dudulle,chantal). 
enfant(damien,clement). 
enfant(damien,chantal). 
enfant(daniela,clement). 
enfant(daniela,chantal). 
enfant(didier,cedric). 
enfant(didier,charlotte). 
enfant(dagobert,cedric). 
enfant(dagobert,charlotte). 
enfant(dominique,cedric). 
enfant(dominique,charlotte).

parent(X,Y) :- enfant(Y,X).

pere(X,Y) :- homme(X), parent(X,Y).

mere(X,Y) :- femme(X), parent(X,Y).

grand_pere(X,Y) :- homme(X), parent(X,Z), parent(Z,Y).

grand_mere(X,Y) :- femme(X), parent(X,Z), parent(Z,Y).

herbivore(chevre).
cruel(loup).

carnivore(X) :- cruel(X).

mange(X,viande) :- carnivore(X).
mange(X,herbe) :- herbivore(X).

mange(X,Y) :- carnivore(X), herbivore(Y).

boit(X,eau) :- carnivore(X).
boit(X,eau) :- herbivore(X).

consomme(X,Y) :- mange(X,Y).
consomme(X,Y) :- boit(X,Y).

