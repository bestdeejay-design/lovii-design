# LOVII — видео-промты для H3 / H3-Max / Hailuo-2.3

Один кадр-основа, три движка, идентичный визуальный промт — чтобы сравнение было честным.
Первый кадр: `launch-3.jpg` (рилс 9:16, голубь с пакетом LOVII).

**Параметры:** `duration: 6`, `resolution: 768P`, `ratio: adaptive`, `reference_type: "first_frame"`.
6 секунд и 768P — единственные значения, валидные одновременно для всех трёх моделей, поэтому сравнение получается честным.

---

## Промт для MiniMax-H3 (и H3-Max — тот же текст, со звуком)

```
I2VA:
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Soft 3D animated-film rendering, warm golden Christmas and New Year palette of ochre, sage green and terracotta with rose-pink accents. Vertical medium close-up of the chubby blue pigeon mascot in a blue pilot cap with a small glossy pink heart, standing on a snowy Saint Petersburg pavement, holding a small wrapped gift box with a green ribbon in one wing and a kraft paper grocery bag printed with "LOVII" in bold black capitals in the other. The camera performs a very slow push in. The pigeon blinks once, its chest rising and falling with a breath, the kraft bag swaying softly on its handle and the green ribbon ends fluttering in the cold air. Fresh snowflakes drift down through the warm light, the golden string lights on the decorated fir tree behind glow and twinkle softly, and the bokeh highlights in the blurred shop windows shimmer. The pigeon shifts its weight and turns its head slightly toward the camera with a friendly open expression, keeping both wings holding the bag and the gift steady.

overall_soundscape: Soft crunch of snow under the pigeon's feet, the faint rustle of the paper bag handle, a small metallic tink of the gift ribbon, distant muffled city hum, light wind, and a soft crackle of string lights in the background.

non_diegetic_music: A gentle warm orchestral bed with soft plucked strings and a light bell motif, slow tempo, very low dynamics, rising slightly in the final second.
```

## Промт для MiniMax-Hailuo-2.3 (тот же кадр, без звука)

Модель бесшумная — аудио-поля убраны, визуальная часть идентична.

```
Soft 3D animated-film rendering, warm golden Christmas and New Year palette of ochre, sage green and terracotta with rose-pink accents. Vertical medium close-up of the chubby blue pigeon mascot in a blue pilot cap with a small glossy pink heart, standing on a snowy Saint Petersburg pavement, holding a small wrapped gift box with a green ribbon in one wing and a kraft paper grocery bag printed with "LOVII" in bold black capitals in the other. The camera performs a very slow push in. The pigeon blinks once, its chest rising and falling with a breath, the kraft bag swaying softly on its handle and the green ribbon ends fluttering in the cold air. Fresh snowflakes drift down through the warm light, the golden string lights on the decorated fir tree behind glow and twinkle softly, and the bokeh highlights in the blurred shop windows shimmer. The pigeon shifts its weight and turns its head slightly toward the camera with a friendly open expression, keeping both wings holding the bag and the gift steady.
```

---

## Допустимые значения по моделям

| | H3 | H3-Max | Hailuo-2.3 |
|---|---|---|---|
| `duration` | 4–15 | 5–15 | 6 или 10 |
| `resolution` | 768P, 2K | 480P, 768P | 768P, 1080P |
| `ratio` | adaptive (keyframe) | adaptive (keyframe) | adaptive |
| Референсы | 1–9 картинок / видео / аудио | только ключевые кадры | только первый кадр |
| Звук | нативный | нативный | **нет** |
| `reference_type` | first_frame / last_frame | first_frame / last_frame | first_frame / subject |

## Что дальше

После подтверждения: загружаю `launch-3.jpg`, отправляю три задачи по очереди, поднимаю фоновый поллер и отдаю все три MP4 для сравнения.

**Следующие сцены в очереди** (готовы тем же способом):

1. **«Касса»** 16:9 — first: `lovii-scene-A-lavka-2.jpg`, last: `lovii-scene-A-lavka-1.jpg` → медленный наезд на стойку
2. **«Ло машет»** 1:1 — first: `lovii-mascot-toon-1.jpg` → моргает, взмахивает крылом
3. **«Флэтлей»** 1:1 — first: `lovii-scene-D-flatlay.jpg` → свеча мерцает, снег падает
4. **«Ярмарка»** 16:9 — first: `lovii-scene-B-yarmarka.jpg` → движение по прилавкам, огни гирлянд

## Важное

- Генерация видео **платная**. Правило: на тарифах M Plan, покрывающих модель, видео списывается из недельного лимита M Plan, если остатка хватает на всё видео целиком; иначе — с баланса аккаунта. Старые лимиты Token Plan оплачивают только H2.3.
- Сумму считает сервис — вручную не оценить.
- Одно подтверждение покрывает только перечисленные отправки.
