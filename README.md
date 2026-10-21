# 問路小達人 · ¡Me he perdido!

**Juego para practicar a pedir y entender direcciones en chino (mandarín de Taiwán).**
Escuchas una indicación, caminas por un mapa y llegas al destino.

> 🇹🇼 Hecho para estudiantes hispanohablantes de chino · 每天一分鐘 (@cadadiaunosminutos_ben_chino)

**▶ Jugar:** https://wangchiapin.github.io/Me-he-perdido/ (se abre en el celular o en la computadora, no hay que instalar nada)

---

## ¿Cómo se juega?

1. Escribe tu nombre y elige un nivel.
2. Escucha la indicación (o léela). Puedes volver a oírla las veces que quieras con 🔊.
3. Mueve al personaje con los botones: **直走** (recto), **左轉** (izquierda), **右轉** (derecha) y, desde el nivel 2, **過馬路** (cruzar la calle; hay que pulsarlo en la esquina donde lo dice la indicación).
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
- **過馬路** = cruzar la calle siguiendo recto; se pulsa el botón de cruzar y luego se avanza.

## Ayudas y ajustes

Los ajustes se guardan en la clave compartida `hanziGames.settings` (la misma en todos los juegos de la familia): `{v:1, script, lang, phon, rate}`. Si cambias algo aquí, los otros juegos lo ven (y al revés).

- Caracteres: **繁體** o **简体** (por defecto, tradicional)
- Idioma: **Español**, **English** o **中文** (solo chino: toda la interfaz y el vocabulario en chino, sin traducciones). La traducción se muestra solo si el idioma no es chino; ya no hay un interruptor aparte.
- Pronunciación: **Pinyin** (por defecto, con lecturas de Taiwán), **注音 zhuyin**, **ambos** o **ninguna**
- Velocidad de la voz: lenta (0.45), normal (0.65) o rápida (0.85); siempre voz `zh-TW`
- **Texto** (encendido por defecto): apágalo para practicar solo con el oído (🎧)
- **Por partes**: la indicación se escucha en trozos cortos con «Parte siguiente»
- **Mapa**: elige uno de los 6 mapas o aleatorio
- 📖 Vocabulario del mapa y palabras útiles (先、然後、再、最後…)
- Fotos opcionales: si pones `photos/<clave>.jpg` (p. ej. `bank.jpg`) se muestra al terminar cada pregunta

El nombre del jugador, el mapa elegido, «Texto» y «Por partes» y la clasificación local se guardan solo en este juego (`askdir_settings`, `askdir_lb`). Los ajustes antiguos de `askdir_settings` se pasan a la clave compartida la primera vez.

Se puede abrir con parámetros para saltarse la pantalla de inicio, por ejemplo:
`index.html?name=Ana&script=trad&lang=es` (`script`: `trad`/`tw` o `simp`/`cn`; `lang`: `es`, `en` o `zh`).

## Mapas

Seis mapas sencillos: **便利商店街** (calle comercial), **車站前** (frente a la estación), **夜市** (mercado nocturno), **校園附近** (cerca de la escuela), **醫院附近** (cerca del hospital) y **捷運站出口** (salida del metro), con 31 lugares en total.

---

## 繁體中文簡介

這是一個練習「問路、指路」的小遊戲，給說西班牙語的華語學習者使用。

- 聽一段指路的話，用「直走、左轉、右轉、過馬路」按鈕讓小人走，走到目的地按「我到了」。
- 新功能：只聽不看（隱藏文字）、分段聽、可選地圖、真正的「過馬路」按鈕、6 張地圖、可放自己的街景照片。
- 共 4 個關卡：方向詞 → 路口與過馬路 → 位置詞（對面、旁邊）→ 綜合挑戰。
- 設定和其他遊戲共用（localStorage 的 `hanziGames.settings`）：繁體／簡體；語言可選西班牙文、英文或「中文」（純中文介面，不顯示翻譯）；讀音可選拼音（台灣讀音，預設）、注音、拼音＋注音或不顯示；語音速度慢 0.45／中 0.65／快 0.85。
- 只有語言不是「中文」時才會顯示翻譯，沒有另外的翻譯開關。
- 網址參數：`?name=名字&script=trad|simp（或 tw|cn）&lang=es|en|zh`。
- 每一題的指路句、拼音、翻譯、路線和答案都由同一份資料產生，不會互相對不上。

## Para quien mantiene el proyecto

Es un único archivo, `index.html`, sin dependencias. Funciona directamente en GitHub Pages
(Settings → Pages → Deploy from a branch → `main` / root).

### Clasificación (Firebase)

La clasificación en línea ya está conectada al proyecto `memorma-24dab` (compartido con Memorama y Ordena el Armario), con inicio de sesión anónimo; la configuración está en la constante `FIREBASE_CONFIG` al inicio del `<script>` de `index.html`. Si no se puede conectar, la clasificación se guarda solo en el dispositivo.
Se usan las colecciones `askDirections_L1` … `askDirections_L4` (un documento por dispositivo y nivel, solo se
guarda la mejor puntuación; se muestran los 10 mejores). Las reglas de Firestore de ese proyecto ya permiten esas colecciones.
Desde 2026-10-21 también se registran visitas, inicios y partidas terminadas (colecciones `visits` y `plays`; GA no cambia).
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

Pruebas automáticas: `python3 tools/test/test_game.py` (requiere `pip install playwright` y Chromium).
