# familybudgetapp2

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
