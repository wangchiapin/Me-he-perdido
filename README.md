# 問路小達人 · Pregunta el camino

(Nombre del primer día: ¡Me he perdido!; el nombre del repositorio y de la URL sigue siendo `Me-he-perdido`. El nombre actual es el de `<title>` y `og:title` en `index.html`.)

**Juego para practicar a pedir y entender direcciones en chino (mandarín de Taiwán).**
Escuchas una indicación, caminas por un mapa y llegas al destino.

> 🇹🇼 Hecho para estudiantes hispanohablantes de chino · 每天一分鐘 (@cadadiaunosminutos_ben_chino)

**▶ Jugar:** https://wangchiapin.github.io/Me-he-perdido/ (se abre en el celular o en la computadora, no hay que instalar nada)

---

## ¿Cómo se juega?

1. Escribe tu nombre y elige un nivel.
2. Escucha la indicación con 🔊 (puedes repetirla las veces que quieras). El texto está oculto al empezar: si lo necesitas pulsa «Ver texto» (solo el chino) y después «Ver lectura y traducción». Al responder se muestra todo.
3. Mueve al personaje con los botones: **直走** (recto), **左轉** (izquierda), **右轉** (derecha) y, desde el nivel 2, **過馬路** (cruzar la calle; hay que pulsarlo en la esquina donde lo dice la indicación).
4. Cuando creas que llegaste, pulsa **¡Llegué!**
5. Si te equivocas, el juego te muestra tu ruta y la ruta correcta, y puedes ver cómo se camina.

Cada ronda tiene 8 preguntas y cada acierto vale 10 puntos. Hay clasificación por nivel.

**Importante:** izquierda y derecha dependen de hacia dónde mira el personaje (una persona o un animal visto desde arriba, distinto en cada pregunta), no de la pantalla. Ahí está la práctica. Al revelar la respuesta, el personaje se detiene junto al edificio de destino para que «a tu izquierda/derecha» coincida con el dibujo.

## Niveles

| Nivel | Qué practicas | Ejemplo |
|---|---|---|
| Nivel 1 (第一級) | 直走、左轉、右轉、左手邊／右手邊 | 先直走，再右轉，再直走。銀行就在你的左手邊。 |
| Nivel 2 (第二級) | 第一／第二／第三個路口、下一個路口、過馬路 | 直走到第二個路口，左轉，再直走到下一個路口。 |
| Nivel 3 (第三級) | 對面、旁邊, y usar los edificios como referencia | 一直走，右手邊是銀行，過了銀行就左轉。 |
| Nivel 4 (第四級) | Indicaciones largas con todo lo anterior | 直走到第一個路口，左轉，再一直走，右手邊是公園，過了公園就右轉，再直走到第二個路口。 |
| Nivel 5 (第五級) | Barrio real sin cuadrícula: calles en diagonal y curvas, 圓環（第一～四個出口）、Y字路口（靠左／靠右）, y todo lo anterior | 直走到圓環，從第二個出口出去，左轉，最後直走。 |

Notas de vocabulario:
- **直走** = avanzar hasta justo antes de la siguiente esquina (2/3 de la cuadra); girar entra en la esquina.
- Las esquinas se cuentan desde donde estás parado: para la 第N個路口 pulsa 直走 N veces y luego gira.
- **過馬路** = cruzar la calle siguiendo recto; se pulsa el botón de cruzar y luego se avanza.

## Ayudas y ajustes

Todos los ajustes están en el icono ⚙ (arriba a la derecha, en la pantalla de inicio y en el juego); ❓ explica cómo se juega.
Se guardan en la clave compartida `hanziGames.settings` (la misma en todos los juegos de la familia): `{v:1, script, lang, phon, rate}`. Si cambias algo aquí, los otros juegos lo ven (y al revés).

- Caracteres: **繁體** o **简体** (por defecto, tradicional)
- Idioma: **中文＋Español**, **中文＋English** o **只有中文**. Toda la interfaz (títulos, botones, niveles, resultados, clasificación, ayuda) muestra el chino arriba y el otro idioma debajo en letra pequeña y gris; con «只有中文» solo hay chino y vocabulario sin traducción. No hay un interruptor de traducción aparte.
- Pronunciación: **Pinyin** (por defecto, con lecturas de Taiwán), **注音 zhuyin**, **ambos** o **ninguna**
- Velocidad de la voz: lenta (0.45), normal (0.65) o rápida (0.85); siempre voz `zh-TW`
- **Texto desde el inicio** (apagado por defecto): por defecto cada pregunta empieza solo con 🔊 (el texto está oculto). «👁 Ver texto» muestra el chino; el segundo toque muestra la lectura (pinyin/zhuyin) y la traducción. Al responder se muestra todo. Si lo enciendes, todo se ve desde el principio.
- **Por partes**: la indicación se escucha en trozos cortos con «Parte siguiente»
- 📖 **Vocabulario** (botón sobre el mapa): se abre como una hoja desde abajo con las direcciones, las palabras útiles (先、然後、再、最後…) y los lugares del mapa; se cierra con ✕
- Fotos opcionales: si pones `photos/<clave>.jpg` (p. ej. `bank.jpg`) se muestra al terminar cada pregunta

El nombre del jugador, «Texto desde el inicio» (`showAll`) y «Por partes» y la clasificación local se guardan solo en este juego (`askdir_settings`, `askdir_lb`). Los ajustes antiguos de `askdir_settings` se pasan a la clave compartida la primera vez; el antiguo `showText` ya no se usa.

Se puede abrir con parámetros para saltarse la pantalla de inicio, por ejemplo:
`index.html?name=Ana&script=trad&lang=es` (`script`: `trad`/`tw` o `simp`/`cn`; `lang`: `es`, `en` o `zh`).

## Mapas

El mapa no se elige: en los niveles 1–4 cada ronda mezcla al azar los 6 mapas básicos, y el nivel 5 siempre usa el barrio real. Seis mapas sencillos: **便利商店街** (calle comercial), **車站前** (frente a la estación), **夜市** (mercado nocturno), **校園附近** (cerca de la escuela), **醫院附近** (cerca del hospital) y **捷運站出口** (salida del metro), con 31 lugares en total (el barrio real del nivel 5 añade otros 21).
El nivel 5 usa un mapa aparte, **真實街區** (barrio real), que ya no es una cuadrícula: una rotonda con cinco calles de ángulos distintos, una avenida en diagonal, una calle curva y una bifurcación en Y con isla verde. Es una red de calles (`tools/graph_map.py`, motor en `tools/graph_engine.py`): cada giro se decide por el ángulo (más de 20° a un lado = izquierda/derecha; casi recto = sigue recto). En la rotonda se circula en sentido contrario a las agujas del reloj; la primera salida es la primera calle después de por donde entraste. **靠左／靠右** = pulsar girar y luego recto. En el mapa grande, el botón 🔍/🗺 alterna entre seguir al personaje y ver el mapa completo.

Cinco de los mapas básicos tienen calles cerradas (plazas peatonales) y callejones sin salida, así que no todo es una cuadrícula perfecta. Las calles cerradas se definen en `closed` dentro de `MAPS` en `tools/gen_questions.py`. **直走** avanza 2/3 de la cuadra, hasta justo antes de la siguiente parada (una intersección, una curva o el final de la calle); los tramos rectos sin cruce se pasan de largo.

---

## 繁體中文簡介

這是一個練習「問路、指路」的小遊戲，給說西班牙語的華語學習者使用。

- 聽一段指路的話，用「直走、左轉、右轉、過馬路」按鈕讓小人走，走到目的地按「我到了」。
- 文字一開始是藏起來的：先用聽的，聽不懂再按「看文字」（只出現中文），還不懂再按「看讀音和翻譯」；答完題會全部顯示。設定裡的「一開始就顯示文字」可以改成一開始就全部顯示。
- 其他功能：分段聽、真正的「過馬路」按鈕、6 張地圖、可放自己的街景照片；📖 小字典從畫面下方跳出來，不會被版權文字蓋住。
- 共 5 個關卡：方向詞 → 路口與過馬路 → 位置詞（對面、旁邊）→ 綜合挑戰 → 第五級「真實街區」（不是方格的街道：圓環、Y字路口、斜路與彎路）。
- 設定和其他遊戲共用（localStorage 的 `hanziGames.settings`）：繁體／簡體；語言選項是「中文＋Español」、「中文＋English」、「只有中文」，介面一律中文在上、外語小灰字在下（只有中文就沒有外語）；所有設定集中在右上角 ⚙，玩法說明在 ❓；讀音可選拼音（台灣讀音，預設）、注音、拼音＋注音或不顯示；語音速度慢 0.45／中 0.65／快 0.85。
- 只有語言不是「中文」時才會顯示翻譯，沒有另外的翻譯開關。
- 網址參數：`?name=名字&script=trad|simp（或 tw|cn）&lang=es|en|zh`。
- 每一題的指路句、拼音、翻譯、路線和答案都由同一份資料產生，不會互相對不上。

## Para quien mantiene el proyecto

El juego se entrega como un único archivo, `index.html`, sin dependencias, pero **se genera**: edita `tools/template.html` (incluye el `<head>` con el icono y las etiquetas og) y vuelve a construir con `build.py`; no edites `index.html` a mano. Funciona directamente en GitHub Pages
(Settings → Pages → Deploy from a branch → `main` / root).

### Vista previa al compartir el enlace (2026-10-28)

Al pegar la URL en LINE o WhatsApp se muestra el nombre «問路小達人 · Pregunta el camino» y una miniatura. La miniatura es `og.jpg` (1200x630, en la raíz); el nombre y la descripción están en `og:title` y `og:description` dentro del `<head>` de `tools/template.html` (desde 2026-11-05; antes solo estaban en `index.html` y una reconstrucción los habría borrado).

### Clasificación (Firebase)

La clasificación en línea ya está conectada al proyecto `memorma-24dab` (compartido con Memorama y Ordena el Armario), con inicio de sesión anónimo; la configuración está en la constante `FIREBASE_CONFIG` al inicio del `<script>` de `index.html`. Si no se puede conectar, la clasificación se guarda solo en el dispositivo.
Se usan las colecciones `askDirections_L1` … `askDirections_L5` (la L5 está permitida en la copia maestra de las reglas desde 2026-10-29; hay que pegarla en Firebase; hasta entonces la clasificación del nivel 5 se queda en el dispositivo) (un documento por dispositivo y nivel, solo se
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

## 手機瀏覽器備註：捲動後回不到頂端（2026-10-24）
iPhone 版 Chrome 上，頁面可以捲動時，往下捲之後有時回不到最上面（Safari 正常）。
處理方式（已套用在本遊戲）：
- `<meta name="viewport">` 設 `maximum-scale=1`，不使用 `viewport-fit=cover`。
- `<html>` 加 `html{color-scheme:light}`。

兩項一起改後，手機 Chrome 測試恢復正常；尚未分開測是哪一項有效。新增頁面請照這個寫。
