# 🤖 Morrowind AI OpenMW - иммерсивный ИИ мод!

**Иммерсивный Морровинд** мод, который добавляет **искусственный интеллект** в The Elder Scrolls III: Morrowind на движке **OpenMW**.
**🎮 Погружайся в мир Морровинда с ИИ спутниками!**

## ✨ Возможности

- 🎤 **Голосовой ввод** через VOSK (говорите в микрофон)
- 🤖 **ИИ диалоги** через Google Gemini API
- 📜 **Умные НПС** с памятью и характером
- 🗣️ **Поддержка русского языка** (лор Морровинда)
- 🌍 **Совместимость** с Project Tamriel модами
- 🗣 **ElevenLabs** для синтеза речи голосами персонажей (опционально)
- 🎮 Полная интеграция с OpenMW через Lua скрипты
- 🌐 HTTP API для внешних приложений

## 📋 Требования

- **OpenMW с полной поддержкой API** (обязательно!)
- **Python 3.12+**
- **Google Gemini API ключ** (бесплатно на ai.google.dev)
- **Микрофон** для голосового ввода



## 🚀 Установка

## Шаг 1: Подготовка сервера

1. **Клонируй репозиторий:**
git clone https://github.com/ButCheR-PRO/morrowind_ai_openmw.git
cd morrowind_ai_openmw

2. **Или [скачай](https://github.com/ButCheR-PRO/morrowind_ai_openmw/) репозиторий вручную, нажав залёную кнопку "Code" - "Download ZIP"**

3. Скачай и установи [Python 3.12](https://www.python.org/downloads/release/python-31210/) добавив переменную PATH


4. **Запусти автоматическую установку INSTALL.bat:**
Скрипт автоматически:
Создаст виртуальное окружение Python
Установит все зависимости
Скачает VOSK модель для русского языка
Настроит базовую конфигурацию


5. **Получи Gemini API ключ:**
   - Иди на https://ai.google.dev/
   - Создай новый проект
   - Получи API ключ (бесплатно до 15 запросов/мин)
   - Открой config.yml
   - Замени ВАШ_GEMINI_API_KEY на свой ключ

6. **Скачай Speech to text движок** [vosk-model-small-ru-0.22](https://alphacephei.com/vosk/models ) и распакуй в папку с модом


7. **Настрой пути в config.yml:**
### Измени путь к Data Files твоего Morrowind
morrowind_data_files_dir: "C:/Games/Morrowind/Data Files"

8. **Добавь в openmw.cfg:**
Открой свой openmw.cfg (обычно в Documents\My Games\OpenMW\) и добавь:
### Путь к AI скриптам
data="путь_к_серверу/morrowind_ai_openmw/src/Data Files"

### И в конце файла добавь загрузку AI мода
content=morrowind_ai.omwscripts



## Шаг 2: Запуск системы:

1. **Запусти TEST.bat:**
2. **Запусти сервер START_ALL.bat:**
3. **Запустится OpenMW. Загрузи любой сейв или создай нового персонажа**

## 🎯 Шаг 3: Использование

1. **Подойди к любому НПС и начни диалог**
2. **Говори в микрофон** - НПС ответит через ИИ!
3. **ИИ генерирует ответ** → Видишь умную реплику в игре

### Примеры диалогов
Игрок: "Привет! Как дела в Балморе?"
НПС: "Приветствую, путник. В Балморе дела идут своим чередом.
Гильдия Бойцов набирает новобранцев, а в Доме Редоран
обсуждают торговые пути с материком."

Игрок: "Где найти алхимические ингредиенты?"
НПС: "Советую посетить Аджиру-Накал - у неё лучший выбор трав
и грибов во всём Вварденфелле. Но будь осторожен с
контрабандистами в пещерах!"


## 🛠️ Настройка

### Персонализация НПС
Отредактируй `scenes/default.yml` для изменения поведения:

system_prompt: |
Ты торговец оружием в Балморе.
Говори грубо, с юмором.
Предлагай товары игроку.

personality_traits:

gruff_trader

morrowind_native

business_focused


### Голосовые настройки


speech_to_text:
system:
vosk:
energy_threshold: 300 # Чувствительность микрофона
pause_threshold: 1.0 # Пауза между фразами


## 🔧 Решение проблем

### Сервер не запускается
- Проверь Python 3.12: `python --version`
- Проверь Gemini API ключ в config.yml
- Запусти: `TEST.bat`

### Микрофон не работает
- Запусти: `TEST.bat`
- Измени `device_index` в config.yml


### OpenMW не подключается
- Убедись что версия OpenMW актуальная, с полной поддержкой диалогового API, Input API, Game State API
- Проверь что `morrowind_ai.omwscripts` добавлен в openmw.cfg
- Проверь что скрипты скопированы в Data Files/scripts/ или прописаны в openmw.cfg

### НПС не отвечают
- Проверь что сервер запущен
- Убедись что начат диалог с НПС
- Говори чётко в микрофон (на русском языке)

## 📊 Технические детали

### Архитектура

Игрок говорит → VOSK (STT) → Gemini AI → OpenMW → НПС отвечает


### Использованные технологии
- **OpenMW Lua API** - интеграция с игрой
- **VOSK** - распознавание русской речи (оффлайн)
- **Google Gemini** - генерация ИИ ответов
- **TCP/WebSocket** - связь между компонентами


## 👏 Благодарности

- **Dmitrii Zganiaiko** - За мод "Иммерсивный Морровинд AI" для классического движка и YouTube канал @roleplaydlyadushi
- **M[FR] Team** - в частности aL, за прекрасный репак Morrowind FullRest
- **OpenMW Team** - за потрясающий движок
- **Google** - за бесплатный Gemini API
- **Project Tamriel** - за расширенный мир

## 🔗 Полезные ссылки

- [M[FR] Repack](https://www.fullrest.ru/)
- [OpenMW 0.49.0](https://github.com/openmw/openmw/releases)
- [Google AI Studio](https://ai.google.dev/)
- [VOSK Models](https://alphacephei.com/vosk/models)
- [La2ButCheR](http://La2ButCheR.com)
- [Наш Discord](https://discord.gg/KCnhtJu)

## Разработчик: [ButCheR](https://vk.com/la2butcher) ©
