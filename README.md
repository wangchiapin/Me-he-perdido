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
3. Mueve al personaje con los botones: **直走** (recto), **左轉** (izquierda), **右轉** (derecha) y, desde el nivel 2, **過馬路** (cruzar la calle; solo se usa tras «過了…就過馬路»).
4. Cuando creas que llegaste, pulsa **¡Llegué!**
5. Si te equivocas, el juego te muestra tu ruta y la ruta correcta, y puedes ver cómo se camina.

Cada ronda tiene 8 preguntas y cada acierto vale 10 puntos. Hay clasificación por nivel.

**Importante:** izquierda y derecha dependen de hacia dónde mira el personaje (una persona o un animal visto desde arriba, distinto en cada pregunta), no de la pantalla. Ahí está la práctica. Al revelar la respuesta, el personaje se detiene junto al edificio de destino para que «a tu izquierda/derecha» coincida con el dibujo.

## Niveles

| Nivel | Qué practicas | Ejemplo |
|---|---|---|
| Nivel 1 (第一級) | 直走、左轉、右轉、左手邊／右手邊, 一直走到底, 對面、前面、後面 (mapas de cuadrícula) | 先右轉，然後再一直走到底。麵包店就在你的左手邊，對面是藥局。 |
| Nivel 2 (第二級) | Contar 第一／第二／第三個路口 y 下一個路口, **semáforos al azar** (第N個紅綠燈; solo se cuentan las esquinas con semáforo), edificios como referencia (過了X就轉, 看到X就轉, 經過X，繼續直走) y 過了…就過馬路 (mapas de cuadrícula) | 經過便利商店，繼續直走到第二個紅綠燈，右轉。再直走。書店就在你的右手邊。 |
| Nivel 3 (第三級) | Barrio real sin cuadrícula (calles en diagonal y curvas, 圓環, Y字路口, paradas frente a las tiendas) **y** mapa grande e irregular con la vista siguiendo al personaje (semáforos al azar, tiendas repetidas: 第N個紅綠燈, 第N個路口, 第N間＋tienda) | 直走到第二個紅綠燈，右轉，再直走到第二間便利商店前面。 |
| Nivel 4 (第四級) | **Todo mezclado**: 48 preguntas de mapas de cuadrícula (todo lo de los niveles 1 y 2) y 48 de los dos mapas de calles (nivel 3) | 直走到圓環，從第二個出口出去，左轉，最後直走。 |

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

El mapa no se elige: en los niveles 1 y 2 cada ronda mezcla al azar los 6 mapas básicos, el nivel 3 usa solo el barrio real y el mapa grande, y el nivel 4 mezcla todos. Las 8 preguntas de cada ronda se juegan **de fácil a difícil** (cada pregunta tiene un número `diff`). Además, en los 6 mapas básicos la posición de los edificios cambia en cada pregunta (se mezclan al generar `questions.json`; el edificio «estrella» de cada mapa —estación, templo, escuela, hospital, MRT— se queda en su sitio, y en la calle comercial se mezclan los nueve). Cada pregunta guarda su propia distribución en `blocks`. Seis mapas sencillos: **便利商店街** (calle comercial), **車站前** (frente a la estación), **夜市** (mercado nocturno), **校園附近** (cerca de la escuela), **醫院附近** (cerca del hospital) y **捷運站出口** (salida del metro), con 31 lugares en total (el barrio real del nivel 3 añade otros 21).
El nivel 3 usa dos mapas aparte; el primero es **真實街區** (barrio real), que ya no es una cuadrícula: una rotonda con cinco calles de ángulos distintos, una avenida en diagonal, una calle curva y una bifurcación en Y con isla verde. Es una red de calles (`tools/graph_map.py`, motor en `tools/graph_engine.py`): cada giro se decide por el ángulo (más de 20° a un lado = izquierda/derecha; casi recto = sigue recto). En la rotonda se circula en sentido contrario a las agujas del reloj; la primera salida es la primera calle después de por donde entraste. **靠左／靠右** = pulsar girar y luego recto. En el mapa grande, el botón 🔍/🗺 alterna entre seguir al personaje y ver el mapa completo.

Cinco de los mapas básicos tienen calles cerradas (plazas peatonales) y callejones sin salida, así que no todo es una cuadrícula perfecta. Las calles cerradas se definen en `closed` dentro de `MAPS` en `tools/gen_questions.py`. **直走** avanza 2/3 de la cuadra, hasta justo antes de la siguiente parada (una intersección, una curva o el final de la calle); los tramos rectos sin cruce se pasan de largo.

---

## 繁體中文簡介

這是一個練習「問路、指路」的小遊戲，給說西班牙語的華語學習者使用。

- 聽一段指路的話，用「直走、左轉、右轉、過馬路」按鈕讓小人走，走到目的地按「我到了」。
- 文字一開始是藏起來的：先用聽的，聽不懂再按「看文字」（只出現中文），還不懂再按「看讀音和翻譯」；答完題會全部顯示。設定裡的「一開始就顯示文字」可以改成一開始就全部顯示。
- 其他功能：分段聽、真正的「過馬路」按鈕、6 張地圖、可放自己的街景照片；📖 小字典從畫面下方跳出來，不會被版權文字蓋住。
- 地圖不用選：第 1、2 級每一輪隨機混用 6 張地圖（第 3 級用真實街區和大街區，第 4 級全部混合），建築位置每一題都不一樣（車站、廟、學校、醫院、捷運站這些主角固定在原位，其他亂排；便利商店街全部亂排）。
- 共 4 個關卡：第一級（直走、左右轉、一直走到底、對面／前面／後面）→ 第二級（數路口與紅綠燈、用建築物當參考、過馬路）→ 第三級（真實街區＋大街區）→ 第四級（全部混合）。每一輪 8 題由易到難排。第二級起新增說法「經過銀行，繼續直走」「看到銀行就右轉」；只有一間店／一個紅綠燈時不說「第一間」「第一個」，經過兩個以上才說「第N」。
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
Se usan las colecciones `askDirections_L1` … `askDirections_L4` (desde 2026-11-06 hay 4 niveles; los nombres L1–L4 ya estaban permitidos en las reglas, así que no hay que cambiar nada; las puntuaciones antiguas de los niveles 1–4 se mezclan con los nuevos) (un documento por dispositivo y nivel, solo se
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


## Nivel 3 (mapas de calles): paradas frente a las tiendas / 第三級：店前停下
- En las calles largas del 真實街區 hay una segunda tienda; cada tienda es una **parada**: 直走 avanza solo hasta la siguiente parada (tienda, esquina o rotonda). En una parada no se puede girar ni cruzar. En el 大街區 todas las calles con tienda tienen paradas.
- Frases: 「直走到咖啡店前面」. Con 「直走到第N個路口」「直走到圓環」 se pasan las tiendas sin parar en ellas en la frase, pero hay que pulsar 直走 una vez por parada. Por eso 「經過銀行，繼續直走」 también obliga a pulsar 直走 otra vez delante del banco.
- 繁中：較長的路多了第二間店，「直走」一次只走到下一間店／路口／圓環；店前不能轉彎或過馬路。

## Nivel 3 (mapa grande) y semáforos / 第三級大街區與紅綠燈
- El mapa **大街區** (`BIG` en `tools/graph_map.py`, mismo motor que el barrio real) es grande e irregular y la vista sigue al personaje con una ventana del mismo tamaño que en el barrio real; los edificios tienen el mismo tamaño que siempre. Solo algunas esquinas (`_LIGHTS`) tienen semáforo. Hay tiendas del mismo tipo repetidas (los nombres con `_2`: `conv_2` = la 2.ª tienda de conveniencia; el juego quita el sufijo al dibujar).
- Frases: 「直走到紅綠燈」 / 「直走到第二個紅綠燈」 (solo cuenta las esquinas con semáforo; el primero no lleva número), 「直走到圖書館前面」 / 「直走到第二間便利商店前面」 (la primera tienda de su tipo en el camino no lleva número). 「第N個路口」 sigue valiendo y se puede mezclar.
- Nivel 2: los 6 mapas pequeños también tienen semáforos, solo en algunas esquinas con 3 o más calles, distintas en cada pregunta (`lights` en `questions.json`; se dibujan solo si la pregunta lo trae).
- 「經過X，繼續直走到…」: X está junto al primer tramo (antes de la primera esquina que se cuenta). 「看到X就右轉」: gira en la primera esquina después de X (igual que 「過了X就右轉」, sin decir el lado).
- `questions.json` guarda en cada pregunta un `plan` (casi todas) que `verify_questions.py` vuelve a recorrer por su cuenta (semáforos, esquinas, k-ésima tienda, 經過 / 看到 / 過了, 到底) en los mapas de cuadrícula y en los de calles.
- 繁中：第三級的大街區用一張大又不規則的地圖，畫面會跟著人物移動。只有部分路口有紅綠燈（隨機），第二級的小地圖也一樣。同一種店會出現兩間以上，數到第二個才說「第二個紅綠燈」「第二間便利商店」；第一個不用說「第一」。店前不能轉彎，所以數完店還要再直走到路口才能轉。
