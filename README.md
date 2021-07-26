# Instrukcja

Program służy do symulacji sieci modelu Kartezjańskiego Programowania Genetycznego.

## Parametry modelu

Parametry dotyczące zbioru danych, którymi "zasilana" jest sieć występują w pliku `main.py`: line 21-22.
Reszta parametrów symulacji (np. prawdopodobieństwa mutacji, ilośc kopii w każdym kroku etc.) jest ustalana w pliku `main.py`: line 29.

Opis parametrów i ich wykorzystania znajduje się w pliku `parameters.py`: `class Parameters` - doc-string.

## Funkcja celu

Funkcją celu aktualnie jest minimalizacja różnicy kwadratowej pomiędzy chwilową wartością Output sieci, a wartością rzeczywistą (zbiór danych Data_out). 
W celu selekcji wyników mutacji sieć dostaje jeden wektor danych wejściowych, przelicza i porównuje z wartością oczekiwaną. 
Proces ten jest powtarzany dla wszystkich wektorów wejściowych, a wyniki są sumowane. Sieć, która ma najniższą zsumowaną wartość
jest wybierana jako najlepiej dopasowana.

Implementacja funkcji celu znajduje się w pliku `net_1d.py`: line 196: `calculate_total_potential(self)`
oraz `net_1d.py`: line 171: `run_data(self, _input_set, i)`

## Przeprowadzenie symulacji

Aby przeprowadzić udaną symulację należy wykonwać następujące kroki:
1. Ustalić odpowiednie parametry wejściowe (patrz pkt. **Parametry Modelu**)
2. Będąc w folderze głównym zawierającym plik 'main.py' wykonać komendę w terminalu: `python main.py`
3. Zanim rozpocznie się symulacji pojawi się małe okienko z trzema przyciskami *Start*, *Stop*, *Quit*. Aby rozpocząć należy kliknąć *Start*.
4. W czasie trwania symulacji (default co 100 kroków symulacji) będą wyświetlały się parametry kontrolne sieci (plik `simulation.py`: line 70).
5. Symulacja automatycznie zakończy się w momencie gdy spełnione będą określone warunki dopasowania (plik `simulation.py`: line 78-99).