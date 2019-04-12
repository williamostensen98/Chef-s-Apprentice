# Chef's Apprentice 
Chef's Apprentice er en applikasjon som lar alminnelige brukere og sertifiserte kokker dele og tilgjengeliggjøre sine matoppskrifter for andre brukere av applikasjonen som er laget for og i samarbeid med BackBone Industries LLC.

## Motivasjon

Tusenvis av nordmenn går hver dag sultne fordi de ikke vet hva de skal lage til middag, men likevel kaster de årlig tonnevis av ubrukte ingredienser. Det er ikke bærekraftig, hverken for lønnsomhet, miljø eller etiske årsaker. Applikasjonen Chef's Apprentice har som målsetning å bidra til å redusere og på sikt løse dette omfattende matsvinnproblemet.



## Demo
Etter å ha logget inn på siden vil du bli møtt med denne hjemmesiden:
![Home](pu_project/media/home.png)
Herfra har du tilgang på all funksjonalitet i applikasjonen.

Oppskriftene som vises først her er fra verifiserte kokker, noe som kan ses over til høyre av oppskriftsbildet, og så alle oppskrifter fra alminnelige brukere senere. Man kan trykke på de enkelte oppskriftene for mer informasjon om dem. Her vises alle ingredienser med enheter og mengder, samt fremgangsmåten. Herfra har man også muligheten til å laste ned oppskrifter, og redigere eller slette dem hvis man enten eier oppskriften selv eller er verifisert kokk / administrator.

I søkefeltene kan du søke oppskriftsdatabasen enten på oppskriftsnavn eller på så mange ingredienser du vil. Søker du på mer enn en oppskrift vil søkeresultatet sorteres etter to faktorer; antall treff på ingredienser er den overordnede prioriteten, men har flere oppskrifter like mange treff på ingredienser, vil også her verifiserte kokkers oppskrifter vises først.

Ved å trykke på 'New Recipe' kommer man til et enkelt skjema der det er mulighet for å legge til nye oppskrifter med all relevant informasjon.

Under 'My Account' finner man informasjon om sin egen bruker og muligheten til å bytte passord. Her finner man også en oversikt over alle oppskrifter en selv har lagt ut på siden.

## Teknologi & Rammeverk

### Built with
* [Django 2.1.7](https://www.djangoproject.com/)
* [Atom 1.35.1](https://atom.io/) / [Pycharm 2018.2](https://www.jetbrains.com/pycharm/)



## Installasjon 

###### Kom i gang

_Installasjon av prosjektet krever at [Python](https://www.python.org/downloads/) og [pip](https://pip.pypa.io/en/stable/installing/) er installert_

_Det kan også være hensiktsmessig å installere [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) og [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). Disse er verktøy som tilbyr isolerte Python 'environments', som er mer praktisk enn å installere pakker systembredt_.

_Aktivering av virtualenv gjøres enkelt ved å skrive i kommandolinje/terminal:_
```sh
$ source /path/to/virtualenv/bin/activate
```
###### Installer Django

Etter man har opprettet og aktivert _virtualenv_, skriv inn kommandoen:
```sh
 $ pip install Django
```
###### Kjøre applikasjonen lokalt

Sørg for å ha [Git](https://git-scm.com/) installert og klon prosjektet ved kommandoen:
```sh
$ git clone https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-64.git
```
Sørg også for å ha alle tilleggspakker installert. Dette kan gjøres ved å navigere til Django-prosjekt-mappen(pu_prosjekt) og skriv inn kommandoen:

```sh
$ pip install -r requirements.txt
```

Du er nå klar for å kjøre prosjektet lokalt på maskinen din. 
Applikasjonen kan kjøres ved kommandoen
```sh
$ python manage.py runserver
```
Du vil nå finne siden på 'http://localhost:8000'.

## Tester
Innebygd i prosjektet ligger en pipeline som kjører prosjektets testing hver gang prosjektet oppdateres, slik at det alltid er en fungerende versjon som ligger ute. Status på denne kan ses på gitlab siden til prosjektet under CD/CI og pipelines. Ellers kan også testene kjøres via test.py direkte eller ved kommandoen ```./manage.py test```.  

Mer informasjon om kjøring av testene eller om feilmeldinger finner du [her](https://docs.djangoproject.com/en/2.2/topics/testing/overview/#running-tests).
(_For problemer/feilmelding med ```psycopg2```modulen, se [psycopg2/docs](http://initd.org/psycopg/docs/install.html)_)



## Utviklet av

* William Østensen
* Katarina Gjendem Murphy 
* Henrik Forbord
* Erling Enes Kjevik
* Kristian Flock

## Lisens

NTNU © [Programvareutvikling/gruppe 64](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-64)

