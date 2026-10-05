#!/usr/bin/env python3
"""Generate static, crawlable material pages that reuse the existing gallery photos."""

from __future__ import annotations

from html import escape
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
PHOTO_ROOT = "images/thumbs/"

CATEGORIES = [
    {
        "slug": "grawer-metal",
        "name": "Metal",
        "phrase": "metalu",
        "title": "Grawer laserowy na metalu | Realizacje GrawMe",
        "description": "Zobacz przykłady realizacji GrawMe sklasyfikowanych jako grawer laserowy na metalu. Personalizowane pamiątki i przedmioty.",
        "intro": "Na tej stronie zebrano przykłady prac z metalowej kategorii galerii GrawMe. Zdjęcia pokazują różne przedmioty i motywy; wybierz przykład, aby zobaczyć go w większym rozmiarze.",
        "ids": ["1a", "1b", "1d", "1e", "1h", "2", "3", "41", "46", "48", "51", "58", "59", "66", "82", "89", "96", "97", "100", "104", "108", "111", "120", "131", "140", "145", "146", "147", "150", "151", "152"],
    },
    {
        "slug": "grawer-drewno",
        "name": "Drewno",
        "phrase": "drewnie",
        "title": "Grawer laserowy na drewnie | Realizacje GrawMe",
        "description": "Poznaj przykłady graweru laserowego na drewnie z galerii GrawMe. Zobacz personalizowane prace i skontaktuj się w sprawie projektu.",
        "intro": "Galeria drewna przedstawia wybrane realizacje GrawMe wykonane na drewnianych przedmiotach. Każde zdjęcie to przykład gotowego wzoru lub dedykacji; efekt zależy od konkretnego przedmiotu i projektu.",
        "ids": ["1c", "1g", "33", "34", "54", "67", "99", "115", "135", "149"],
    },
    {
        "slug": "grawer-szklo-akryl",
        "name": "Szkło i akryl",
        "phrase": "szkle i akrylu",
        "title": "Grawer na szkle i akrylu | Realizacje GrawMe",
        "description": "Zobacz przykłady realizacji GrawMe w kategorii szkło i akryl oraz poznaj możliwości personalizowanego graweru.",
        "intro": "Ta część galerii zbiera prace oznaczone jako szkło i akryl. Zobacz dostępne przykłady, a jeśli masz pomysł na własny przedmiot, skontaktuj się z GrawMe, aby omówić szczegóły.",
        "ids": ["56", "74", "91"],
    },
    {
        "slug": "grawer-kamien",
        "name": "Kamień",
        "phrase": "kamieniu",
        "title": "Grawer laserowy na kamieniu | Realizacje GrawMe",
        "description": "Zobacz realizacje GrawMe sklasyfikowane jako grawer na kamieniu: przykłady pamiątek i personalizowanych wzorów.",
        "intro": "W galerii kamienia znajdziesz przykłady personalizowanych realizacji GrawMe na kamiennych przedmiotach. Zdjęcia pokazują różne motywy i projekty; kliknij wybraną pracę, aby powiększyć oryginał.",
        "ids": ["76", "80", "121", "122", "123", "126", "127", "128", "129", "130", "132", "133", "134", "135", "137", "137-heic", "137-jpg", "138", "139"],
    },
]

ALT_GROUPS = {
    "metal": ("metalu", ["1a", "1b", "1d", "1e", "1h", "2", "3", "41", "46", "48", "51", "58", "59", "66", "82", "89", "96", "97", "100", "104", "108", "111", "120", "131", "140", "145", "146", "147", "150", "151", "152"]),
    "wood": ("drewnie", ["1c", "1g", "33", "34", "54", "67", "99", "115", "135", "149"]),
    "glass": ("szkle lub akrylu", ["56", "74", "91"]),
    "stone": ("kamieniu", ["76", "80", "121", "122", "123", "126", "127", "128", "129", "130", "132", "133", "134", "135", "137", "137-heic", "137-jpg", "138", "139"]),
    "dog-tags": ("zawieszce dla psa", ["148"]),
    "pens": ("długopisie", ["112"]),
    "nameplates": ("tabliczce znamionowej", ["68", "69", "144"]),
    "medals": ("medalu lub pucharze", ["1", "40", "141", "142", "143"]),
    "jewelry": ("elemencie biżuteryjnym", ["75"]),
    "other": ("przedmiocie", ["10", "64"]),
}


def render_page(category: dict[str, object]) -> str:
    name = str(category["name"])
    phrase = str(category["phrase"])
    slug = str(category["slug"])
    photos = []
    for photo_id in category["ids"]:  # type: ignore[union-attr]
        file_name = f"prezenty z grawerem {photo_id}.webp"
        photo_url = quote(file_name, safe="-_.")
        photos.append(
            "\n        <figure class=\"photo-card\">\n"
            f"            <img src=\"{PHOTO_ROOT}{photo_url}\" alt=\"Przykład realizacji graweru na {escape(name.lower())}, zdjęcie {escape(str(photo_id))}\" loading=\"lazy\" decoding=\"async\">\n"
            f"            <figcaption>Przykład realizacji · {escape(name)}</figcaption>\n"
            "        </figure>"
        )

    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{escape(str(category['description']), quote=True)}">
    <link rel="canonical" href="https://grawme.pl/{slug}.html">
    <meta name="theme-color" content="#111111">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="pl_PL">
    <meta property="og:site_name" content="GrawMe">
    <meta property="og:title" content="{escape(str(category['title']), quote=True)}">
    <meta property="og:description" content="{escape(str(category['description']), quote=True)}">
    <meta property="og:url" content="https://grawme.pl/{slug}.html">
    <title>{escape(str(category['title']))}</title>
    <link rel="stylesheet" href="kategoria.css">
</head>
<body>
    <div class="topbar">
        <nav class="topbar-inner" aria-label="Nawigacja główna">
            <a class="brand" href="index.html">GrawMe</a>
            <a class="back-link" href="index.html#gallery-section">← Wszystkie realizacje</a>
        </nav>
    </div>
    <header class="hero">
        <div class="hero-inner">
            <p class="eyebrow">Galeria realizacji GrawMe</p>
            <h1>Grawer laserowy na {escape(phrase)}</h1>
            <p>{escape(str(category['intro']))}</p>
            <div class="hero-actions">
                <a class="button" href="index.html#contact">Kontakt do GrawMe</a>
                <a class="button secondary" href="index.html#gallery-section">Pełna galeria</a>
            </div>
        </div>
    </header>
    <main>
        <section class="intro" aria-labelledby="examples-title">
            <h2 id="examples-title">Przykłady graweru na {escape(phrase)}</h2>
            <p>Wszystkie zdjęcia pochodzą z galerii GrawMe. Pełny zbiór realizacji oraz dotychczasowe sposoby kontaktu — e-mail, TikTok, Facebook i kody QR — są dostępne na <a href="index.html">stronie głównej</a>.</p>
        </section>
        <section class="photo-grid" aria-label="Zdjęcia realizacji: {escape(name.lower())}">{''.join(photos)}
        </section>
        <section class="contact-band" aria-labelledby="contact-title">
            <h2 id="contact-title">Masz pomysł na własny grawer?</h2>
            <p>Napisz e-mail lub wybierz dotychczasowy kanał kontaktu na stronie GrawMe.</p>
            <a class="button" href="index.html#contact">Zobacz sposoby kontaktu</a>
        </section>
    </main>
    <footer>© 2026 GrawMe · Grawer laserowy na {escape(phrase)}</footer>
</body>
</html>
'''


def update_gallery_alt_text() -> None:
    import re

    photo_materials: dict[str, list[str]] = {}
    for _, (material, photo_ids) in ALT_GROUPS.items():
        for photo_id in photo_ids:
            photo_materials.setdefault(photo_id, []).append(material)

    path = ROOT / "index.html"
    with path.open(encoding="utf-8", newline="") as source_file:
        source = source_file.read()
    pattern = re.compile(
        r'(<img src="images/thumbs/prezenty%20z%20grawerem%20)([^"]+)(\.webp" alt=")[^"]+(" loading="lazy" decoding="async">)'
    )

    def describe(match: re.Match[str]) -> str:
        photo_id = match.group(2)
        materials = photo_materials.get(photo_id, [])
        if materials:
            material_text = " i ".join(materials)
            description = f"Przykład graweru laserowego na {material_text}, zdjęcie {photo_id}"
        else:
            description = f"Przykład personalizowanego graweru laserowego GrawMe, zdjęcie {photo_id}"
        return f"{match.group(1)}{photo_id}{match.group(3)}{description}{match.group(4)}"

    updated, count = pattern.subn(describe, source)
    if count != 77:
        raise RuntimeError(f"Expected to update alt text for 77 gallery images, found {count}")
    with path.open("w", encoding="utf-8", newline="") as destination:
        destination.write(updated)


def main() -> None:
    update_gallery_alt_text()
    for category in CATEGORIES:
        destination = ROOT / f"{category['slug']}.html"
        destination.write_text(render_page(category), encoding="utf-8")
        print(f"Wygenerowano {destination.name}: {len(category['ids'])} zdjęć")


if __name__ == "__main__":
    main()
