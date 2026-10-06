(() => {
    const footer = document.querySelector("footer");
    if (!footer || footer.querySelector(".site-visitor-counter")) return;

    const counter = document.createElement("span");
    counter.className = "site-visitor-counter";

    const label = document.createElement("span");
    label.textContent = "Odsłony strony";

    const image = document.createElement("img");
    image.alt = "Licznik odsłon strony GrawMe";
    image.width = 110;
    image.height = 22;
    image.decoding = "async";

    const counterUrl = new URL("https://visitor-badge.laobi.icu/badge");
    counterUrl.searchParams.set("page_id", "grawme.pl");
    counterUrl.searchParams.set("left_text", "odsłony");
    counterUrl.searchParams.set("left_color", "25221b");
    counterUrl.searchParams.set("right_color", "d6b36a");
    counterUrl.searchParams.set("height", "22");

    const isLocalPreview = location.protocol === "file:" || ["localhost", "127.0.0.1"].includes(location.hostname);
    if (isLocalPreview) {
        counterUrl.searchParams.set("query_only", "true");
        image.alt = "Podgląd licznika — lokalne otwarcie nie zwiększa liczby odsłon.";
    }

    image.src = counterUrl.toString();
    counter.append(label, image);
    footer.append(document.createElement("br"), counter);
})();
