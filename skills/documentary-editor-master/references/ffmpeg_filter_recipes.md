# Przepisy na Filtry FFmpeg w Postprodukcji Filmowej

## 1. Dynamiczny Sidechain Ducking (Broadcast Standard)

```text
[1:a]loudnorm=I=-24:TP=-2:LRA=11,aloop=loop=-1:size=2e+09,atrim=0:DURATION[music_loop];
[music_loop][0:a]sidechaincompress=threshold=0.08:ratio=5:attack=100:release=1000[music_ducked];
[0:a][music_ducked]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]
```
* `threshold=0.08` – czułość wyzwalania kompresji podkładu mową aktora.
* `ratio=5` – stopień stłumienia muzyki (~5-7 dB obniżenia poziomu w trakcie mowy).
* `attack=100` – łagodne wejście duckingu (100 ms) eliminujące stuki.
* `release=1000` – powolny, filmowy powrót poziomu muzyki po zakończeniu kwestii (1 sekunda).

---

## 2. Prawidłowy Miks Audio Lektora i Ambientu w B-Roll

```text
[0:a]loudnorm=I=-16:TP=-1.5:LRA=7,apad=whole_dur=DURATION[lektor_padded];
[ambient_concat]volume=0.08[ambient_low];
[lektor_padded][ambient_low]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]
```
* **Żelazna kolejność**: `[lektor_padded]` musi być na wejściu pierwszym (`[0]`). Przy `duration=first` gwarantuje to, że lektor nigdy nie zostanie ucięty przed końcem zdania.

---

## 3. Wtapianie Napisów ASS z Kodowaniem Znaków Windows/Linux

```text
-filter_complex "[0:v]ass='sciezka_do_napisow.ass'[vout]"
```
* W systemie Windows dwukropek po literze dysku musi być poprzedzony backslashem (`C\:/path/to/file.ass`), a ukośniki zamienione na slashe (`/`).
