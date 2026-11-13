# LOVII — переносной пакет промтов

Все промты проверены на генерациях 13.11.2026 в H3 (модель `connector__matrix__generate_image`).
Основной промт написан универсально: **он работает в H3, Banana/Gemini, Qwen Image, Seedream и Flux одинаково**.
Ниже — что меняется в Midjourney и в H3.

---

## Что переносится как есть (90% промта)

- БАЗА (палитра, свет, стиль) — одинакова везде
- Блок персонажа (LO / голубь) — одинаково
- Сцена и композиция — одинаково
- Блок текста на вывеске — одинаково, но работает только в H3 / Banana / Qwen

## Что НЕ переносится

| Параметр | H3 (здесь) | Midjourney | Banana / Gemini | Qwen Image / Seedream |
|---|---|---|---|---|
| Формат | `aspect_ratio: "16:9"` | `--ar 16:9` | Aspect ratio 16:9 в UI | Ratio в UI |
| Версия | выбирает рантайм | `--v 6` | Nano Banana Pro | — |
| Негатив | в конце того же промта | `--no garbled text, watermark` | отдельное поле | отдельное поле |
| «8k / 4k» | `area: "4K"` | **выкинуть** | **выкинуть** | **выкинуть** |
| Референсы | `reference_images` до 16 | `--cref` + `--sref` | до 3–4 картинки | img2img |
| Текст в кадре | **отлично** | средне | **отлично** | средне |
| Кириллица | плохо | плохо | хорошо | плохо |

**Главное правило переноса:** кириллицу и длинные русские фразы не просить нигде, кроме Banana/Gemini. В H3 проси только цифры и латиницу — они рисуются точно.

## Ссылка на референсы

Для единообразия персонажа во всех моделях нужны три картинки:
- `ref1-icon.png` — иконка приложения (силуэт, рюкзак, сердце в круге)
- `ref3-wordmark.png` — вырезанный логотип «ЛОВИ» (для точных букв)
- `lovii-mascot-toon-1.jpg` — утверждённый 3D-маскот (эталон персонажа)

В H3 они грузятся через `mcode-tools upload_temp_url` → `reference_images[]`.
В Midjourney: `--cref <url маскота> --cw 100` для персонажа, `--sref <url иконки> --sw 60` для стиля.
В Banana: прикрепить как reference images, 1-я = персонаж, 2-я = эмблема.

---

## Промты


### 16:9 — касса (hero)

Голубь за стойкой лицом к зрителю, QR-карта на столе, ценники, вывеска LOVII, ёлка


**Промт:**

```
A cozy neighbourhood grocery and cafe on a snowy Saint Petersburg street. The LOVII pigeon mascot stands behind the wooden counter facing the camera, smiling warmly at the viewer with one wing raised in a friendly greeting. On the counter a customer holds a smartphone toward a small printed QR code card, the phone screen glowing. Wooden shelves behind hold jars, bread and vegetables, with small plain price tags hanging from the shelves. A decorated fir tree with warm string lights and gold ornaments stands at the left, garlands of warm bulbs overhead, mikan mandarins in a crate on the counter, steam rising from a cup of tea. A small wooden sign on the wall above the counter. The sign reads LOVII in simple bold Latin capital letters and nothing else; the letter O is a plain solid circle with nothing inside it, no heart, no symbol; the letters are black on light wood, evenly spaced, perfectly legible.

Exactly one pigeon mascot. Picture 1 - the exact character design, proportions, colours and 3D rendering style to keep: round chubby blue pigeon (#7e90c2), soft white belly, charcoal-grey beak that is definitely grey and not orange, one large round eye with white sclera, black pupil and bright catchlight, blue pilot cap with a small glossy pink heart (#f64a8a), rounded blue backpack worn on the back. The pigeon faces the camera, head-on or three-quarter front view, its face and white chest toward the viewer, a friendly open expression with slightly raised brows and a small warm smile, one wing raised in a welcoming gesture. The backpack sits behind him and is only slightly visible over one shoulder; the emblem is not the focus of the picture. The neck is short, straight and never bent, tilted or turned back.

Christmas and New Year in Saint Petersburg, warm winter evening: a decorated fir tree with warm string lights and gold ornaments, garlands of warm bulbs, mikan mandarins, warm shop windows, gentle falling snow, festive and cozy. The palette stays warm - terracotta, sage green, ochre, rose-pink accents - never icy blue.

Modern Russian digital economy aesthetic, clean UI/UX-inspired visuals, soft natural lighting, warm color palette (ochre #F0EDDE, sage green #8F9E8B, terracotta #C97C5D), realistic yet slightly stylized, human-centered, shallow depth of field, soft shadows, matte textured surfaces, natural saturation, neutral white balance, photorealistic illustration suitable for a B2B SaaS presentation.

All visible text must be spelled exactly as written, legible, no garbled letters. No watermark, no signature.
```


**H3 — параметры:** `aspect_ratio: "16:9"`, `area: "4K"`, `n: 1`


**Midjourney:** тот же промт + `--ar 16:9` (или `--ar 1:1` для квадрата) + `--v 6` + `--no watermark, garbled letters, extra limbs` + `--style raw`


**Banana / Gemini:** тот же промт как есть. Aspect ratio выставить в UI. Кириллицу добавлять можно — там она читается.


**Qwen Image / Seedream / Flux:** тот же промт как есть. Если текст на вывеске поехал — рисуй его в макете поверх.

---


### 16:9 — меню с ценами

Грифельная доска с ценами 120 ₽ / 180 ₽ / 450 ₽, чистая вывеска LOVII


**Промт:**

```
Inside a warm neighbourhood cafe at New Year. The LOVII pigeon mascot stands in front of a brick wall facing the camera, friendly and welcoming, one wing resting on the wooden counter beside him. On the brick wall next to him hangs a dark chalkboard with three clean handwritten chalk prices reading 120, 180 and 450, each followed by a ruble sign. A cash register and a coffee machine sit on the counter, croissants on a plate, mikan mandarins in a bowl, a decorated fir tree with warm string lights at the right, garlands of warm bulbs above. A small wooden sign stands on the counter. The sign reads LOVII in simple bold Latin capital letters and nothing else; the letter O is a plain solid circle with nothing inside it, no heart, no symbol; the letters are black on light wood, evenly spaced, perfectly legible.

Exactly one pigeon mascot. Picture 1 - the exact character design, proportions, colours and 3D rendering style to keep: round chubby blue pigeon (#7e90c2), soft white belly, charcoal-grey beak that is definitely grey and not orange, one large round eye with white sclera, black pupil and bright catchlight, blue pilot cap with a small glossy pink heart (#f64a8a), rounded blue backpack worn on the back. The pigeon faces the camera, head-on or three-quarter front view, its face and white chest toward the viewer, a friendly open expression with slightly raised brows and a small warm smile, one wing raised in a welcoming gesture. The backpack sits behind him and is only slightly visible over one shoulder; the emblem is not the focus of the picture. The neck is short, straight and never bent, tilted or turned back.

Christmas and New Year in Saint Petersburg, warm winter evening: a decorated fir tree with warm string lights and gold ornaments, garlands of warm bulbs, mikan mandarins, warm shop windows, gentle falling snow, festive and cozy. The palette stays warm - terracotta, sage green, ochre, rose-pink accents - never icy blue.

Modern Russian digital economy aesthetic, clean UI/UX-inspired visuals, soft natural lighting, warm color palette (ochre #F0EDDE, sage green #8F9E8B, terracotta #C97C5D), realistic yet slightly stylized, human-centered, shallow depth of field, soft shadows, matte textured surfaces, natural saturation, neutral white balance, photorealistic illustration suitable for a B2B SaaS presentation.

All visible text must be spelled exactly as written, legible, no garbled letters. No watermark, no signature.
```


**H3 — параметры:** `aspect_ratio: "16:9"`, `area: "4K"`, `n: 1`


**Midjourney:** тот же промт + `--ar 16:9` (или `--ar 1:1` для квадрата) + `--v 6` + `--no watermark, garbled letters, extra limbs` + `--style raw`


**Banana / Gemini:** тот же промт как есть. Aspect ratio выставить в UI. Кириллицу добавлять можно — там она читается.


**Qwen Image / Seedream / Flux:** тот же промт как есть. Если текст на вывеске поехал — рисуй его в макете поверх.

---


### 1:1 — портрет

Голубь машет крылом, круглая вывеска LOVII, ёлка с золотыми шарами


**Промт:**

```
Close-up portrait of the LOVII pigeon mascot facing the camera head-on, cheerful, one wing raised in a wave, big friendly eye, blue pilot cap with a small pink heart on the front. Behind him a round wooden sign with the word LOVII in simple bold Latin capital letters, a decorated fir tree with warm string lights and gold ornaments, mikan mandarins on the counter, soft falling snow, warm golden light. Square composition, festive, clean background. The sign reads LOVII in simple bold Latin capital letters and nothing else; the letter O is a plain solid circle with nothing inside it, no heart, no symbol; the letters are black on light wood, evenly spaced, perfectly legible.

Exactly one pigeon mascot. Picture 1 - the exact character design, proportions, colours and 3D rendering style to keep: round chubby blue pigeon (#7e90c2), soft white belly, charcoal-grey beak that is definitely grey and not orange, one large round eye with white sclera, black pupil and bright catchlight, blue pilot cap with a small glossy pink heart (#f64a8a), rounded blue backpack worn on the back. The pigeon faces the camera, head-on or three-quarter front view, its face and white chest toward the viewer, a friendly open expression with slightly raised brows and a small warm smile, one wing raised in a welcoming gesture. The backpack sits behind him and is only slightly visible over one shoulder; the emblem is not the focus of the picture. The neck is short, straight and never bent, tilted or turned back.

Christmas and New Year in Saint Petersburg, warm winter evening: a decorated fir tree with warm string lights and gold ornaments, garlands of warm bulbs, mikan mandarins, warm shop windows, gentle falling snow, festive and cozy. The palette stays warm - terracotta, sage green, ochre, rose-pink accents - never icy blue.

Modern Russian digital economy aesthetic, clean UI/UX-inspired visuals, soft natural lighting, warm color palette (ochre #F0EDDE, sage green #8F9E8B, terracotta #C97C5D), realistic yet slightly stylized, human-centered, shallow depth of field, soft shadows, matte textured surfaces, natural saturation, neutral white balance, photorealistic illustration suitable for a B2B SaaS presentation.

All visible text must be spelled exactly as written, legible, no garbled letters. No watermark, no signature.
```


**H3 — параметры:** `aspect_ratio: "1:1"`, `area: "4K"`, `n: 1`


**Midjourney:** тот же промт + `--ar 1:1` (или `--ar 1:1` для квадрата) + `--v 6` + `--no watermark, garbled letters, extra limbs` + `--style raw`


**Banana / Gemini:** тот же промт как есть. Aspect ratio выставить в UI. Кириллицу добавлять можно — там она читается.


**Qwen Image / Seedream / Flux:** тот же промт как есть. Если текст на вывеске поехал — рисуй его в макете поверх.

---


## Что проверено на этих кадрах

| Элемент | Результат |
|---|---|
| Цены `120 ₽ / 180 ₽ / 450 ₽` | отрисованы **точно**, каждая цифра |
| Латиница на вывеске `LOVII` | **идеально** |
| QR-код на карточке | **настоящий читаемый паттерн** |
| Крупная цифра на экране (`500`) | **безупречно** |
| Кириллица длинной фразой | мусор — рисуем в макете |
| Буква O в слове | слипается с сердцем → страховка в промте обязательна |

## Обязательные страховки (вставлять всегда)

```
the letter O is a plain solid circle with nothing inside it, no heart, no symbol
the beak is charcoal grey, definitely grey and not orange
exactly one raised glossy white circular plaque on the outer face of the backpack
the pigeon faces the camera, head-on or three-quarter front view
```

Последняя строка — не косметика. Без неё голубь разворачивается затылком, потому что «рюкзак на спине» + «эмблема лицом к камере» взаимно исключают лицо к зрителю.
