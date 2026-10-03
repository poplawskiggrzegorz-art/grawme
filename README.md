# GrawMe

## Konwersja zdjęć do WebP

Wymagany jest Python 3.12 lub nowszy. Oficjalny instalator Windows jest dostępny na [python.org](https://www.python.org/downloads/windows/).

Uruchom `konwertuj_zdjecia_webp.bat` dwukrotnym kliknięciem. Program zainstaluje brakujące biblioteki, a następnie zapisze skompresowane kopie w `images/webp`. Zdjęcia źródłowe pozostają bez zmian.

Można też uruchomić program z terminala:

```powershell
py -3 -m pip install -r requirements.txt
py -3 convert_to_webp.py
```

Domyślna jakość to 82/100. Aby zmienić jakość albo ponownie przeliczyć istniejące WebP:

```powershell
py -3 convert_to_webp.py --quality 78 --overwrite
```

Program obsługuje JPG, JPEG, PNG oraz HEIC/HEIF. Plik JPG z uciętymi danymi próbuje odzyskać w trybie awaryjnym.
