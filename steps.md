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

Plik z dodatkowymi informacjami

Jest to plik tekstowy składający się z 5 linii, z których każda zawiera jedną liczbę oznaczającą odpowiednio:

    1 linia (liczba całkowita): długość znalezionego rozwiązania - o takiej samej wartości jak w pliku z rozwiązaniem (przy czym gdy program nie znalazł rozwiązania, wartość ta to -1);
    2 linia (liczba całkowita): liczbę stanów odwiedzonych;
    3 linia (liczba całkowita): liczbę stanów przetworzonych;
    4 linia (liczba całkowita): maksymalną osiągniętą głębokość rekursji;
    5 linia (liczba rzeczywista z dokładnością do 3 miejsc po przecinku): czas trwania procesu obliczeniowego w milisekundach.
