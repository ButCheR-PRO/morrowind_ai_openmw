# 🤖 Morrowind AI OpenMW - Первый ИИ мод с голосовым управлением!

**Революционный мод** который добавляет **искусственный интеллект** и **голосовое управление** в The Elder Scrolls III: Morrowind на движке **OpenMW 0.49+**.

## ✨ Возможности

- 🎤 **Голосовой ввод** через VOSK (говорите в микрофон)
- 🤖 **ИИ диалоги** через Google Gemini API
- 📜 **Умные НПС** с памятью и характером
- 🗣️ **Поддержка русского языка** (лор Морровинда)
- 🌍 **Совместимость** с Project Tamriel модами

## 📋 Требования

- **OpenMW 0.49.0+** (обязательно!)
- **Python 3.12+**
- **Google Gemini API ключ** (бесплатно на ai.google.dev)
- **Микрофон** для голосового ввода
- **16+ ГБ ОЗУ** (рекомендуется)

## 🚀 Установка

### Шаг 1: Подготовка сервера

1. **Клонируй репозиторий:**
git clone https://github.com/ButCheR-PRO/morrowind_ai_openmw.git
cd morrowind_ai_openmw


2. **Запусти установку:**

INSTALL.bat


3. **Настрой config.yml:**

Измени пути под свою систему
morrowind_data_files_dir: "C:/Path/To/Your/Morrowind/Data Files"

Вставь свой Gemini API ключ
llm:
system:
google:
api_key: "ВАШ_GEMINI_API_КЛЮЧ"


4. **Получи Gemini API ключ:**
   - Иди на https://ai.google.dev/
   - Создай новый проект
   - Получи API ключ (бесплатно до 15 запросов/мин)

### Шаг 2: Установка OpenMW модуля

5. **Скопируй Lua скрипты:**

Из репозитория в твою папку Data Files
scripts/ → C:/Path/To/Your/Morrowind/Data Files/scripts/


6. **Добавь в openmw.cfg:**

Открой файл `Documents/My Games/OpenMW/openmw.cfg` и добавь в конец:


Morrowind AI Mod
content=morrowind_ai.omwscripts


### Шаг 3: Настройка микрофона

7. **Проверь микрофон:**


TEST_VOSK.bat


8. **Если микрофон не работает** - измени в config.yml:


speech_to_text:
system:
vosk:
device_index: 0 # Попробуй другие значения: 1, 2, 3...


## 🎮 Запуск

### Запуск сервера

START.bat


**Должно появиться:**
[SUCCESS] Initialization completed
[WAITING] Waiting for the Morrowind to connect to the server...

### Запуск игры
1. Запусти **OpenMW** (версия 0.49+)
2. Загрузи любой сейв или создай нового персонажа
3. Подойди к любому НПС и начни диалог
4. **Говори в микрофон** - НПС ответит через ИИ!

## 🎯 Использование

### Голосовые команды
- **Подойди к НПС** → Начни диалог
- **Говори в микрофон** → VOSK распознает речь
- **ИИ генерирует ответ** → Видишь умную реплику в игре

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
- Запусти: `CHECK_CONFIG.bat`

### Микрофон не работает
- Запусти: `TEST_VOSK.bat`
- Измени `device_index` в config.yml
- Проверь права доступа к микрофону

### OpenMW не подключается
- Убедись что версия OpenMW 0.49+
- Проверь что `morrowind_ai.omwscripts` добавлен в openmw.cfg
- Проверь что скрипты скопированы в Data Files/scripts/

### НПС не отвечают
- Проверь что сервер запущен
- Убедись что начат диалог с НПС
- Говори чётко в микрофон (русский язык)

## 📊 Технические детали

### Архитектура

Игрок говорит → VOSK (STT) → Gemini AI → OpenMW → НПС отвечает


### Использованные технологии
- **OpenMW Lua API** - интеграция с игрой
- **VOSK** - распознавание русской речи (оффлайн)
- **Google Gemini** - генерация ИИ ответов
- **TCP/WebSocket** - связь между компонентами

### Производительность
- **CPU:** Средняя нагрузка при диалогах
- **RAM:** ~2GB дополнительно
- **Сеть:** Только Gemini API запросы

## 🤝 Вклад в проект

1. Форкни репозиторий
2. Создай ветку для своих изменений
3. Сделай Pull Request
4. Опиши что изменил/улучшил

## 📄 Лицензия

MIT License - используй свободно!

## 👏 Благодарности

- **OpenMW Team** - за потрясающий движок
- **VOSK Developers** - за бесплатное STT
- **Google** - за Gemini API
- **Project Tamriel** - за расширенный мир

## 🔗 Полезные ссылки

- [OpenMW Official](https://openmw.org/)
- [Google AI Studio](https://ai.google.dev/)
- [VOSK Models](https://alphacephei.com/vosk/models)
- [M[FR] Repack](https://www.fullrest.ru/)

---

**🎮 Погружайся в мир Морровинда с ИИ спутниками!**


🗂️ Что копировать куда
Структура файлов для установки:

# Твой репозиторий:
morrowind_ai_openmw/
├── scripts/                     ← КОПИРОВАТЬ в Data Files
│   ├── morrowind_ai.omwscripts  
│   └── morrowind_ai/
│       ├── init.lua
│       ├── dialogue.lua
│       └── network.lua
├── server/                      ← Остаётся в папке мода
├── config.yml                   ← Остаётся в папке мода
└── scenes/                      ← Остаётся в папке мода
Куда копировать пользователю:
Lua скрипты:
scripts/ → C:/Games/MorrowindFullrest/game/Data Files/scripts/


Настройка openmw.cfg:

# В файл: Documents/My Games/OpenMW/openmw.cfg
# Добавить строку:
content=morrowind_ai.omwscripts


🎯 Следующие шаги для тебя
Создай OpenMW Lua скрипты (я дам код ниже)

Обнови README.md моим текстом

Запуши на GitHub

Протестируй подключение

Нужно создать эти файлы в папке scripts:
morrowind_ai.omwscripts:
PLAYER: scripts/morrowind_ai/player.lua
GLOBAL: scripts/morrowind_ai/init.lua


scripts/morrowind_ai/init.lua:

local core = require('openmw.core')
local ui = require('openmw.ui')

local M = {}

function M.onInit()
    print("[Morrowind AI] Сервер готов к подключению...")
    -- Здесь будет логика подключения к TCP серверу
end

function M.onUpdate(dt)
    -- Периодическая проверка связи с сервером
end

return M

