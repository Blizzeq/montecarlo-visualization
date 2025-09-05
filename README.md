# Monte Carlo π Visualization

Interaktywna wizualizacja algorytmu Monte Carlo do wyznaczania wartości liczby π z zaawansowanymi funkcjami analizy i wizualizacji.

## 📊 Funkcjonalności

### 🎯 Symulacja Monte Carlo
- **Wizualizacja w czasie rzeczywistym** - punkty pojawiają się z animacjami
- **Kontrola prędkości** - od 10ms do 1000ms między iteracjami
- **Rozmiar partii** - 1-1000 punktów na iterację
- **Dokładność na żywo** - estymacja π z błędem i procentową dokładnością

### 📈 Analizy Statystyczne
- **Wykres zbieżności** - jak estymacja π zmienia się w czasie
- **Wykres błędu** - błąd bezwzględny w skali logarytmicznej
- **Rozkład punktów** - histogram odległości od środka
- **Statystyki wydajności** - punkty/sekundę, czas obliczeń

### 🎨 Interfejs Użytkownika
- **Dark theme** - profesjonalny wygląd
- **Panel kontrolny** - pełne sterowanie symulacją
- **3 zakładki statystyk** - zbieżność, statystyki, rozkład
- **Interaktywne canvas** - kliknij PPM aby przełączyć siatkę

## 🛠️ Instalacja

### Wymagania
- Python 3.8+
- PySide6
- NumPy
- Matplotlib  
- PyQtGraph

### Instalacja zależności
```bash
pip install -r requirements.txt
```

### Uruchomienie
```bash
python main.py
```

## 🎮 Jak używać

1. **Uruchom aplikację** - `python main.py`
2. **Naciśnij "▶ Start"** - rozpocznij symulację Monte Carlo
3. **Dostosuj ustawienia**:
   - Prędkość symulacji (slider)
   - Rozmiar partii punktów (spinbox)
   - Opcje wyświetlania (checkboxy)
4. **Analizuj wyniki** w zakładkach:
   - **Zbieżność** - wykresy π(t) i błędu(t)
   - **Statystyki** - aktualne i historyczne dane
   - **Rozkład** - histogram i metryki wydajności

### Skróty klawiszowe
- `Ctrl+R` - Reset symulacji
- `Ctrl+T` - Pokaż/ukryj panel statystyk
- `Ctrl+Q` - Wyjście
- `PPM na canvas` - Przełącz siatkę współrzędnych

## 🧮 Jak działa algorytm Monte Carlo

1. **Generuj losowe punkty** w kwadracie [-1,1] × [-1,1]
2. **Sprawdź czy punkt w kole** - jeśli x² + y² ≤ 1
3. **Oblicz stosunek** - punkty_w_kole / wszystkie_punkty ≈ π/4
4. **Estymuj π** - π ≈ 4 × stosunek

### Teoretyczne podstawy
- **Pole koła**: π × r² = π (dla r=1)  
- **Pole kwadratu**: (2r)² = 4 (dla r=1)
- **Stosunek pól**: π/4
- **Prawo wielkich liczb**: gdy n→∞, estymacja→π

## 🏗️ Architektura projektu

```
montecarlo-visualization/
├── main.py                 # Punkt wejścia aplikacji
├── requirements.txt        # Zależności Python
├── proces.md              # Dokumentacja procesu tworzenia
├── README.md              # Ten plik
└── src/
    ├── core/
    │   └── monte_carlo.py  # Algorytmy Monte Carlo
    ├── ui/
    │   ├── main_window.py  # Główne okno Qt
    │   └── widgets/
    │       ├── simulation_canvas.py   # Canvas wizualizacji
    │       ├── control_panel.py       # Panel kontrolny
    │       └── statistics_panel.py    # Panel statystyk
    └── utils/
        └── colors.py       # Kolory i style UI
```

## 🔧 Rozszerzenia

Projekt można łatwo rozszerzyć o:

1. **Inne problemy Monte Carlo**:
   - Igła Buffona
   - Całkowanie funkcji
   - Problemy prawdopodobieństwa

2. **Dodatkowe wizualizacje**:
   - Heatmapy gęstości punktów
   - Animacje 3D
   - Wykresy konturowe

3. **Eksport danych**:
   - CSV z wynikami
   - PNG z wykresami  
   - PDF z raportem

4. **Optymalizacje**:
   - Wielowątkowość
   - GPU computing (CUDA)
   - Streaming danych

## 📊 Przykładowe wyniki

- **100 punktów**: π ≈ 3.16 (błąd ~0.02)
- **1,000 punktów**: π ≈ 3.148 (błąd ~0.006)  
- **10,000 punktów**: π ≈ 3.1416 (błąd ~0.0001)
- **100,000 punktów**: π ≈ 3.14159 (błąd ~0.00001)

**Błąd maleje jako 1/√n** gdzie n to liczba punktów.

## 🤝 Rozwój

Kod jest napisany w sposób modularny i łatwy do rozszerzania:

- **Czysta architektura** - podział na core/ui/utils
- **Qt Signals/Slots** - luźne powiązania między komponentami  
- **Type hints** - klarowność kodu
- **Dokumentacja** - komentarze i proces.md

## 📄 Licencja

Ten projekt służy celom edukacyjnym i demonstracyjnym.