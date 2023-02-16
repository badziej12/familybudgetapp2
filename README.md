# familybudgetapp2

Celem pracy było zaprojektowanie oraz zaimplementowanie bazy danych oraz apli-
kacji webowej służącej do zarządzania budżetem domowym. Użytkownik korzystający
z aplikacji może założyć swoje własne konto, którego dane będą przechowywane w ze-
wnętrznej bazie danych, tak jak i informacje o jego transakcjach, rodzinach oraz port-
felu. Za pomocą takiego konta można planować i odnotowywać wydatki w danym mie-
siącu, by później analizować w jakich kategoriach wydano swoje pieniądze, a ile plano-
wano wydać. Aplikacja służy również do dzielenia swoich wydatków między członkami
”rodzin”, czyli grup użytkowników, którzy postanowili taką rodzinę założyć i w niej
uczestniczyć. W panelu rodziny można umieszczać cele lub wydatki, których kwota
dzielić się będzie równomiernie między członkami tej rodziny. Zarządzane fundusze są
wirtualne i nie posiadają żadnej wartości. Daje to możliwość podglądu i analizy swoich
wydatków. Aplikacja została zaimplementowana przy użyciu Framework’a Flask oraz
języka Python. Interfejs graficzny został zaprojektowany w aplikacji Figma i zaimple-
mentowany w języku HTML, CSS oraz JavaScript. Do aplikacji zaprojektowana została
również baza danych PostgreSQL na platfromie ElephantSQL. Jest ona przeznaczona
dla każdej osoby chcącej zadbać o swój domowy budżet.


Instalacja aplikacji
 
Intstrukcja przedstawiona w tej sekcji przedstawia rozwiązanie dostępne dla systemu Windows.
Dodatkowo do uruchomienia aplikacji wymagane jest posiadanie Pythona w wersji 3.11 oraz systemu zarządania pakietami "pip", aby zainstalować resztę modułów.
Na początku należy pobrać aplikację, która dostępna jest do pobrania pod adresem https://github.com/badziej12/familybudgetapp2.git. 
Następnie za pomocą wiersza~poleceń należy przejść do katalogu projektu korzystając z komendy:

    cd familybudget
    
Z tego poziomu należy utworzyć wirtualne środowisko wpisując komendę:
    
    py -m venv *nazwa środowiska*
    
a następnie uruchomić je za pomocą komendy:
    
    Scripts\textbackslash activate
    
Po uruchomieniu należy pobrać wszystkie wymagane biblioteki i komponenty komendą:
    
    pip install -r requirements.txt
    
Na końcu należy uruchomić aplikację wpisując w okno wiersza poleceń komendę: 
    
    flask run

Od tego momentu możliwe jest połącznie się z aplikacją wpisując w pasek adresu przeglądarki adres http://localhost:5000.
