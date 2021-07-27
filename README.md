# Instrukcja - wersja PL

Program służy do symulacji modelu Kartezjańskiego Programowania Genetycznego z
dodatkowymi technikami optymalizacyjnymi - `Simulated Annealing` (Symulowane
Wyżarzanie) oraz `Parallel Tempering`.

## Słownik pojęć:
* *CGP* - Cartesian Genetic Programming / Kartezjańskie Programowanie Genetyczne
* *SA* - Simulated Annealing / Symulowane Wyżarzanie
* *PT* - Parallel Tempering

## Opis modułów

* *notebooks* - notatniki `jupyter`, służące do analizy danych zebranych z symulacji
* *solutions* - przykładowe wyniki ekperymentów
* *src* - zawiera wszystkie skrypty definiujące algorytmy *CGP*, *SA*, *PT*, opis
  poszczególnych skryptów i parametrów symulacji w języku angielskim znajduje się w
  dedykowanym pliku `README` w katalogu `src`.

## Konfiguracja środowiska

### Instalacja `poetry`

**Poetry** pełni rolę menadżera pakietów, zastępuję typowy plik `requirements.txt` w
bardziej ustrukturyzowanej, czystej i automatycznej formie.

Zainstaluj `poetry` używając preferowanej przez siebie metody. Jednak należy pamiętać,
że użycie metody innej niż "recommended" (`curl`) może powodować problemy zmiennej PATH.
[Link do instrukcji instalacji](https://github.com/python-poetry/poetry#installation).

### Instalacja pakietów

Po zainstalowaniu `poetry` wywołaj:
```sh
make install
```
komenda ta spowoduje zainstalowanie wszystkich wymaganych pakietów i bibliotek
zewnętrznych.

## Interakcja z kodem

### Notatniki Jupyter

Aby włączyć możliwośc przeglądania notatników wywołaj:

```sh
make notebook
```

### Eksperymenty

Aby rozpocząć eksperyment należy wywołać:
```
make experiment EXP_NAME=<name_of_the_chosen_experiment>
```
gdzie zmienna `EXP_NAME` wskazuje nazwę skryptu z folderu `src.experiments` z
pominięciem rozszerzenia `.py`.

## Development

### Przed `commit`'em...

Przed publikacją swojego kodu należy wywołać komendę formatującą i sprawdzającą
czystość kodu:

```sh
make check
```

Można wywołać samo formatowanie oddzielnie:
```sh
make format
```

Każdy krok formatowania można także wywołać osobno:

```sh
make lint
make black
```

# Guidelines - ENG version

Package is designed to perform Cartesian Genetic Programming algorithm with
Simulated Annealing and Parallel Tempering techniques as optimization procedures.

## Install `poetry`

With your preferred method install `poetry` tool. Please note, that installing `poetry` with other that **recommended**
method (curl) could cause troubles. Using `pip`, `homebrew` or other similar method could cause `PATH` problems and lead
to errors while setting-up some packages. See [installation instructions for poetry](https://github.com/python-poetry/poetry#installation).

## Install dependencies

When poetry is installed on your machine you can run:
```sh
make install
```
all the necessary dependencies would be installed.

## Running

### Notebooks

To run the notebook server use:

```sh
make notebook
```

### Experiments

To start an experiment run:
```
make experiment EXP_NAME=<name_of_the_chosen_experiment>
```
where `EXP_NAME` contains the name of the chosen experiment from the `src.experiments`
directory, ommiting the `.py` extension.

## Development

### Before commit

Before you commit your code you need to apply automatic code formatting and checking:

```sh
make check
```

You can also run formatting separately:
```sh
make format
```

Each step of the formatting/linting process can be also executed in isolation,
for example:

```sh
make lint
make black
```

For more commands check the `Makefile`.