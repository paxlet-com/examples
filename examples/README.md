# 📚 Paxlet Ecosystem Examples Catalog

Zbiór oficjalnych przykładów demonstrujących możliwości pakietów **Paxlet**, kompilatora **nl-dsl-sh** oraz silnika orkiestracji **Taskand**.

---

## 🗂️ Spis kategorii

### 1. `01-paxlet-basics/` — Podstawowe pakiety Paxlet
Wszystkie pakiety posiadają manifest `paxlet.json`, deklarację uprawnień i wejść/wyjść, generują certyfikaty kryptograficzne `receipt.json`:
- **`hello/`**: Prosty pakiet powitalny przyjmujący `{"name": "..."}` i zwracający `{"message": "Hello, ..."}`.
- **`statistics-mean/`**: Obliczanie średniej arytmetycznej z tablicy liczb `{"values": [...]}`.
- **`text-wordcount/`**: Zliczanie słów w tekście `{"text": "..."}`.
- **`sensor-calibrate/`**: Kalibracja odczytów czujników IoT `{"values": [...], "gain": ..., "offset": ...}`.
- **`science-fasta-gc/`**: Analiza bioinformatyczna plików FASTA (obliczanie długości sekwencji i frakcji GC) z dostępem do lokalnego pliku `data/sample.fasta`.

### 2. `02-nldsl-compilation/` — Kompilacja języka naturalnego (`nl-dsl-sh`)
- **`catalog-offline/`**: Praca w trybie offline bez połączenia z LLM – dopasowywanie aliasów w języku naturalnym do zaufanych skryptów powłoki (`Catalog.import_script`), budowanie planu i wykonanie.
- **`modular-scripts/`**: Modułowe skrypty powłoki z importem bibliotek (`source ./lib.sh`).
- **`compiled-bundle/`**: Skompilowany, hermetyczny pakiet Paxlet wygenerowany automatycznie przez `nl-dsl-sh`.

### 3. `03-taskand-orchestration/` — Orkiestracja zadań w Taskand
- **`network-scan/`**: Skanowanie urządzeń sieciowych z weryfikacją cyfrowego bliźniaka i niezmienności rejestru (`network-scan-task.mjs`).
- **`web-twin/`**: Preflight webowy w sandboxie `bubblewrap` z testem blokowania kroków zależnych (*dependency gating* na statusie `PARTIAL`).
- **`shell-workflow/`**: Przykładowe plany JSON i uprawnienia dla powłoki Taskand (`taskand shell`).

### 4. `04-complex-scenarios/` — Złożone scenariusze autonomii
- **`autonomous-devops-pipeline/`**: Wieloetapowy potok: inspekcja telemetrii systemu -> bramka jakościowa / detekcja anomalii -> synteza raportu z audytu -> hermetyzacja w Paxlet z kryptograficznym `receipt.json`.
- **`multi-language-dag/`**: Heterogeniczny graf DAG łączący kroki w Bashu (przygotowanie danych) i Pythonie (analiza statystyczna) ze współdzieleniem stanu.
- **`digital-twin-browser-agent/`**: Cyfrowy bliźniak agenta przeglądarkowego wykonujący asercje DOM, nawigację i interakcję w odizolowanym profilu.

---

## 🧪 Uruchomienie testów weryfikacyjnych

Wszystkie przykłady są automatycznie testowane przez zestaw testów:
```bash
python3 tests/test_all_examples.py
```
