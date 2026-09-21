"""
Szablon pliku danych scenariuszowych dla filmu dokumentalnego.
Zawiera definicje kwestii lektora (VOICEOVERS) oraz listę scen (SCENES).
"""

VOICEOVERS = {
    "vo_s02_kontekst": (
        "[thoughtful] Pod koniec lat dziewięćdziesiątych świat zachłysnął się nową obietnicą. "
        "W roku tysiąc dziewięćset dziewięćdziesiątym piątym sieć dopiero raczkowała. [pause] "
        "Pięć lat później miliony ludzi uwierzyły, że stare zasady ekonomii przestały obowiązywać."
    ),
    "vo_s04_przelom": (
        "[thoughtful] Dziesiątego marca roku dwutysięcznego rynek osiągnął historyczny szczyt. "
        "A potem runął w dół. [ironic] Technologia była prawdziwa. To ludzkie oczekiwania były całkowicie oderwane od rzeczywistości."
    )
}

SCENES = [
    {
        "id": "s01",
        "type": "A-ROLL",
        "name": "Świadek: Otwarcie dokumentu",
        "anchor": "swiadek_dziejow.jpg",
        "prompt": "16:9 cinematic medium shot of the Charismatic Witness (mature 45yo man, salt-and-pepper beard, simple linen shirt, reference anchor face). He speaks in Polish: 'Najgroźniejsze złudzenia rodzą się wtedy, kiedy prawdziwa rewolucja dostaje absurdalną wycenę.'. Subtle slow push-in, 16:9.",
        "dialogue": "Najgroźniejsze złudzenia rodzą się wtedy, kiedy prawdziwa rewolucja dostaje absurdalną wycenę."
    },
    {
        "id": "s02",
        "type": "B-ROLL",
        "name": "Lektor: Narodziny hype'u",
        "vo_key": "vo_s02_kontekst",
        "shots": [
            {"id": "s02_a", "prompt": "16:9 cinematic macro close-up of vintage 1995 dial-up modem blinking green LEDs in dark room."},
            {"id": "s02_b", "prompt": "16:9 busy trading floor in 1999, young brokers cheering at soaring green stock tickers."}
        ]
    }
]
