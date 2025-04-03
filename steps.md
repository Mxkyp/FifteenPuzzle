# steps

---

> "Wprawdzie program będzie służył do przebadania zachowania poszczególnych metod
> przeszukiwania przestrzeni stanów w przypadku klasycznej
> "Piętnastki", musi on być jednak napisany w sposób uniwersalny,
> to znaczy taki, który umożliwi generowanie rozwiązań także dla ramek o innych niż standardowe rozmiarach,
> w tym ramek niekwadratowych."

1. the program requires **5** command line arguments

1.1 the program strategy (bfs, dfs, astr) \
1.2 the strategy options (permutations of LURD, hamm, manh) \
1.3 text-file name with the initial puzzle \
1.4 solution text-file \
1.5 text-file with additional solution information

## Przykladowe pliki

Plik z układem początkowym

Jest to plik tekstowy, w którym liczba linii zależy od rozmiaru ramki. Pierwsza linia zawiera dwie liczby całkowite w oraz k, oddzielone od siebie spacją, które określają odpowiednio pionowy (liczbę wierszy) i poziomy (liczbę kolumn) rozmiar ramki. Każda z pozostałych w linii zawiera k oddzielonych spacjami liczb całkowitych, które opisują położenie poszczególnych elementów układanki, przy czym wartość 0 oznacza wolne pole.
