# Uniwersalne Wzorce Promptów dla Google Flow (Omni 1.1 Flash & Veo 2)

Niniejszy dokument przedstawia profesjonalne wzorce promptowania dla różnych gatunków filmowych, uwzględniając formaty poziome (16:9) oraz pionowe (9:16), a także tryby z kotwicą (Image-to-Video) i bez kotwicy (Pure Text-to-Video).

---

## 1. Struktura Idealnego Promptu dla Modelu Wideo

Model wideo Google Flow najlepiej reaguje na strukturę 5-elementową:
1. **Format i typ ujęcia**: `16:9 / Vertical 9:16 cinematic medium shot / wide landscape / macro close-up`.
2. **Sceneria i oświetlenie**: Dokładny opis środowiska, epoki, pory dnia i palety barw (np. `soft golden hour backlight, heavy atmospheric haze`).
3. **Obiekt / Postać**: Wygląd, ubiór, rekwizyty i interakcja z otoczeniem. Jeśli używamy kotwicy: odwołanie do cech ze Start Frame.
4. **Dynamika i ruch kamery**: `Slow steady push-in`, `gentle orbital pan`, `locked camera with subtle wind drift`.
5. **Estetyka kinowa**: `Authentic 35mm film grain, anamorphic lens flare, sharp volumetric lighting, photorealistic color grade`.

---

## 2. Wzorce dla Różnych Gatunków Filmowych

### A. Film Dokumentalny i Historyczny
* **A-Roll (Mówiący Świadek / Narrator) [Z Kotwicą `Start Frame`]**:
  > `Vertical 9:16 cinematic medium close-up of the Charismatic Witness (anchor face, salt-and-pepper beard, simple linen shirt) sitting in an atmospheric vintage study room filled with antique globes and leather-bound books. He speaks directly to the camera in Polish: "Treść wypowiedzi do piętnastu słów." with natural expressive lip-sync and calm authority. Locked camera with subtle slow push-in, soft warm desk lamp illumination, authentic 35mm film look.`
* **B-Roll (Przebitka historyczna) [Czysty Text-to-Video lub z kotwicą lokacji]**:
  > `16:9 cinematic wide shot of a crowded medieval marketplace in 14th-century Europe, peasants in rough wool garments bustling between timber market stalls, banners fluttering gently in the breeze, overcast moody northern sky, historical documentary realism, natural camera motion, shallow depth of field.`

---

### B. Sci-Fi / Cyberpunk / Futuryzm
* **Ujęcie Miejskie (B-Roll) [Czysty Text-to-Video]**:
  > `Vertical 9:16 cinematic drone shot descending through a colossal neon-drenched cyberpunk metropolis in the year 2088. Flying spinner vehicles stream along holographic sky-freeways through dense volumetric rain and steam. Giant glowing advertisements reflect on wet metallic skyscraper facades, deep cyan and magenta color grade, blade runner aesthetics, 8k cinematic realism.`
* **Bohater w Kokpicie / Terminalu [Z Kotwicą postaci]**:
  > `16:9 cinematic close-up of a cybernetic pilot (anchor face with subtle glowing ocular implant) inside a dimly lit spaceship cockpit. Holographic telemetry HUD reflects in his eyes as warning lights flash soft amber. Subtle camera vibration, mechanical lens flares, hyper-detailed hard-surface sci-fi design.`

---

### C. Reklama / Produkt / Tech Minimalizm
* **Prezentacja Urządzenia [Czysty Text-to-Video]**:
  > `Vertical 9:16 ultra-clean commercial hero shot of an ultra-thin matte titanium smartphone floating weightlessly in pure studio void. Smooth dramatic studio spotlight sweeps across the brushed metal edges and sapphire camera lenses. Elegant slow-motion rotation, crisp reflections, premium Apple-style product commercial, pristine minimalist lighting.`
* **Lifestyle / Użytkownik [Z Kotwicą modela/modelki]**:
  > `16:9 bright cinematic lifestyle shot of a modern professional woman (anchor face, sleek casual blazer) smiling thoughtfully while working on a transparent holographic glass tablet in a sunlit architectural penthouse. Lush indoor plants, warm morning sunlight, premium cinematic commercial grade.`

---

### D. Fantasy / Epika / Mitologia
* **Monumentalna Lokacja [Czysty Text-to-Video]**:
  > `16:9 epic cinematic panoramic vista of an ancient colossal elven stone fortress carved directly into a misty mountain waterfall. Massive carved guardian statues tower above the roaring crystal waters, golden dawn rays breaking through low clouds, Lord of the Rings scale, sweeping slow aerial pan, breathtaking fantasy realism.`
* **Mag / Wojownik [Z Kotwicą postaci]**:
  > `Vertical 9:16 dramatic portrait of an ancient sorcerer in ornate velvet robes (anchor face, long silver hair) holding an ancient gnarled oak staff topped with a glowing sapphire rune. Swirling sparks of arcane blue energy dance around his hands in a cavernous stone library, high contrast lighting, dark fantasy cinema.`

---

### E. Thriller / Kryminał / Noir
* **Śledztwo w Nocy [Czysty Text-to-Video]**:
  > `Vertical 9:16 moody neo-noir low-angle tracking shot along a dark rain-soaked cobblestone alleyway in Berlin. Streetlights cast long eerie amber reflections across wet puddles, solitary trench-coated detective walking away into dense rolling fog, slow deliberate camera push-in, suspenseful cinematic atmosphere.`
* **Przesłuchanie [Z Kotwicą postaci]**:
  > `16:9 tense dramatic close-up of a stern detective (anchor face) leaning forward under a harsh single overhead tungsten bulb in a concrete interrogation room. Heavy shadows across his eyes, curls of cigarette smoke rising into the beam of light, gritty Fincher-style color palette.`

---

### F. Stylizacja Animowana / Stylized 3D
* **Animacja Pixar/Disney 3D [Czysty Text-to-Video lub z kotwicą postaci 3D]**:
  > `Vertical 9:16 charming Pixar-style 3D animated scene: a curious little mechanical owl with brass gears and glowing amber eyes hops along a workshop table filled with whimsical wooden clockwork toys. Soft warm storybook lighting, rich subsurface scattering, smooth expressive animation, charming and magical.`

---

## 3. Kluczowe Zasady dla Dialogów i Lip-Sync (Model Omni 1.1 Flash)

1. **Język i cudzysłów**: Model musi wiedzieć, w jakim języku mówi postać (`He speaks in Polish: "..."` lub `She speaks in English: "..."`).
2. **Limit słów (Word Budget)**: Maksymalnie **14–16 słów** na 10.0-sekundowe ujęcie. Wypowiedź musi kończyć się w 7.5–8.5s, aby zapewnić min. 1.5 sekundy naturalnej pauzy przed cięciem montażowym.
3. **Kotwica w kadrze**: Postać mówiąca powinna zajmować plan bliski lub średni (Medium Shot / Medium Close-Up). Na planach ogólnych (Wide Shot) ruch warg jest mniej czytelny i może zanikać.
