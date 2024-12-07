Documentația Proiectului
1. Descriere Generală a Proiectului
Proiectul reprezintă o simulare a unui ecosistem simplificat, în care plantele, erbivorele și carnivorele interacționează între ele într-o hartă de dimensiuni fixe. Principalele mecanisme simulate sunt:

Creșterea și reproducerea plantelor.
Deplasarea, hrănirea și reproducerea animalelor (erbivore și carnivore).
Consumul de energie și eliminarea entităților atunci când energia acestora scade la zero.
Parametrii precum rata de reproducere, energia inițială, pragurile de reproducere sau raza de detectare a hranei pot fi ajustați în cod pentru a obține comportamente diferite ale ecosistemului.

2. Ierarhia Claselor și Descrierea lor
Clasa abstractă EntitateEcosistem
Rol: Baza pentru toate entitățile din ecosistem (plante și animale).

Atribute:

nume: String ce identifică entitatea.
energie: int/float, reprezintă energia curentă.
pozitie_x, pozitie_y: int, poziția entității pe hartă.
rata_supravietuire: float, indică probabilitatea sau rata cu care entitatea se poate adapta/supraviețui (parametru general).
Metode:

actioneaza(): Metodă abstractă. Determină acțiunea entității pe durata unui pas de simulare.
pozitie(): Returnează coordonatele (x, y) ale entității.
Clasa Planta (moștenește EntitateEcosistem)
Rol: Reprezintă plantele din ecosistem. Plantele cresc în energie la fiecare pas și se pot reproduce dacă ating un anumit prag de energie.

Metode:
actioneaza(): Crește energia plantei.
reproduce(): Creează o nouă plantă în apropiere dacă pragul de energie este depășit.
Clasa abstractă Animal (moștenește EntitateEcosistem)
Rol: Baza pentru erbivore și carnivore. Animalele se deplasează pe hartă, consumă energie la fiecare pas și își caută hrana.

Atribute suplimentare:

viteza: int, indică raza maximă de deplasare a animalului într-un pas.
tip_hrana: String, indică tipul de hrană (e.g., "plante" pentru erbivore, "animale" pentru carnivore).
Metode:

deplaseaza(): Modifică aleator poziția animalului în funcție de viteză.
actioneaza(): Deplasare + consum de energie.
mananca(prada): Animalul consumă energia prăzii. Dacă prada este compatibilă (erbivor->plantă, carnivor->erbivor), câștigul de energie este mărit.
reproduce(): Creează un nou animal cu energie scăzută, pentru a nu se putea reproduce imediat.
Clasa Erbivor (moștenește Animal)
Rol: Animale care consumă plante. Au energie inițială, viteză și prag de reproducere definit.

Clasa Carnivor (moștenește Animal)
Rol: Animale care consumă erbivorele. Au un mod similar de funcționare cu erbivorele, dar hrana lor este diferită.

Clasa Ecosistem
Rol: Gestionează lista de entități, simulează pașii, coordonează reproducerea, hrănirea și eliminarea entităților moarte.

Atribute:

dimensiune_harta_x, dimensiune_harta_y: Dimensiunile hărții.
entitati: list, conține toate entitățile din ecosistem.
Metode:

adauga_entitate(entitate): Adaugă o nouă entitate în ecosistem.
elimina_entitate(entitate): Elimină o entitate din ecosistem.
simuleaza_pas(): Rulează un pas de simulare în care fiecare entitate acționează, se reproduce, se hrănește etc.
afiseaza_stare(): Afișează starea curentă a ecosistemului.
3. Diagrama UML

          EntitateEcosistem (abstract)
         /             \
        /               \
     Planta           Animal (abstract)
                     /           \
                    /             \
                Erbivor         Carnivor

Ecosistem
 - entitati: List<EntitateEcosistem>
 - dimensiune_harta_x: int
 - dimensiune_harta_y: int
Relații:

EntitateEcosistem este superclasa pentru Planta și Animal.
Animal este superclasa pentru Erbivor și Carnivor.
Ecosistem conține o listă de EntitateEcosistem.
4. Scenarii de Utilizare
Scenariu 1: Inițializare și rulare

Inițiem un ecosistem 100x100.
Adăugăm 5 plante, 8 erbivore (iepurii) și 5 carnivore (lupii).
Rulăm 5 pași de simulare.
La fiecare pas:
Plantele cresc și se pot reproduce dacă depășesc pragul.
Erbivorele se deplasează, consumă energie, caută plante în apropiere și, dacă îndeplinesc condițiile, se reproduc.
Carnivorele se deplasează, consumă energie, caută erbivore în apropiere. Dacă au suficientă energie, se reproduc.
Entitățile cu energie ≤0 sunt eliminate.
Output așteptat:
În timpul rulării vor apărea mesaje precum:

"Iepure2 mănâncă Planta3 (Plantă) cu un beneficiu mărit!"
"Lup1 atacă și mănâncă Iepure5 (Erbivor) cu un beneficiu mărit!"
"Iepure4 s-a reprodus, creând Iepure4_copil!"
De asemenea, după fiecare pas se afișează starea ecosistemului.
5. Dificultăți Întâlnite și Soluțiile Adoptate
Problemă: Eliminarea dublă a entităților din listă cauzând erori ValueError.
Soluție: Adăugarea unor verificări if prada in self.entitati înainte de a elimina entitatea, asigurându-ne că o entitate este eliminată o singură dată.

Problemă: Parametrii de reproducere prea restrictivi sau prea laxi, ducând la populații care cresc necontrolat sau dispar rapid.
Soluție: Ajustarea pragurilor de energie și costurilor de reproducere pentru a obține un echilibru intermediar.

Problemă: Animale care se reproduc imediat după ce se nasc.
Soluție: Setarea energiei inițiale a copiilor la o valoare mai mică decât pragul de reproducere, astfel încât aceștia să nu se poată reproduce imediat.

Problemă: Interacțiuni complexe și consum reciproc nedorit.
Soluție: Limitarea tipului de hrană pentru fiecare categorie (erbivore -> plante, carnivore -> erbivore) și eliminarea consumului reciproc între animale de același tip.

Concluzie
Documentația oferă o imagine de ansamblu asupra arhitecturii și comportamentului proiectului. Prin ajustarea parametrilor din clase, pot fi obținute diferite scenarii ecologice, explorând dinamici complexe într-un mod simplificat.
