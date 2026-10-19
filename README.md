# 問路小達人 · ¡Me he perdido!

**Juego para practicar a pedir y entender direcciones en chino (mandarín de Taiwán).**
Escuchas una indicación, caminas por un mapa y llegas al destino.

> 🇹🇼 Hecho para estudiantes hispanohablantes de chino · 每天一分鐘 (@cadadiaunosminutos_ben_chino)

**▶ Jugar:** https://wangchiapin.github.io/Me-he-perdido/ (se abre en el celular o en la computadora, no hay que instalar nada)

---

## ¿Cómo se juega?

1. Escribe tu nombre y elige un nivel.
2. Escucha la indicación (o léela). Puedes volver a oírla las veces que quieras con 🔊.
3. Mueve al personaje con tres botones: **直走** (recto), **左轉** (izquierda), **右轉** (derecha).
4. Cuando creas que llegaste, pulsa **¡Llegué!**
5. Si te equivocas, el juego te muestra tu ruta y la ruta correcta, y puedes ver cómo se camina.

Cada ronda tiene 8 preguntas y cada acierto vale 10 puntos. Hay clasificación por nivel.

**Importante:** izquierda y derecha dependen de hacia dónde mira el personaje (la flecha negra), no de la pantalla. Ahí está la práctica.

## Niveles

| Nivel | Qué practicas | Ejemplo |
|---|---|---|
| 1 · Direcciones | 直走、左轉、右轉、左手邊／右手邊 | 先直走，再右轉，再直走。銀行就在你的左手邊。 |
| 2 · Esquinas y cruzar | 第一／第二／第三個路口、下一個路口、過馬路 | 直走到第二個路口，左轉，再直走到下一個路口。 |
| 3 · Posiciones | 對面、旁邊, y usar los edificios como referencia | 一直走，右手邊是銀行，過了銀行就左轉。 |
| 4 · Reto combinado | Indicaciones largas con todo lo anterior | 直走到第一個路口，左轉，再一直走，右手邊是公園，過了公園就右轉，再直走到第二個路口。 |

Notas de vocabulario:
- **直走** = avanzar hasta la siguiente esquina.
- Las esquinas se cuentan desde donde estás parado.
- **過馬路** = seguir recto al otro lado de la calle, sin girar.

## Ayudas y ajustes

- Caracteres: **繁體** o **简体**
- Idioma de la interfaz y la traducción: **Español** o **English**
- **Pinyin** (apagado por defecto) con lecturas de Taiwán
- **Traducción** (encendida por defecto)
- Velocidad de la voz: lenta, normal o rápida
- 📖 Vocabulario del mapa

Se puede abrir con parámetros para saltarse la pantalla de inicio, por ejemplo:
`index.html?name=Ana&script=tw&lang=es` (`script`: `tw` o `cn`; `lang`: `es` o `en`).

## Mapas

Tres mapas sencillos: **便利商店街** (calle comercial), **車站前** (frente a la estación) y **夜市** (mercado nocturno), con 27 lugares en total.

---

## 繁體中文簡介

這是一個練習「問路、指路」的小遊戲，給說西班牙語的華語學習者使用。

- 聽一段指路的話，用「直走、左轉、右轉」三個按鈕讓小人走，走到目的地按「我到了」。
- 共 4 個關卡：方向詞 → 路口與過馬路 → 位置詞（對面、旁邊）→ 綜合挑戰。
- 可選繁體／簡體、西班牙文／英文、拼音（台灣讀音）、三種語音速度。
- 每一題的指路句、拼音、翻譯、路線和答案都由同一份資料產生，不會互相對不上。

## Para quien mantiene el proyecto

Es un único archivo, `index.html`, sin dependencias. Funciona directamente en GitHub Pages
(Settings → Pages → Deploy from a branch → `main` / root).

### Clasificación (Firebase)

Por defecto la clasificación se guarda solo en el dispositivo. Para compartirla, pega la configuración web de
Firebase en la constante `FIREBASE_CONFIG` al inicio del `<script>` de `index.html`.
Se usan las colecciones `askDirections_L1` … `askDirections_L4` (un documento por dispositivo y nivel, solo se
guarda la mejor puntuación). Hay que permitir lectura y escritura en esas colecciones en las reglas de Firestore.
Si usas GA4, escribe el identificador en `GA_ID`.

### Añadir o cambiar preguntas

Las preguntas se generan con los scripts de `tools/`:

```bash
cd tools
python3 gen_questions.py      # crea questions.json (vocabulario y mapas están al inicio del archivo)
python3 verify_questions.py   # comprueba rutas, destinos y que el pinyin coincida con los caracteres
python3 build.py              # escribe ../index.html
```

Para agregar un edificio o un mapa, edita los diccionarios `B` y `MAPS` en `tools/gen_questions.py`.
Cada edificio lleva escritura tradicional y simplificada, pinyin con lectura de Taiwán, y traducción al español y al inglés.
