import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8669298087:AAH1Oyl-M47xwLzuUvaq2lbSNkIsM5PyLQQ"

logging.basicConfig(level=logging.INFO)

logging.basicConfig(level=logging.INFO)

TESTS = {
    1: [
        {
            "question": "TRUE or FALSE?\nCharles Dickens was famous for writing musicals.",
            "translation": "\U0001f1f7\U0001f1fa Верно или нет?\nЧарльз Диккенс был известен написанием мюзиклов.",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": (
                "\u274c *Неверно! / False!*\n\n"
                "📖 Charles Dickens wrote a number of famous novels, including Oliver Twist and Great Expectations.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Чарльз Диккенс написал множество известных романов, включая «Оливер Твист» и «Большие надежды»."
            ),
        },
        {
            "question": "TRUE or FALSE?\nA General Election is held at least every five years.",
            "translation": "\U0001f1f7\U0001f1fa Верно или нет?\nВсеобщие выборы проводятся не реже одного раза в пять лет.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно! / True!*\n\n"
                "📖 A General Election is held at least every five years.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Всеобщие выборы проводятся не реже одного раза в пять лет."
            ),
        },
        {
            "question": "TRUE or FALSE?\nIn the UK you are expected to respect the rights of others to have their own opinions.",
            "translation": "\U0001f1f7\U0001f1fa Верно или нет?\nВ Великобритании вы обязаны уважать право других иметь собственное мнение.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно! / True!*\n\n"
                "📖 There are responsibilities and freedoms which are shared by all those living in the UK.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Все живущие в Великобритании разделяют общие обязанности и свободы."
            ),
        },
        {
            "question": "TRUE or FALSE?\nOn the 1st of April, people in the UK play jokes on each other until midday.",
            "translation": "\U0001f1f7\U0001f1fa Верно или нет?\n1 апреля люди в Великобритании разыгрывают друг друга до полудня.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно! / True!*\n\n"
                "📖 April Fool\'s Day is the 1st of April. People play jokes on each other until midday.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* День дурака — 1 апреля. Люди разыгрывают друг друга до полудня."
            ),
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "\U0001f1f7\U0001f1fa Какое из следующих утверждений верно?",
            "options": [
                "A — Shakespeare wrote \'To be or not to be\'",
                "B — Shakespeare wrote \'We shall fight on the beaches\'"
            ],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно — A!*\n\n"
                "📖 William Shakespeare wrote \'To be or not to be\' in the play Hamlet.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Шекспир написал «Быть или не быть» в пьесе «Гамлет»."
            ),
        },
        {
            "question": "How can you reduce your carbon footprint?",
            "translation": "\U0001f1f7\U0001f1fa Как можно уменьшить свой углеродный след?",
            "options": [
                "A — Shop locally for products",
                "B — Buy duty-free products when abroad",
                "C — Do all your shopping online",
                "D — Drive to the supermarket"
            ],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно — A!*\n\n"
                "📖 You can reduce your carbon footprint by shopping locally.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Покупки у местных производителей снижают выбросы CO2."
            ),
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "\U0001f1f7\U0001f1fa Какое из следующих утверждений верно?",
            "options": [
                "A — The civil service largely consists of political appointees",
                "B — The civil service is politically neutral"
            ],
            "answer": 1,
            "explanation": (
                "\u2705 *Верно — B!*\n\n"
                "📖 Civil servants are politically neutral and do not support any political party.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Государственные служащие политически нейтральны."
            ),
        },
        {
            "question": "Which TWO are Protestant Christian groups in the UK?",
            "translation": "\U0001f1f7\U0001f1fa Какие ДВЕ группы являются протестантскими христианскими группами в UK?",
            "options": [
                "A — Methodists and Roman Catholics",
                "B — Baptists and Methodists",
                "C — Baptists and Hindus",
                "D — Roman Catholics and Sikhs"
            ],
            "answer": 1,
            "explanation": (
                "\u2705 *Верно — B!*\n\n"
                "📖 Baptists and Methodists are Protestant Christian groups in the UK.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Баптисты и методисты — протестантские группы."
            ),
        },
        {
            "question": "What is the role of a jury at a court trial?",
            "translation": "\U0001f1f7\U0001f1fa Какова роль присяжных на судебном процессе?",
            "options": [
                "A — To decide whether evidence should be allowed to be heard",
                "B — To decide the sentence that the accused should be given",
                "C — To decide who the judge should be",
                "D — To decide a verdict based on what they have heard"
            ],
            "answer": 3,
            "explanation": (
                "\u2705 *Верно — D!*\n\n"
                "📖 The jury decides a verdict of \'guilty\' or \'not guilty\'. The judge decides the sentence.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Присяжные выносят вердикт, судья — приговор."
            ),
        },
        {
            "question": "Which form of comedy became famous in the 19th century?",
            "translation": "\U0001f1f7\U0001f1fa Какая форма комедии стала знаменитой в 19 веке?",
            "options": [
                "A — Sitcoms",
                "B — Satirical magazines",
                "C — Progressive comedy",
                "D — Court jesters"
            ],
            "answer": 1,
            "explanation": (
                "\u2705 *Верно — B!*\n\n"
                "📖 In the 19th century, satirical magazines became popular. The most famous was Punch, first published in 1841.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* В 19 веке сатирические журналы стали популярными. Самый известный — Punch (1841)."
            ),
        },
        {
            "question": "During which period did John Barbour and other poets begin to write poetry in the Scots language?",
            "translation": "\U0001f1f7\U0001f1fa В какой период Джон Барбур и другие поэты начали писать стихи на шотландском языке?",
            "options": [
                "A — The 19th century",
                "B — The 20th century",
                "C — The Middle Ages",
                "D — The Bronze Age"
            ],
            "answer": 2,
            "explanation": (
                "\u2705 *Верно — C!*\n\n"
                "📖 In the Middle Ages, poets began to write in the Scots language. John Barbour wrote The Bruce about the Battle of Bannockburn.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* В Средние века поэты начали писать на шотландском языке."
            ),
        },
        {
            "question": "What are Beowulf, The Tyger and She Walks in Beauty?",
            "translation": "\U0001f1f7\U0001f1fa Что такое «Беовульф», «Тигр» и «Она идёт во всей красе»?",
            "options": [
                "A — Plays",
                "B — Films",
                "C — Poems",
                "D — Novels"
            ],
            "answer": 2,
            "explanation": (
                "\u2705 *Верно — C!*\n\n"
                "📖 Beowulf is an Anglo-Saxon poem. The Tyger was written by William Blake and She Walks in Beauty by Lord Byron.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* «Беовульф», «Тигр» и «Она идёт во всей красе» — поэмы/стихи."
            ),
        },
        {
            "question": "What is a jury made up of?",
            "translation": "\U0001f1f7\U0001f1fa Из кого состоят присяжные?",
            "options": [
                "A — People working in high-powered jobs",
                "B — People randomly chosen from the electoral register",
                "C — People who have submitted an application form",
                "D — People who are members of political parties"
            ],
            "answer": 1,
            "explanation": (
                "\u2705 *Верно — B!*\n\n"
                "📖 A jury is made up of members of the public who are randomly chosen from the electoral register.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Присяжные — граждане, случайно выбранные из списка избирателей."
            ),
        },
        {
            "question": "Which TWO fought in wars against Napoleon?",
            "translation": "\U0001f1f7\U0001f1fa Кто из перечисленных ДВУХ воевал против Наполеона?",
            "options": [
                "A — Winston Churchill and the Duke of Wellington",
                "B — Margaret Thatcher and the Duke of Wellington",
                "C — Margaret Thatcher and Admiral Nelson",
                "D — Admiral Nelson and the Duke of Wellington"
            ],
            "answer": 3,
            "explanation": (
                "\u2705 *Верно — D!*\n\n"
                "📖 Admiral Nelson commanded the British fleet at Trafalgar in 1805. The Duke of Wellington defeated Napoleon at Waterloo in 1815.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Нельсон — Трафальгар 1805, Веллингтон — Ватерлоо 1815."
            ),
        },
        {
            "question": "After slavery was abolished in the British Empire, more than 2 million migrants came from which TWO countries?",
            "translation": "\U0001f1f7\U0001f1fa После отмены рабства более 2 миллионов мигрантов приехали из каких ДВУХ стран?",
            "options": [
                "A — India and China",
                "B — Russia and China",
                "C — India and Australia",
                "D — Russia and Australia"
            ],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно — A!*\n\n"
                "📖 After 1833, 2 million Indian and Chinese workers were employed to replace the freed slaves.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* После 1833 года 2 миллиона рабочих из Индии и Китая заменили освобождённых рабов."
            ),
        },
        {
            "question": "Which group of adults is NOT eligible to vote in all UK elections?",
            "translation": "\U0001f1f7\U0001f1fa Какая группа взрослых НЕ имеет права голосовать на всех выборах в UK?",
            "options": [
                "A — Citizens of the USA",
                "B — Adult citizens of the UK",
                "C — Qualifying Commonwealth citizens resident in the UK",
                "D — Citizens of Ireland resident in the UK"
            ],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно — A!*\n\n"
                "📖 Adult citizens of the UK, qualifying Commonwealth citizens and Irish citizens resident in the UK can vote. Citizens of other countries cannot.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Граждане США и других стран не могут голосовать на выборах в UK."
            ),
        },
        {
            "question": "Which statement about Big Ben is correct?",
            "translation": "\U0001f1f7\U0001f1fa Какое утверждение о Биг Бене верно?",
            "options": [
                "A — Big Ben is a mountain in eastern England",
                "B — Big Ben is the nickname for the great bell of the clock at the Houses of Parliament"
            ],
            "answer": 1,
            "explanation": (
                "\u2705 *Верно — B!*\n\n"
                "📖 Big Ben is the nickname for the great bell of the clock at the Houses of Parliament in London.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Биг Бен — прозвище большого колокола часов в здании Парламента."
            ),
        },
        {
            "question": "Bobby Moore is famous for his achievements in which sport?",
            "translation": "\U0001f1f7\U0001f1fa Бобби Мур известен своими достижениями в каком виде спорта?",
            "options": [
                "A — Football",
                "B — Rugby union",
                "C — Horse racing",
                "D — Motor racing"
            ],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно — A!*\n\n"
                "📖 Bobby Moore captained the England football team that won the World Cup in 1966.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Бобби Мур был капитаном сборной Англии, выигравшей Чемпионат мира 1966 года."
            ),
        },
        {
            "question": "TRUE or FALSE?\nIf you are a qualifying Commonwealth citizen resident in the UK, you can vote in all public elections.",
            "translation": "\U0001f1f7\U0001f1fa Верно или нет?\nКвалифицированный гражданин Содружества, проживающий в UK, может голосовать на всех публичных выборах?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно! / True!*\n\n"
                "📖 Qualifying citizens of the Commonwealth who are resident in the UK can vote in all public elections.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Квалифицированные граждане Содружества в UK могут голосовать на всех выборах."
            ),
        },
        {
            "question": "Which TWO of the following were important 20th-century inventors?",
            "translation": "\U0001f1f7\U0001f1fa Кто из перечисленных ДВУХ был важным изобретателем 20 века?",
            "options": [
                "A — Alan Turing and Tim Berners-Lee",
                "B — Tim Berners-Lee and Isambard Kingdom Brunel",
                "C — George Stephenson and Isambard Brunel",
                "D — Alan Turing and George Stephenson"
            ],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно — A!*\n\n"
                "📖 Alan Turing contributed to the development of the modern computer. Tim Berners-Lee invented the World Wide Web.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Тьюринг — основы компьютера, Бернерс-Ли — Всемирная паутина."
            ),
        },
        {
            "question": "Which statement is correct about applying for UK citizenship?",
            "translation": "\U0001f1f7\U0001f1fa Какое утверждение верно относительно заявки на гражданство UK?",
            "options": [
                "A — When you apply you can choose which laws to accept",
                "B — When you apply to become a permanent resident, you agree to accept the responsibilities, values and traditions of the UK"
            ],
            "answer": 1,
            "explanation": (
                "\u2705 *Верно — B!*\n\n"
                "📖 Applying to become a permanent resident or citizen of the UK means agreeing to accept the values and responsibilities.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Подавая заявку, вы соглашаетесь принять ценности и обязанности UK."
            ),
        },
        {
            "question": "Which TWO are plays by William Shakespeare?",
            "translation": "\U0001f1f7\U0001f1fa Какие ДВЕ пьесы написал Уильям Шекспир?",
            "options": [
                "A — A Midsummer Night\'s Dream and Oliver Twist",
                "B — Romeo and Juliet and Oliver Twist",
                "C — A Midsummer Night\'s Dream and Romeo and Juliet",
                "D — Pride and Prejudice and Romeo and Juliet"
            ],
            "answer": 2,
            "explanation": (
                "\u2705 *Верно — C!*\n\n"
                "📖 Among Shakespeare\'s plays are A Midsummer Night\'s Dream and Romeo and Juliet.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* «Сон в летнюю ночь» и «Ромео и Джульетта» — пьесы Шекспира."
            ),
        },
        {
            "question": "Which TWO commemorations are held in November each year?",
            "translation": "\U0001f1f7\U0001f1fa Какие ДВА памятных события отмечаются в ноябре каждый год?",
            "options": [
                "A — Remembrance Day and Bonfire Night",
                "B — Valentine\'s Day and Remembrance Day",
                "C — Valentine\'s Day and Father\'s Day",
                "D — Father\'s Day and Bonfire Night"
            ],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно — A!*\n\n"
                "📖 Bonfire Night is on 5 November. Remembrance Day is on 11 November.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Ночь костров — 5 ноября. День памяти — 11 ноября."
            ),
        },
        {
            "question": "TRUE or FALSE?\nAll young people in the UK are sent a National Insurance number just before their 16th birthday.",
            "translation": "\U0001f1f7\U0001f1fa Верно или нет?\nВсем молодым людям в UK отправляют номер национального страхования незадолго до 16-летия.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "\u2705 *Верно! / True!*\n\n"
                "📖 All young people in the UK are sent a National Insurance number just before their 16th birthday.\n\n"
                "\U0001f1f7\U0001f1fa *Перевод:* Все молодые люди в UK получают номер национального страхования до 16 лет."
            ),
        },
    ],
    2: [
        {
            "question": "TRUE or FALSE?\nThe Civil War between Charles I and Parliament in the mid-17th century led to Oliver Cromwell becoming king of England.",
            "translation": "🇷🇺 Гражданская война между Карлом I и Парламентом привела к тому, что Кромвель стал королём?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Oliver Cromwell became Lord Protector, not king.\n🇷🇺 Кромвель стал лордом-протектором, а не королём.",
        },
        {
            "question": "Which event is remembered on 5 November each year?",
            "translation": "🇷🇺 Какое событие вспоминают 5 ноября?",
            "options": ["A — End of Second World War", "B — The King's birthday", "C — A plan to blow up the Houses of Parliament in 1605", "D — Defeat of the Spanish Armada in 1588"],
            "answer": 2,
            "explanation": "✅ C!\n📖 Bonfire Night — the Gunpowder Plot of 1605.\n🇷🇺 Ночь костров — Пороховой заговор 1605 года.",
        },
        {
            "question": "When is Boxing Day?",
            "translation": "🇷🇺 Когда День подарков?",
            "options": ["A — Day after Easter", "B — Day after Christmas Day", "C — Last Monday in August", "D — First day in May"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Boxing Day is 26 December, the day after Christmas.\n🇷🇺 День подарков — 26 декабря.",
        },
        {
            "question": "Which group of refugees settled in England between 1680 and 1720?",
            "translation": "🇷🇺 Какая группа беженцев осела в Англии между 1680 и 1720?",
            "options": ["A — Welsh", "B — Germans", "C — Bretons", "D — Huguenots"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Huguenots were French Protestants persecuted for their religion.\n🇷🇺 Гугеноты — французские протестанты, бежавшие из-за преследований.",
        },
        {
            "question": "TRUE or FALSE?\n'We shall fight on the beaches' is a famous quote from Queen Elizabeth I about the Spanish Armada.",
            "translation": "🇷🇺 «Мы будем сражаться на пляжах» — цитата Елизаветы I об Испанской Армаде?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 This was said by Winston Churchill in WWII.\n🇷🇺 Это слова Черчилля во Второй мировой войне.",
        },
        {
            "question": "TRUE or FALSE?\nBritain has never been at war with France.",
            "translation": "🇷🇺 Великобритания никогда не воевала с Францией?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Britain fought many wars against France including Agincourt and Waterloo.\n🇷🇺 Британия воевала с Францией много раз.",
        },
        {
            "question": "Which TWO are famous British fashion designers?",
            "translation": "🇷🇺 Какие ДВОЕ — знаменитые британские дизайнеры моды?",
            "options": ["A — Capability Brown and Edwin Lutyens", "B — Mary Quant and Capability Brown", "C — Mary Quant and Vivienne Westwood", "D — Capability Brown and Vivienne Westwood"],
            "answer": 2,
            "explanation": "✅ C!\n📖 Mary Quant and Vivienne Westwood are famous British fashion designers.\n🇷🇺 Мэри Куант и Вивьен Вествуд — знаменитые дизайнеры.",
        },
        {
            "question": "Which TWO services are funded by National Insurance Contributions?",
            "translation": "🇷🇺 Какие ДВЕ услуги финансируются взносами национального страхования?",
            "options": ["A — State retirement pension and NHS", "B — Supermarket home deliveries and NHS", "C — Local taxi services and state pension", "D — State pension and supermarket deliveries"],
            "answer": 0,
            "explanation": "✅ A!\n📖 NI Contributions fund the state pension and the NHS.\n🇷🇺 Взносы НС финансируют государственную пенсию и NHS.",
        },
        {
            "question": "TRUE or FALSE?\nCardiff, Swansea and Newport are cities in England.",
            "translation": "🇷🇺 Кардифф, Суонси и Ньюпорт — города в Англии?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Cardiff, Swansea and Newport are cities in Wales.\n🇷🇺 Эти города находятся в Уэльсе.",
        },
        {
            "question": "Which TWO developments were features of the Industrial Revolution?",
            "translation": "🇷🇺 Какие ДВА достижения характерны для Промышленной революции?",
            "options": ["A — Machinery and steam power", "B — Changes in the law and steam power", "C — Machinery and medical advances", "D — Medical advances and changes in the law"],
            "answer": 0,
            "explanation": "✅ A!\n📖 The Industrial Revolution was driven by machinery and steam power.\n🇷🇺 Промышленная революция — машинерия и паровая энергия.",
        },
        {
            "question": "Who has to pay National Insurance Contributions?",
            "translation": "🇷🇺 Кто обязан платить взносы национального страхования?",
            "options": ["A — Almost everybody in the UK in paid work", "B — Only people who work full-time", "C — Only those aged 50 and below", "D — Only single people with no dependants"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Almost everybody in paid work, including self-employed, must pay NI Contributions.\n🇷🇺 Почти все работающие обязаны платить взносы НС.",
        },
        {
            "question": "TRUE or FALSE?\nA husband who forces his wife to have sex can be charged with rape.",
            "translation": "🇷🇺 Муж, принуждающий жену к сексу, может быть обвинён в изнасиловании?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 Any man who forces a woman, including his wife, to have sex can be charged with rape.\n🇷🇺 Принуждение к сексу является изнасилованием даже в браке.",
        },
        {
            "question": "TRUE or FALSE?\nAll people in the UK are expected to help the police prevent and detect crimes whenever they can.",
            "translation": "🇷🇺 Все люди в UK обязаны помогать полиции предотвращать преступления?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 All people in the UK are expected to help the police prevent and detect crimes.\n🇷🇺 Все граждане UK должны содействовать полиции.",
        },
        {
            "question": "TRUE or FALSE?\nIn 1805, at the Battle of Trafalgar, Admiral Nelson defeated the German fleet.",
            "translation": "🇷🇺 В 1805 году Нельсон разгромил немецкий флот при Трафальгаре?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Nelson defeated the combined French and Spanish fleet at Trafalgar.\n🇷🇺 Нельсон победил французско-испанский флот, не немецкий.",
        },
        {
            "question": "TRUE or FALSE?\nAnybody can be asked to serve on a jury, no matter how old they are.",
            "translation": "🇷🇺 Любой человек может быть призван присяжным, независимо от возраста?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 You must be on the electoral register and aged 18–70 (18–75 in England and Wales).\n🇷🇺 Присяжным может быть только человек 18–70 лет.",
        },
        {
            "question": "TRUE or FALSE?\nThere is no place in British society for extremism or intolerance.",
            "translation": "🇷🇺 В британском обществе нет места экстремизму?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 British society is founded on fundamental values. There is no place for extremism or intolerance.\n🇷🇺 В британском обществе нет места экстремизму.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — By 1400, the preferred language of the royal court was French.", "B — By 1400, the preferred language of the royal court was English."],
            "answer": 1,
            "explanation": "✅ B!\n📖 By 1400 the preferred language of the royal court was English.\n🇷🇺 К 1400 году английский стал языком королевского двора.",
        },
        {
            "question": "Which TWO of these novels are by Charles Dickens?",
            "translation": "🇷🇺 Какие ДВА романа написал Чарльз Диккенс?",
            "options": ["A — Harry Potter and Great Expectations", "B — Great Expectations and Oliver Twist", "C — Harry Potter and Pride and Prejudice", "D — Pride and Prejudice and Oliver Twist"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Charles Dickens wrote Oliver Twist and Great Expectations.\n🇷🇺 Диккенс написал «Оливер Твист» и «Большие надежды».",
        },
        {
            "question": "At which festival are mince pies traditionally eaten?",
            "translation": "🇷🇺 На каком празднике едят mince pies?",
            "options": ["A — Easter", "B — Diwali", "C — Christmas", "D — Vaisakhi"],
            "answer": 2,
            "explanation": "✅ C!\n📖 Mince pies are a traditional Christmas food.\n🇷🇺 Пироги с начинкой — традиционное рождественское угощение.",
        },
        {
            "question": "TRUE or FALSE?\nDuring the 18th century, new ideas about politics, philosophy and science were developed. This period is often called the Enlightenment.",
            "translation": "🇷🇺 В 18 веке развивались новые идеи — это эпоха Просвещения?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 The 18th century period of new ideas is often called the Enlightenment.\n🇷🇺 18 век — эпоха Просвещения.",
        },
        {
            "question": "What is the youngest age at which you can be asked to serve on a jury?",
            "translation": "🇷🇺 Минимальный возраст для службы присяжным?",
            "options": ["A — 22", "B — 18", "C — 16", "D — 30"],
            "answer": 1,
            "explanation": "✅ B!\n📖 You can be asked to serve on a jury from age 18.\n🇷🇺 Минимальный возраст присяжного — 18 лет.",
        },
        {
            "question": "TRUE or FALSE?\nAn example of a civil law case is when you have purchased a faulty item and made a legal complaint.",
            "translation": "🇷🇺 Покупка бракованного товара и жалоба — пример гражданского дела?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 Civil law is used to settle disputes, e.g. purchasing a faulty item.\n🇷🇺 Гражданское право регулирует споры, включая бракованные товары.",
        },
        {
            "question": "Which TWO of the following are famous British artists?",
            "translation": "🇷🇺 Кто из перечисленных ДВОЕ — знаменитые британские художники?",
            "options": ["A — David Hockney and Henry Moore", "B — Sir Edward Elgar and Sir Edward Elgar", "C — David Hockney and Sir Edward Elgar", "D — Sir Andy Murray and Sir Edward Elgar"],
            "answer": 0,
            "explanation": "✅ A!\n📖 David Hockney (pop art) and Henry Moore (abstract sculptures) are famous British artists.\n🇷🇺 Дэвид Хокни и Генри Мур — знаменитые британские художники.",
        },
        {
            "question": "Which TWO of the following countries are members of the Commonwealth?",
            "translation": "🇷🇺 Какие ДВЕ страны являются членами Содружества?",
            "options": ["A — USA and Australia", "B — Australia and Canada", "C — Canada and Russia", "D — Australia and Russia"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Australia and Canada are members of the Commonwealth (56 member states).\n🇷🇺 Австралия и Канада — члены Содружества наций.",
        },
    ],
    3: [
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Carrying a weapon is an example of a criminal offence.", "B — Being in debt is an example of a criminal offence."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Carrying a weapon is a criminal offence.\n🇷🇺 Ношение оружия — уголовное преступление.",
        },
        {
            "question": "Which TWO developments are associated with the Swinging Sixties?",
            "translation": "🇷🇺 Какие ДВА события связаны с Лихими шестидесятыми?",
            "options": ["A — Reform of abortion law and introduction of decimal currency", "B — Reform of children's rights law and introduction of decimal currency", "C — Reform of children's rights law and reform of divorce law", "D — Reform of abortion law and reform of divorce law"],
            "answer": 3,
            "explanation": "✅ D!\n📖 In the 1960s, laws on abortion and divorce were liberalised.\n🇷🇺 В 60-е были либерализованы законы об абортах и разводе.",
        },
        {
            "question": "Which TWO religions celebrate Diwali?",
            "translation": "🇷🇺 Какие ДВЕ религии отмечают Дивали?",
            "options": ["A — Hindus and Christians", "B — Hindus and Sikhs", "C — Christians and Sikhs", "D — Buddhists and Christians"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Diwali is celebrated by Hindus and Sikhs.\n🇷🇺 Дивали отмечают индуисты и сикхи.",
        },
        {
            "question": "During the Great Depression of the 1930s, which TWO major new industries developed?",
            "translation": "🇷🇺 В Великую депрессию какие ДВЕ новые отрасли развились?",
            "options": ["A — Automobiles and aviation", "B — Ship building and coal mining", "C — Ship building and aviation", "D — Coal mining and automobiles"],
            "answer": 0,
            "explanation": "✅ A!\n📖 During the Great Depression, aviation and the automobile industry developed.\n🇷🇺 В 30-е развились авиация и автопром.",
        },
        {
            "question": "TRUE or FALSE?\nDundee and Aberdeen are cities in Northern Ireland.",
            "translation": "🇷🇺 Данди и Абердин — города в Северной Ирландии?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Dundee and Aberdeen are cities in Scotland.\n🇷🇺 Данди и Абердин — города в Шотландии.",
        },
        {
            "question": "Which TWO are examples of civil law?",
            "translation": "🇷🇺 Какие ДВА являются примерами гражданского права?",
            "options": ["A — Housing law and employment law", "B — Drugs law and racial crime law", "C — Employment law and drugs law", "D — Housing law and racial crime law"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Civil law includes housing law and employment law.\n🇷🇺 Гражданское право включает жилищное и трудовое право.",
        },
        {
            "question": "Which TWO of the following are Christian festivals celebrated in the UK?",
            "translation": "🇷🇺 Какие ДВА христианских праздника отмечаются в UK?",
            "options": ["A — Halloween and New Year", "B — Easter and Christmas", "C — Christmas and New Year", "D — Easter and Halloween"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Easter and Christmas are the two main Christian festivals.\n🇷🇺 Пасха и Рождество — два главных христианских праздника.",
        },
        {
            "question": "Which TWO of the following wars were English kings involved in during the Middle Ages?",
            "translation": "🇷🇺 В каких ДВУХ войнах участвовали английские короли в Средние века?",
            "options": ["A — The Crusades and the First World War", "B — The Crimean War and the Crusades", "C — The Crimean War and the Hundred Years War", "D — The Crusades and the Hundred Years War"],
            "answer": 3,
            "explanation": "✅ D!\n📖 English kings fought in the Crusades and the Hundred Years War with France.\n🇷🇺 Английские короли участвовали в Крестовых походах и Столетней войне.",
        },
        {
            "question": "TRUE or FALSE?\nThe Channel Islands are a part of the UK.",
            "translation": "🇷🇺 Нормандские острова являются частью UK?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 The Channel Islands are Crown dependencies, not part of the UK.\n🇷🇺 Нормандские острова — зависимые территории Короны, не часть UK.",
        },
        {
            "question": "What is a fundamental principle of British life?",
            "translation": "🇷🇺 Что является фундаментальным принципом британской жизни?",
            "options": ["A — Relaxed work ethic", "B — Democracy", "C — Extremism", "D — Disrespect for the law"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Democracy is one of the fundamental principles of British society.\n🇷🇺 Демократия — один из фундаментальных принципов UK.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Civil servants are politically aligned to the elected government.", "B — Civil servants are politically neutral."],
            "answer": 1,
            "explanation": "✅ B!\n📖 Civil servants are chosen on merit and are politically neutral.\n🇷🇺 Государственные служащие политически нейтральны.",
        },
        {
            "question": "TRUE or FALSE?\nDuring the Victorian period, the British Empire grew to cover all of Africa and became the largest empire the world has ever seen, with more than 400 million people.",
            "translation": "🇷🇺 В викторианский период Британская империя стала крупнейшей в мире?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 The British Empire grew to cover India, Australia and large parts of Africa — over 400 million people.\n🇷🇺 Британская империя охватила более 400 миллионов человек.",
        },
        {
            "question": "TRUE or FALSE?\nDuring the Victorian period the British Empire became the largest empire the world has ever seen.",
            "translation": "🇷🇺 Британская империя стала крупнейшей в истории?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 The British Empire was the largest empire the world has ever seen.\n🇷🇺 Британская империя — крупнейшая в мировой истории.",
        },
        {
            "question": "Which TWO of the following are UK landmarks?",
            "translation": "🇷🇺 Какие ДВА — достопримечательности UK?",
            "options": ["A — Edinburgh Castle and the London Eye", "B — The National Trust and the London Eye", "C — The Eisteddfod and the National Trust", "D — The National Trust and Edinburgh Castle"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Edinburgh Castle and the London Eye are famous UK landmarks.\n🇷🇺 Эдинбургский замок и Лондонский глаз — знаменитые достопримечательности.",
        },
        {
            "question": "Dylan Thomas was a famous writer and poet from which country?",
            "translation": "🇷🇺 Дилан Томас — поэт из какой страны?",
            "options": ["A — England", "B — Wales", "C — Scotland", "D — Northern Ireland"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Dylan Thomas was a Welsh poet, known for Under Milk Wood.\n🇷🇺 Дилан Томас — валлийский поэт.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — County Courts deal with criminal cases.", "B — County Courts deal with civil disputes."],
            "answer": 1,
            "explanation": "✅ B!\n📖 County Courts deal with civil disputes including recovering money owed.\n🇷🇺 Окружные суды рассматривают гражданские споры.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Everyone in the UK with a TV must have a television licence.", "B — People who watch live TV on computers don't need a licence."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Everyone with any device for watching live TV must have a television licence.\n🇷🇺 Все, у кого есть устройство для живого ТВ, обязаны иметь лицензию.",
        },
        {
            "question": "Which TWO of the following are famous Paralympians?",
            "translation": "🇷🇺 Кто из перечисленных ДВОЕ — знаменитые паралимпийцы?",
            "options": ["A — Ellie Simmonds and Baroness Tanni Grey-Thompson", "B — Ellie Simmonds and Dame Ellen MacArthur", "C — Dame Jessica Ennis-Hill and Baroness Tanni Grey-Thompson", "D — Dame Jessica Ennis-Hill and Dame Ellen MacArthur"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Tanni Grey-Thompson won 16 Paralympic medals. Ellie Simmonds won gold in swimming.\n🇷🇺 Тanni Грей-Томпсон и Элли Симмондс — знаменитые паралимпийцы.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Elizabeth I was successful in balancing her wishes against those of the Houses of Parliament.", "B — Elizabeth I was not successful in balancing her wishes against those of the Houses of Parliament."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Elizabeth I was successful in balancing her wishes and views against Parliament.\n🇷🇺 Елизавета I успешно балансировала между Парламентом и своими интересами.",
        },
        {
            "question": "Which court would you use to get back money that was owed to you?",
            "translation": "🇷🇺 В какой суд обратиться для возврата долга?",
            "options": ["A — County Court", "B — Magistrates Court", "C — Youth Court", "D — Coroner's Court"],
            "answer": 0,
            "explanation": "✅ A!\n📖 County Courts deal with civil disputes including recovering money owed.\n🇷🇺 Окружной суд рассматривает дела о возврате долгов.",
        },
        {
            "question": "TRUE or FALSE?\nEmmeline Pankhurst is famous for her role in the campaign to give women the vote in parliamentary elections.",
            "translation": "🇷🇺 Эммелин Панкхёрст известна борьбой за право женщин голосовать?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 Emmeline Pankhurst (1858–1928) co-founded the WSPU and campaigned for women's suffrage.\n🇷🇺 Панкхёрст основала WSPU и боролась за избирательное право женщин.",
        },
        {
            "question": "TRUE or FALSE?\nUK citizens must practise a Christian religion.",
            "translation": "🇷🇺 Граждане UK обязаны исповедовать христианство?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Everyone has the legal right to choose their religion, or choose not to practise a religion.\n🇷🇺 Каждый вправе выбирать религию или не исповедовать никакой.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — People in paid work need to pay National Insurance Contributions.", "B — People in paid work do not need to pay National Insurance Contributions."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Almost everybody in paid work must pay National Insurance Contributions.\n🇷🇺 Все работающие обязаны платить взносы НС.",
        },
        {
            "question": "The Enlightenment led to major developments in which TWO areas?",
            "translation": "🇷🇺 Просвещение привело к развитию в каких ДВУХ областях?",
            "options": ["A — Science and politics", "B — History and theatre", "C — Science and theatre", "D — Politics and history"],
            "answer": 0,
            "explanation": "✅ A!\n📖 The Enlightenment brought new ideas in science and politics.\n🇷🇺 Просвещение дало развитие науке и политике.",
        },
    ],
    4: [
        {
            "question": "Which TWO of the following are examples of criminal law?",
            "translation": "🇷🇺 Какие ДВА являются примерами уголовного права?",
            "options": ["A — Disputes about faulty goods and discrimination in the workplace", "B — Racial crime and discrimination in the workplace", "C — Racial crime and disputes about faulty goods", "D — Racial crime and selling tobacco to anyone under the age of 18"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Racial crime and selling tobacco to under-18s are criminal offences.\n🇷🇺 Расовые преступления и продажа табака несовершеннолетним — уголовные дела.",
        },
        {
            "question": "TRUE or FALSE?\nBritain and Germany developed Concorde, a supersonic passenger aircraft.",
            "translation": "🇷🇺 Великобритания и Германия разработали Конкорд?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Concorde was developed by Britain and France. It flew from 1969 and retired in 2003.\n🇷🇺 Конкорд разработали Великобритания и Франция.",
        },
        {
            "question": "Which of the following is dealt with under civil law?",
            "translation": "🇷🇺 Что регулируется гражданским правом?",
            "options": ["A — Debt", "B — Violent crime", "C — Burglary", "D — Disorderly behaviour"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Debt is a civil matter.\n🇷🇺 Долг — гражданское дело.",
        },
        {
            "question": "Which TWO of the following are major horse-racing events in the UK?",
            "translation": "🇷🇺 Какие ДВА — крупные скачки в UK?",
            "options": ["A — The Open Championship and Scottish Grand National", "B — The Open Championship and Six Nations Championship", "C — Scottish Grand National and Six Nations Championship", "D — Scottish Grand National and Royal Ascot"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Royal Ascot in Berkshire and the Scottish Grand National at Ayr are major horse-racing events.\n🇷🇺 Королевский Аскот и Шотландский Гранд Нэшнл — крупные скачки.",
        },
        {
            "question": "TRUE or FALSE?\nFlorence Nightingale is famous for her work on education in the 19th century.",
            "translation": "🇷🇺 Найтингейл известна работой в сфере образования?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Florence Nightingale is regarded as the founder of modern nursing, not education.\n🇷🇺 Найтингейл — основатель современного сестринского дела, не образования.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — There is no place in British society for extreme views.", "B — Britain encourages people to have extreme views."],
            "answer": 0,
            "explanation": "✅ A!\n📖 There is no place for extremism or intolerance in British society.\n🇷🇺 В британском обществе нет места экстремизму.",
        },
        {
            "question": "What important event happened in England in 1066?",
            "translation": "🇷🇺 Какое важное событие произошло в Англии в 1066?",
            "options": ["A — The Romans left England", "B — The building of the Offa Dyke", "C — The Norman Conquest", "D — The Battle of Bannockburn"],
            "answer": 2,
            "explanation": "✅ C!\n📖 In 1066 William the Duke of Normandy defeated Harold at the Battle of Hastings — the Norman Conquest.\n🇷🇺 Нормандское завоевание — последнее успешное вторжение в Англию.",
        },
        {
            "question": "Which event occurs each year on the third Sunday in June?",
            "translation": "🇷🇺 Что происходит каждый год в третье воскресенье июня?",
            "options": ["A — Halloween", "B — Father's Day", "C — Boxing Day", "D — Remembrance Day"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Father's Day is the third Sunday in June.\n🇷🇺 День отца — третье воскресенье июня.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Donated blood is used by hospitals to help people with injuries and illnesses.", "B — Donated blood is not used by hospitals."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Donated blood is used by hospitals to help people with injuries and illnesses.\n🇷🇺 Донорская кровь используется больницами для лечения пациентов.",
        },
        {
            "question": "Which of the following was a well known author of children's books?",
            "translation": "🇷🇺 Кто из перечисленных известен детскими книгами?",
            "options": ["A — Roald Dahl", "B — William Shakespeare", "C — Graham Greene", "D — Jane Austen"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Roald Dahl was born in Wales to Norwegian parents and is best known for his children's books.\n🇷🇺 Роальд Даль — знаменитый автор детских книг.",
        },
        {
            "question": "What happened to Margaret Thatcher in 1979 to make her famous in UK history?",
            "translation": "🇷🇺 Что произошло с Маргарет Тэтчер в 1979 году?",
            "options": ["A — She took part in the Olympics.", "B — She became a High Court judge.", "C — She became the first woman Prime Minister.", "D — She was made a general in the British army."],
            "answer": 2,
            "explanation": "✅ C!\n📖 Margaret Thatcher became the first woman Prime Minister of the UK in 1979.\n🇷🇺 В 1979 году Тэтчер стала первой женщиной-премьером UK.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Local elections for councillors are normally held in May.", "B — Local elections are normally held in March."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Local elections for councillors are held in May every year.\n🇷🇺 Местные выборы обычно проводятся в мае.",
        },
        {
            "question": "Which TWO of the following are major outdoor music festivals?",
            "translation": "🇷🇺 Какие ДВА — крупные музыкальные фестивали под открытым небом?",
            "options": ["A — Hogmanay and Glastonbury", "B — Royal Ascot and Isle of Wight Festival", "C — Royal Ascot and Hogmanay", "D — Isle of Wight Festival and Glastonbury"],
            "answer": 3,
            "explanation": "✅ D!\n📖 The Isle of Wight Festival and Glastonbury are major outdoor music festivals.\n🇷🇺 Фестиваль острова Уайт и Гластонбери — крупнейшие музыкальные фестивали UK.",
        },
        {
            "question": "After the Bill of Rights was passed in 1689, which TWO main political groups emerged?",
            "translation": "🇷🇺 После Билля о правах 1689 года какие ДВЕ политические группы появились?",
            "options": ["A — Labour and Tories", "B — Whigs and Nationalists", "C — Nationalists and Tories", "D — Whigs and Tories"],
            "answer": 3,
            "explanation": "✅ D!\n📖 After the Bill of Rights, the Whigs and Tories emerged as the two main groups in Parliament.\n🇷🇺 После Билля о правах появились виги и тори.",
        },
        {
            "question": "TRUE or FALSE?\nForcing another person to marry is a criminal offence in the UK.",
            "translation": "🇷🇺 Принуждение к браку — уголовное преступление в UK?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 Forced marriage is a criminal offence in the UK.\n🇷🇺 Принудительный брак — уголовное преступление.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — The first professional UK football clubs were formed in the late 19th century.", "B — The first professional UK football clubs were formed in 1066."],
            "answer": 0,
            "explanation": "✅ A!\n📖 The first professional football clubs in the UK were formed in the late 19th century.\n🇷🇺 Первые профессиональные клубы UK появились в конце 19 века.",
        },
        {
            "question": "TRUE or FALSE?\nGetting to know your neighbours can help you to become part of the community.",
            "translation": "🇷🇺 Знакомство с соседями помогает стать частью сообщества?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 Getting to know your neighbours helps you become part of the community.\n🇷🇺 Знакомство с соседями помогает стать частью сообщества.",
        },
        {
            "question": "Which collection of poems was written by Geoffrey Chaucer?",
            "translation": "🇷🇺 Какой сборник написал Чосер?",
            "options": ["A — The Westbury Tales", "B — The Ambridge Tales", "C — The London Tales", "D — The Canterbury Tales"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Geoffrey Chaucer wrote The Canterbury Tales — poems about pilgrims going to Canterbury.\n🇷🇺 Чосер написал «Кентерберийские рассказы».",
        },
        {
            "question": "Which is the most popular sport in the UK?",
            "translation": "🇷🇺 Самый популярный спорт в UK?",
            "options": ["A — Football", "B — Rugby", "C — Golf", "D — Tennis"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Football is the UK's most popular sport.\n🇷🇺 Футбол — самый популярный спорт в UK.",
        },
        {
            "question": "When a Member of Parliament (MP) dies or resigns, what is the election called?",
            "translation": "🇷🇺 Как называются выборы при уходе депутата?",
            "options": ["A — Hustings", "B — Re-selection", "C — Selection", "D — By-election"],
            "answer": 3,
            "explanation": "✅ D!\n📖 When an MP dies or resigns, there is a by-election in their constituency.\n🇷🇺 Дополнительные выборы (by-election) проводятся при уходе депутата.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — After 70, drivers must renew their licence every three years.", "B — After 70, drivers must renew their licence every five years."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Drivers can use their licence until 70. After that it is valid for three years at a time.\n🇷🇺 После 70 лет водительские права нужно обновлять каждые 3 года.",
        },
        {
            "question": "Which country was the composer George Frederick Handel born in?",
            "translation": "🇷🇺 В какой стране родился Гендель?",
            "options": ["A — Iceland", "B — Russia", "C — Japan", "D — Germany"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Handel was born in Germany in 1685 and became a British citizen in 1727.\n🇷🇺 Гендель родился в Германии, стал британским гражданином в 1727 году.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — George and Robert Stephenson were famous pioneers of railway engines.", "B — George and Robert Stephenson were famous pioneers of agricultural changes."],
            "answer": 0,
            "explanation": "✅ A!\n📖 George and Robert Stephenson were famous pioneers of railway engines.\n🇷🇺 Стефенсоны — пионеры железнодорожных двигателей.",
        },
        {
            "question": "Which of the following is a famous garden in Scotland?",
            "translation": "🇷🇺 Какой из перечисленных — знаменитый сад в Шотландии?",
            "options": ["A — Hidcote", "B — Inveraray Castle", "C — Mount Stewart", "D — Bodnant Garden"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Inveraray Castle is a famous garden in Scotland.\n🇷🇺 Замок Инверари — знаменитый сад в Шотландии.",
        },
    ],
    5: [
        {
            "question": "TRUE or FALSE?\nIf an accused person is aged 18 to 21, their case will be heard in a Youth Court.",
            "translation": "🇷🇺 Дела обвиняемых 18–21 лет рассматривает Суд по делам молодёжи?",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": "❌ False!\n📖 Youth Court handles cases for accused persons aged 10 to 17.\n🇷🇺 Суд по делам молодёжи — для лиц 10–17 лет.",
        },
        {
            "question": "Which TWO of the following are fundamental principles of British life?",
            "translation": "🇷🇺 Какие ДВА — фундаментальные принципы британской жизни?",
            "options": ["A — Only driving on weekdays and participation in community life", "B — Participation in community life and tolerance of those with different faiths", "C — Only driving on weekdays and growing own fruit and vegetables", "D — Growing own fruit and vegetables and tolerance of different faiths"],
            "answer": 1,
            "explanation": "✅ B!\n📖 Participation in community life and tolerance of different faiths are fundamental principles.\n🇷🇺 Участие в жизни сообщества и толерантность — ключевые принципы.",
        },
        {
            "question": "What is the name of the Houses of Parliament's clock tower?",
            "translation": "🇷🇺 Как называется часовая башня Парламента?",
            "options": ["A — Big Ben Tower", "B — Parliament Tower", "C — House of Commons Tower", "D — Elizabeth Tower"],
            "answer": 3,
            "explanation": "✅ D!\n📖 The clock tower was named Elizabeth Tower in honour of Queen Elizabeth II's Diamond Jubilee in 2012.\n🇷🇺 Башня называется Елизаветинской башней с 2012 года.",
        },
        {
            "question": "Which of the following was a famous British inventor?",
            "translation": "🇷🇺 Кто из перечисленных — знаменитый британский изобретатель?",
            "options": ["A — Dylan Thomas", "B — Clement Attlee", "C — Emmeline Pankhurst", "D — Sir Peter Mansfield"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Sir Peter Mansfield (1933–2017) was co-inventor of the MRI scanner.\n🇷🇺 Сэр Питер Мэнсфилд — изобретатель МРТ-сканера.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Jane Austen and Charles Dickens were famous novelists.", "B — Jane Austen and Charles Dickens were famous painters."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Jane Austen and Charles Dickens were famous novelists.\n🇷🇺 Остин и Диккенс — знаменитые романисты.",
        },
        {
            "question": "Which of the following is a traditional food associated with Scotland?",
            "translation": "🇷🇺 Какое блюдо традиционно шотландское?",
            "options": ["A — Roast beef", "B — Ulster fry", "C — Fish and chips", "D — Haggis"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Haggis is a traditional Scottish food — sheep's stomach stuffed with offal, suet, onions and oatmeal.\n🇷🇺 Хаггис — традиционное шотландское блюдо.",
        },
        {
            "question": "When is a by-election for a parliamentary seat held?",
            "translation": "🇷🇺 Когда проводятся дополнительные выборы?",
            "options": ["A — Half-way through a parliamentary term", "B — Every two years", "C — When an MP dies or resigns", "D — When the Prime Minister decides"],
            "answer": 2,
            "explanation": "✅ C!\n📖 A by-election is held when an MP dies or resigns.\n🇷🇺 Дополнительные выборы — при смерти или отставке депутата.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Halloween is when lovers exchange cards and gifts.", "B — Halloween has its roots in an ancient pagan festival marking the beginning of winter."],
            "answer": 1,
            "explanation": "✅ B!\n📖 Halloween is an ancient pagan festival marking the beginning of winter.\n🇷🇺 Хэллоуин — древний языческий праздник начала зимы.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — In 1588, the English defeated the Spanish Armada.", "B — In 1588, the English defeated German bomber planes."],
            "answer": 0,
            "explanation": "✅ A!\n📖 In 1588, the English defeated the Spanish Armada.\n🇷🇺 В 1588 году Англия разгромила Испанскую Армаду.",
        },
        {
            "question": "Which TWO actions can a judge take if a public body is not respecting someone's legal rights?",
            "translation": "🇷🇺 Какие ДВА действия может предпринять судья против нарушающего права органа?",
            "options": ["A — Order compensation and close down the body", "B — Place members in prison and close down the body", "C — Order body to change practices and pay compensation", "D — Place members in prison and order to change practices"],
            "answer": 2,
            "explanation": "✅ C!\n📖 A judge can order the body to change its practices and/or pay compensation.\n🇷🇺 Судья может обязать орган изменить практику и выплатить компенсацию.",
        },
        {
            "question": "Who invaded England in 1066?",
            "translation": "🇷🇺 Кто вторгся в Англию в 1066?",
            "options": ["A — Richard the Lionheart", "B — King Canute", "C — William, the Duke of Normandy", "D — Harold of Wessex"],
            "answer": 2,
            "explanation": "✅ C!\n📖 William the Duke of Normandy invaded England in 1066 and defeated Harold at Hastings.\n🇷🇺 Вильгельм Нормандский вторгся в Англию в 1066 году.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — In a Crown Court case, the judge decides the penalty.", "B — In a Crown Court case, the jury decides the penalty."],
            "answer": 0,
            "explanation": "✅ A!\n📖 In a Crown Court, if the jury finds the defendant guilty, the judge decides on the penalty.\n🇷🇺 В суде Короны присяжные решают виновность, судья — наказание.",
        },
        {
            "question": "Which of these events changed the powers of the king in 1215?",
            "translation": "🇷🇺 Какое событие изменило власть короля в 1215?",
            "options": ["A — The Domesday Book", "B — The Magna Carta", "C — The Reform Act", "D — The Black Death"],
            "answer": 1,
            "explanation": "✅ B!\n📖 The Magna Carta (1215) established that even the king was subject to the law.\n🇷🇺 Великая хартия вольностей установила верховенство закона над королём.",
        },
        {
            "question": "Which TWO are famous British composers?",
            "translation": "🇷🇺 Кто из перечисленных ДВОЕ — знаменитые британские композиторы?",
            "options": ["A — Henry Purcell and Ralph Vaughan Williams", "B — Johann Sebastian Bach and Henry Purcell", "C — Claude Debussy and Henry Purcell", "D — Claude Debussy and Johann Sebastian Bach"],
            "answer": 0,
            "explanation": "✅ A!\n📖 Henry Purcell wrote church music and operas. Ralph Vaughan Williams wrote orchestral works based on English folk music.\n🇷🇺 Пёрселл и Воан Уильямс — знаменитые британские композиторы.",
        },
        {
            "question": "If your car is more than three years old, how often will it need an MOT test?",
            "translation": "🇷🇺 Как часто нужен MOT для машины старше 3 лет?",
            "options": ["A — Every three years", "B — Every six months", "C — Every 10 years", "D — Every year"],
            "answer": 3,
            "explanation": "✅ D!\n📖 Cars over three years old must have an MOT test every year.\n🇷🇺 Машины старше 3 лет проходят технический осмотр ежегодно.",
        },
        {
            "question": "In 1348, a third of the population died as a result of which plague?",
            "translation": "🇷🇺 В 1348 году треть населения погибла от какой чумы?",
            "options": ["A — The Blue Death", "B — The White Death", "C — The Green Death", "D — The Black Death"],
            "answer": 3,
            "explanation": "✅ D!\n📖 The Black Death (bubonic plague) came to Britain in 1348 and killed a third of the population.\n🇷🇺 «Чёрная смерть» 1348 года уничтожила треть населения Британии.",
        },
        {
            "question": "What type of church is the Church of Scotland?",
            "translation": "🇷🇺 Что представляет собой Церковь Шотландии?",
            "options": ["A — Quaker", "B — Roman Catholic", "C — Presbyterian", "D — Methodist"],
            "answer": 2,
            "explanation": "✅ C!\n📖 The Church of Scotland is a Presbyterian church.\n🇷🇺 Церковь Шотландии — пресвитерианская.",
        },
        {
            "question": "TRUE or FALSE?\nParticipating in your community is a fundamental principle of British life.",
            "translation": "🇷🇺 Участие в жизни сообщества — фундаментальный принцип?",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": "✅ True!\n📖 Participation in community life is a fundamental principle of British society.\n🇷🇺 Участие в жизни сообщества — фундаментальный принцип.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — The Wars of the Roses were between the Houses of Lancaster and York.", "B — The Wars of the Roses were between the Houses of Windsor and Tudor."],
            "answer": 0,
            "explanation": "✅ A!\n📖 The Wars of the Roses were between the Houses of Lancaster and York.\n🇷🇺 Войны Роз — между домами Ланкастер и Йорк.",
        },
        {
            "question": "What important change to voting rights took place in 1969?",
            "translation": "🇷🇺 Какое изменение избирательного права произошло в 1969?",
            "options": ["A — Women over 35 were given the vote.", "B — Prisoners were given the vote.", "C — The voting age was reduced to 18 for men and women.", "D — Compulsory voting was introduced."],
            "answer": 2,
            "explanation": "✅ C!\n📖 In 1969, the voting age was reduced to 18 for men and women.\n🇷🇺 В 1969 году возраст голосования снизили до 18 лет.",
        },
        {
            "question": "In 1776, 13 British colonies declared independence. In which part of the world were these colonies?",
            "translation": "🇷🇺 В 1776 году 13 колоний провозгласили независимость. Где они находились?",
            "options": ["A — Australia", "B — Canada", "C — America", "D — South Africa"],
            "answer": 2,
            "explanation": "✅ C!\n📖 In 1776, 13 American colonies declared independence. Britain recognised this in 1783.\n🇷🇺 13 американских колоний провозгласили независимость в 1776 году.",
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое утверждение верно?",
            "options": ["A — Lancelot Capability Brown and Gertrude Jekyll were famous garden designers.", "B — Lancelot Capability Brown and Gertrude Jekyll were famous Sherlock Holmes characters."],
            "answer": 0,
            "explanation": "✅ A!\n📖 Capability Brown designed natural landscapes. Gertrude Jekyll worked with Edwin Lutyens on colourful gardens.\n🇷🇺 Браун и Джекилл — знаменитые британские дизайнеры садов.",
        },
        {
            "question": "Which TWO are famous horse-racing events?",
            "translation": "🇷🇺 Какие ДВА — знаменитые скачки?",
            "options": ["A — The Cup Final and the Six Nations", "B — The Grand National and Royal Ascot", "C — Royal Ascot and the Six Nations", "D — The Grand National and the Cup Final"],
            "answer": 1,
            "explanation": "✅ B!\n📖 The Grand National (Aintree) and Royal Ascot (Berkshire) are famous horse-racing events.\n🇷🇺 Гранд Нэшнл и Королевский Аскот — знаменитые скачки.",
        },
        {
            "question": "What is the minimum age you can drive a car or motorcycle in the UK?",
            "translation": "🇷🇺 Минимальный возраст для вождения в UK?",
            "options": ["A — 17", "B — 21", "C — 18", "D — 25"],
            "answer": 0,
            "explanation": "✅ A!\n📖 In the UK, you must be at least 17 years old to drive a car or motorcycle.\n🇷🇺 Минимальный возраст для вождения — 17 лет.",
        },
    ],
    6: [
    {
        "question": "How old do you need to be in order to stand for public office?",
        "translation": "🇷🇺 Сколько лет нужно, чтобы баллотироваться на публичную должность?",
        "options": [
            "A — 16",
            "B — 18",
            "C — 20",
            "D — 21"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Most citizens of the UK, Ireland or the Commonwealth aged 18 or over can stand for public office.\n\n"
            "🇷🇺 *Перевод:* Большинство граждан UK, Ирландии или Содружества в возрасте 18+ могут баллотироваться."
        ),
    },
    {
        "question": "What sort of cases do Crown Courts and Sheriff Courts deal with?",
        "translation": "🇷🇺 Какие дела рассматривают суды Короны и суды шерифов?",
        "options": [
            "A — Small claims procedures",
            "B — Youth cases",
            "C — Minor criminal cases",
            "D — Serious offences"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 In England, Wales and Northern Ireland, serious offences are tried in a Crown Court. In Scotland, in a Sheriff Court.\n\n"
            "🇷🇺 *Перевод:* Серьёзные преступления — суды Короны (Англия/Уэльс/СИ) и суды шерифов (Шотландия)."
        ),
    },
    {
        "question": "What is the minimum age at which you can legally buy alcohol in the UK?",
        "translation": "🇷🇺 Минимальный возраст для легальной покупки алкоголя в UK?",
        "options": [
            "A — 20",
            "B — 21",
            "C — 18",
            "D — 19"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 It is a criminal offence to sell alcohol to anyone who is under 18.\n\n"
            "🇷🇺 *Перевод:* Продажа алкоголя лицам младше 18 лет — уголовное преступление."
        ),
    },
    {
        "question": "Which TWO famous London buildings are built in the 19th-century gothic style?",
        "translation": "🇷🇺 Какие ДВА знаменитых лондонских здания построены в готическом стиле 19 века?",
        "options": [
            "A — The Houses of Parliament and Buckingham Palace",
            "B — St Paul\'s Cathedral and St Pancras Station",
            "C — St Paul\'s Cathedral and Buckingham Palace",
            "D — The Houses of Parliament and St Pancras Station"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The Houses of Parliament and St Pancras Station were built in the 19th-century gothic style.\n\n"
            "🇷🇺 *Перевод:* Здания Парламента и вокзал Сент-Панкрас — неоготический стиль 19 века."
        ),
    },
    {
        "question": "How many people serve on a jury in Scotland?",
        "translation": "🇷🇺 Сколько человек входит в состав присяжных в Шотландии?",
        "options": [
            "A — 8",
            "B — 11",
            "C — 15",
            "D — 20"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 In Scotland a jury has 15 members. In England, Wales and Northern Ireland a jury has 12 members.\n\n"
            "🇷🇺 *Перевод:* В Шотландии — 15 присяжных, в Англии/Уэльсе/СИ — 12."
        ),
    },
    {
        "question": "TRUE or FALSE?\nIn 1588 the English defeated the Spanish Armada.",
        "translation": "🇷🇺 Верно или нет?\nВ 1588 году англичане разгромили Испанскую Армаду.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 In 1588, the English defeated the Spanish Armada — a large fleet sent by Spain to conquer England.\n\n"
            "🇷🇺 *Перевод:* В 1588 году англичане разгромили Испанскую Армаду."
        ),
    },
    {
        "question": "Which TWO members of a family have a special day dedicated to them?",
        "translation": "🇷🇺 Каким ДВУМ членам семьи посвящён особый день?",
        "options": [
            "A — Uncles and aunts",
            "B — Mothers and aunts",
            "C — Fathers and aunts",
            "D — Fathers and mothers"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Mothering Sunday is celebrated three weeks before Easter and Father\'s Day on the third Sunday in June.\n\n"
            "🇷🇺 *Перевод:* День матери (за 3 недели до Пасхи) и День отца (3-е воскресенье июня)."
        ),
    },
    {
        "question": "How old do you have to be to go into a betting shop in the UK?",
        "translation": "🇷🇺 Сколько лет нужно для входа в букмекерскую контору в UK?",
        "options": [
            "A — 21",
            "B — 18",
            "C — 25",
            "D — 30"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 You have to be over 18 to go into betting shops or gambling clubs.\n\n"
            "🇷🇺 *Перевод:* Для входа в букмекерские конторы необходимо быть старше 18 лет."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — In 1776, 13 American colonies declared their independence from Britain.",
            "B — The American colonists were eventually defeated by the British."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 In 1776, 13 American colonies declared their independence from Britain.\n\n"
            "🇷🇺 *Перевод:* В 1776 году 13 американских колоний провозгласили независимость от Британии."
        ),
    },
    {
        "question": "How old must you be to ride a moped in the UK?",
        "translation": "🇷🇺 Сколько лет нужно, чтобы ездить на мопеде в UK?",
        "options": [
            "A — 18",
            "B — 25",
            "C — 16",
            "D — 21"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 In the UK you need to be at least 16 years old to ride a moped.\n\n"
            "🇷🇺 *Перевод:* В UK минимальный возраст для езды на мопеде — 16 лет."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Gilbert and Sullivan were a comedy double act.",
            "B — Gilbert and Sullivan wrote many comic operas."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Gilbert and Sullivan wrote comic operas including HMS Pinafore, The Pirates of Penzance and The Mikado.\n\n"
            "🇷🇺 *Перевод:* Гилберт и Салливан писали комические оперы, высмеивающие культуру и политику."
        ),
    },
    {
        "question": "TRUE or FALSE?\nBritish values and principles are based on history and traditions.",
        "translation": "🇷🇺 Верно или нет?\nБританские ценности и принципы основаны на истории и традициях.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 British society is founded on fundamental values and principles, based on history and traditions.\n\n"
            "🇷🇺 *Перевод:* Британское общество основано на ценностях, базирующихся на истории и традициях."
        ),
    },
    {
        "question": "TRUE or FALSE?\nIn 1833 the Emancipation Act abolished slavery throughout the British Empire.",
        "translation": "🇷🇺 Верно или нет?\nВ 1833 году Закон об эмансипации отменил рабство во всей Британской империи.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 In 1833 the Emancipation Act abolished slavery throughout the British Empire.\n\n"
            "🇷🇺 *Перевод:* В 1833 году рабство было отменено на всей территории Британской империи."
        ),
    },
    {
        "question": "Which of these is the name of a novel by Jane Austen?",
        "translation": "🇷🇺 Какое из произведений является романом Джейн Остен?",
        "options": [
            "A — Sense and Sensibility",
            "B — Far from the Madding Crowd",
            "C — Oliver Twist",
            "D — Our Man in Havana"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Jane Austen\'s novels include Pride and Prejudice and Sense and Sensibility.\n\n"
            "🇷🇺 *Перевод:* «Разум и чувство» — роман Джейн Остен."
        ),
    },
    {
        "question": "Which TWO things can you do to look after the environment?",
        "translation": "🇷🇺 Какие ДВА действия помогут сохранить окружающую среду?",
        "options": [
            "A — Recycle your waste and never turn your lights off.",
            "B — Drive your car as much as possible and never turn the lights off.",
            "C — Recycle your waste and walk and use public transport to get around.",
            "D — Drive your car as much as possible and recycle your waste."
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Recycle as much of your waste as you can. Walk and use public transport to protect the environment.\n\n"
            "🇷🇺 *Перевод:* Переработка мусора и общественный транспорт помогают защитить окружающую среду."
        ),
    },
    {
        "question": "Why is 1918 an important date in the history of women\'s rights?",
        "translation": "🇷🇺 Почему 1918 год важен в истории прав женщин?",
        "options": [
            "A — The first divorce laws were introduced.",
            "B — Women over the age of 30 were given voting rights.",
            "C — Equal pay laws were passed.",
            "D — Women were made legally responsible for their children."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 In 1918, women over the age of 30 were given voting rights. In 1928, women got the vote at 21.\n\n"
            "🇷🇺 *Перевод:* В 1918 году женщины старше 30 лет получили право голоса."
        ),
    },
    {
        "question": "TRUE or FALSE?\nIn 1921 a peace treaty was signed which led to Ireland becoming two countries.",
        "translation": "🇷🇺 Верно или нет?\nВ 1921 году был подписан мирный договор, разделивший Ирландию.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 In 1921 a peace treaty was signed and in 1922 Ireland became two countries.\n\n"
            "🇷🇺 *Перевод:* В 1922 году Ирландия разделилась на Северную Ирландию и Ирландское свободное государство."
        ),
    },
    {
        "question": "TRUE or FALSE?\nJohn Constable (1776–1837) founded the modern police force in England.",
        "translation": "🇷🇺 Верно или нет?\nДжон Констебл основал современную полицию в Англии.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 John Constable was a landscape painter famous for his works of Dedham Vale.\n\n"
            "🇷🇺 *Перевод:* Джон Констебл — художник-пейзажист, а не основатель полиции."
        ),
    },
    {
        "question": "Who appoints life peers in the House of Lords?",
        "translation": "🇷🇺 Кто назначает пожизненных пэров в Палату лордов?",
        "options": [
            "A — The monarch",
            "B — The Archbishop of Canterbury",
            "C — The Speaker of the House of Commons",
            "D — The Chief Whip"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Life peers are appointed by the monarch on the advice of the Prime Minister.\n\n"
            "🇷🇺 *Перевод:* Пожизненные пэры назначаются монархом по совету премьер-министра."
        ),
    },
    {
        "question": "Dunkirk is associated with which TWO events?",
        "translation": "🇷🇺 Дюнкерк ассоциируется с какими ДВУМЯ событиями?",
        "options": [
            "A — The fall of Singapore and small boats coming to the rescue",
            "B — The D-Day landings and the fall of Singapore",
            "C — The rescue of 300,000 men and small boats coming to the rescue",
            "D — The fall of Singapore and the rescue of 300,000 men"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 In 1940, civilian volunteers in small boats helped the Navy rescue 300,000 men from Dunkirk.\n\n"
            "🇷🇺 *Перевод:* В 1940 году малые суда помогли эвакуировать 300 000 солдат с берегов Дюнкерка."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Black Death caused the death of one third of people in Ireland.",
            "B — The Black Death caused the death of one third of people in England, Scotland and Wales."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 In 1348, the Black Death came to Britain. One third of the population of England, Scotland and Wales died.\n\n"
            "🇷🇺 *Перевод:* «Чёрная смерть» 1348 года унесла треть населения Англии, Шотландии и Уэльса."
        ),
    },
    {
        "question": "What happens when a Member of Parliament (MP) dies or resigns?",
        "translation": "🇷🇺 Что происходит, когда депутат Парламента умирает или уходит в отставку?",
        "options": [
            "A — The post remains vacant until the next General Election.",
            "B — Their party chooses someone to fill the post.",
            "C — A by-election is held to replace the MP.",
            "D — A neighbouring MP looks after the constituency."
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 If an MP dies or resigns, a by-election is held in his or her constituency.\n\n"
            "🇷🇺 *Перевод:* При уходе депутата проводятся дополнительные выборы (by-election)."
        ),
    },
    {
        "question": "Which festival is celebrated on 31 October?",
        "translation": "🇷🇺 Какой праздник отмечается 31 октября?",
        "options": [
            "A — Valentine\'s Day",
            "B — Bonfire Night",
            "C — Halloween",
            "D — Hogmanay"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Halloween is celebrated on 31 October.\n\n"
            "🇷🇺 *Перевод:* Хэллоуин отмечается 31 октября."
        ),
    },
    {
        "question": "TRUE or FALSE?\nMost people live in the countryside in the UK.",
        "translation": "🇷🇺 Верно или нет?\nБольшинство людей в UK живут в сельской местности.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 Most people in the UK live in towns and cities, but much of Britain is still countryside.\n\n"
            "🇷🇺 *Перевод:* Большинство жителей UK живут в городах."
        ),
    },
    ],
    7: [
    {
        "question": "TRUE or FALSE?\nThe 40 days before Easter are known as Lent.",
        "translation": "🇷🇺 Верно или нет?\n40 дней перед Пасхой называются Великим постом (Lent).",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Lent is a time when Christians take time to reflect and prepare for Easter. Many people give something up during this period.\n\n"
            "🇷🇺 *Перевод:* Великий пост — время размышлений и подготовки к Пасхе. Многие от чего-то отказываются."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Magistrates usually work unpaid and do not need legal qualifications.",
            "B — Magistrates must be specially trained legal experts who have been solicitors for three years."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Magistrates are members of the local community. They usually work unpaid and do not need legal qualifications.\n\n"
            "🇷🇺 *Перевод:* Мировые судьи — члены местного сообщества, работают бесплатно и не нуждаются в юридической квалификации."
        ),
    },
    {
        "question": "Which TWO were 20th-century British discoveries or inventions?",
        "translation": "🇷🇺 Какие ДВА из перечисленных — британские открытия или изобретения 20 века?",
        "options": [
            "A — Mobile phones and walkmans",
            "B — Cashpoints (ATMs) and walkmans",
            "C — Cloning a mammal and cashpoints (ATMs)",
            "D — Cloning a mammal and mobile phones"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 In 1996 Sir Ian Wilmut led the team that first cloned a mammal. In the 1960s James Goodfellow invented the cashpoint (ATM).\n\n"
            "🇷🇺 *Перевод:* В 1996 году — клонирование млекопитающего. В 1960-х — банкомат (ATM)."
        ),
    },
    {
        "question": "Who do some local councils appoint as a ceremonial leader?",
        "translation": "🇷🇺 Кого некоторые местные советы назначают церемониальным лидером?",
        "options": [
            "A — A local business leader",
            "B — A member of the Royal Family",
            "C — A local celebrity",
            "D — A mayor"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Many local authorities appoint a mayor, who is the ceremonial leader of the council.\n\n"
            "🇷🇺 *Перевод:* Многие местные органы власти назначают мэра — церемониального лидера совета."
        ),
    },
    {
        "question": "With which sport do you associate Lewis Hamilton, Jenson Button and Damon Hill?",
        "translation": "🇷🇺 С каким видом спорта вы ассоциируете Льюиса Хэмилтона, Дженсона Баттона и Деймона Хилла?",
        "options": [
            "A — Football",
            "B — Athletics",
            "C — Skiing",
            "D — Formula 1"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Lewis Hamilton, Jenson Button and Damon Hill are all British Grand Prix drivers who have won the Formula 1 World Championship.\n\n"
            "🇷🇺 *Перевод:* Хэмилтон, Баттон и Хилл — британские гонщики Формулы 1, чемпионы мира."
        ),
    },
    {
        "question": "TRUE or FALSE?\nA public vote in 2002 decided that Winston Churchill was the greatest Briton of all time.",
        "translation": "🇷🇺 Верно или нет?\nВ 2002 году публичное голосование признало Черчилля величайшим британцем всех времён.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 In 2002 Winston Churchill (1874–1965) was voted the greatest Briton of all time by the public.\n\n"
            "🇷🇺 *Перевод:* В 2002 году Черчилль был признан величайшим британцем всех времён по итогам народного голосования."
        ),
    },
    {
        "question": "What happens when Members of Parliament (MPs) hold surgeries?",
        "translation": "🇷🇺 Что происходит, когда депутаты Парламента проводят приёмы (surgeries)?",
        "options": [
            "A — Local councillors meet their MP to discuss local issues.",
            "B — Members of the public meet their MP to discuss issues.",
            "C — MPs meet doctors to discuss local health issues.",
            "D — MPs meet the press to discuss national issues."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Many MPs hold regular local surgeries, where constituents can go in person to talk about issues that concern them.\n\n"
            "🇷🇺 *Перевод:* На приёмах (surgeries) избиратели могут лично встретиться со своим депутатом."
        ),
    },
    {
        "question": "Which of the following UK landmarks is in Northern Ireland?",
        "translation": "🇷🇺 Какая из следующих достопримечательностей UK находится в Северной Ирландии?",
        "options": [
            "A — Big Ben",
            "B — Snowdonia",
            "C — The Giant\'s Causeway",
            "D — The Eden Project"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Located on the north-east coast of Northern Ireland, the Giant\'s Causeway is a land formation of columns made from volcanic lava.\n\n"
            "🇷🇺 *Перевод:* Мостовая Гигантов — скальное образование из вулканической лавы на северо-востоке Северной Ирландии."
        ),
    },
    {
        "question": "What task is associated with the National Trust?",
        "translation": "🇷🇺 С какой задачей связан Национальный фонд (National Trust)?",
        "options": [
            "A — Building new public roads",
            "B — Preserving old aircraft",
            "C — Preserving important buildings and places",
            "D — Managing investment accounts"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The National Trust works to preserve important buildings, coastline and countryside in the UK.\n\n"
            "🇷🇺 *Перевод:* Национальный фонд занимается сохранением важных зданий, побережья и сельской местности UK."
        ),
    },
    {
        "question": "Which of the following is a fundamental principle of British life?",
        "translation": "🇷🇺 Какой из следующих принципов является основополагающим в британской жизни?",
        "options": [
            "A — Extremism",
            "B — Individual liberty",
            "C — Intolerance",
            "D — Inequality"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Individual liberty is a fundamental principle of British life. There is no place in British society for extremism or intolerance.\n\n"
            "🇷🇺 *Перевод:* Личная свобода — основополагающий принцип британской жизни."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — In Elizabeth I\'s time, English settlers began to colonise Australia.",
            "B — In Elizabeth I\'s time, English settlers began to colonise the eastern coast of America."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 In Elizabeth I\'s time, English settlers first began to colonise the eastern coast of America.\n\n"
            "🇷🇺 *Перевод:* При Елизавете I английские поселенцы начали колонизацию восточного побережья Америки."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Members of the House of Lords are not elected by the people.",
            "B — Members of the House of Lords are voted in by members of the House of Commons."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Members of the House of Lords are not elected by the people.\n\n"
            "🇷🇺 *Перевод:* Члены Палаты лордов не избираются народом."
        ),
    },
    {
        "question": "In which battle during the First World War did the British suffer 60,000 casualties on the first day?",
        "translation": "🇷🇺 В какой битве Первой мировой войны британцы потеряли 60 000 человек в первый день?",
        "options": [
            "A — Agincourt",
            "B — El Alamein",
            "C — The Somme",
            "D — Waterloo"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 In July 1916 the British suffered 60,000 casualties on the first day of the Battle of the Somme.\n\n"
            "🇷🇺 *Перевод:* В июле 1916 года в первый день битвы на Сомме британцы потеряли 60 000 человек."
        ),
    },
    {
        "question": "TRUE or FALSE?\nMembers of the public are allowed to attend Youth Court hearings.",
        "translation": "🇷🇺 Верно или нет?\nОбщественность допускается на заседания Суда по делам несовершеннолетних.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 Members of the public are not allowed in Youth Courts, and the name or photographs of the accused cannot be published in newspapers.\n\n"
            "🇷🇺 *Перевод:* Общественность не допускается в Суд по делам несовершеннолетних, СМИ не могут публиковать данные обвиняемого."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — A famous sailing event is held at Cowes on the Isle of Wight.",
            "B — A famous sailing event is held in the city of Norwich."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Many sailing events are held throughout the UK, the most famous of which is at Cowes on the Isle of Wight.\n\n"
            "🇷🇺 *Перевод:* Самые известные парусные гонки проходят в Коузе на острове Уайт."
        ),
    },
    {
        "question": "During which part of the year are pantomime productions staged in theatres?",
        "translation": "🇷🇺 В какое время года театры ставят пантомимы?",
        "options": [
            "A — Easter",
            "B — Summer",
            "C — Christmas",
            "D — Valentine\'s Day"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Many theatres produce a pantomime at Christmas time. They are light-hearted plays with music and comedy.\n\n"
            "🇷🇺 *Перевод:* Рождественские пантомимы — традиционные лёгкие спектакли с музыкой и комедией."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe Restoration refers to the re-establishment of Catholicism as the official Church in the 17th century.",
        "translation": "🇷🇺 Верно или нет?\nРеставрация означала восстановление католицизма как официальной церкви в 17 веке.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The Restoration refers to Parliament inviting Charles II back from exile. He was crowned King of England, Wales, Scotland and Ireland.\n\n"
            "🇷🇺 *Перевод:* Реставрация — возвращение Карла II из изгнания и его коронация, а не восстановление католицизма."
        ),
    },
    {
        "question": "TRUE or FALSE?\nMembers of the armed forces cannot stand for public office.",
        "translation": "🇷🇺 Верно или нет?\nЧлены вооружённых сил не могут баллотироваться на публичную должность.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Most citizens of the UK, Ireland or the Commonwealth aged 18 or over can stand for public office. There are some exceptions, including members of the armed forces.\n\n"
            "🇷🇺 *Перевод:* Члены вооружённых сил — одно из исключений из правила о праве баллотироваться на публичную должность."
        ),
    },
    {
        "question": "Which TWO political parties formed the coalition government in 2010?",
        "translation": "🇷🇺 Какие ДВЕ партии сформировали коалиционное правительство в 2010 году?",
        "options": [
            "A — Labour and Chartists",
            "B — Chartists and Liberal Democrats",
            "C — Conservatives and Liberal Democrats",
            "D — Conservatives and Labour"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 In May 2010, the Conservative and Liberal Democrat parties formed a coalition. David Cameron became Prime Minister.\n\n"
            "🇷🇺 *Перевод:* В мае 2010 года консерваторы и либерал-демократы образовали коалицию. Дэвид Кэмерон стал премьером."
        ),
    },
    {
        "question": "How often are Members of Parliament (MPs) elected?",
        "translation": "🇷🇺 Как часто избираются члены Парламента?",
        "options": [
            "A — At least every three years",
            "B — Every six months",
            "C — Every year",
            "D — At least every five years"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 MPs are elected at a General Election, which is held at least every five years.\n\n"
            "🇷🇺 *Перевод:* Депутаты избираются на всеобщих выборах, которые проводятся не реже одного раза в пять лет."
        ),
    },
    {
        "question": "In the 19th century, the UK produced more than half the world\'s supply of one of these products. Which one?",
        "translation": "🇷🇺 В 19 веке UK производила более половины мирового запаса одного из этих продуктов. Какого?",
        "options": [
            "A — Cotton cloth",
            "B — Beer",
            "C — Cigarettes",
            "D — Rubber"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 In the 19th century the UK produced more than half of the world\'s supplies of iron, coal and cotton cloth.\n\n"
            "🇷🇺 *Перевод:* В 19 веке UK производила более половины мирового запаса железа, угля и хлопчатобумажной ткани."
        ),
    },
    {
        "question": "TRUE or FALSE?\nMost people in the UK live in towns and cities.",
        "translation": "🇷🇺 Верно или нет?\nБольшинство людей в UK живут в городах.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Most people live in towns and cities but much of Britain is still countryside.\n\n"
            "🇷🇺 *Перевод:* Большинство жителей UK живут в городах, хотя большая часть страны — сельская местность."
        ),
    },
    {
        "question": "Which TWO courts deal with minor criminal cases in the UK?",
        "translation": "🇷🇺 Какие ДВА суда рассматривают мелкие уголовные дела в UK?",
        "options": [
            "A — Justice of the Peace Court and Magistrates\' Court",
            "B — Centre Court and Crown Court",
            "C — Justice of the Peace Court and Crown Court",
            "D — Crown Court and Magistrates\' Court"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 In England, Wales and Northern Ireland, minor criminal cases are dealt with in a Magistrates\' Court. In Scotland, they go to a Justice of the Peace Court.\n\n"
            "🇷🇺 *Перевод:* Мелкие уголовные дела: суд мировых судей (Англия/Уэльс/СИ) и суд мирового судьи (Шотландия)."
        ),
    },
    {
        "question": "Once you are aged 17, which TWO vehicles can you learn to drive?",
        "translation": "🇷🇺 С 17 лет на каких ДВУХ транспортных средствах можно учиться ездить?",
        "options": [
            "A — Car and fire engine",
            "B — Motor cycle and fire engine",
            "C — Motor cycle and heavy goods vehicle",
            "D — Motor cycle and car"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 In the UK, you must be at least 17 years old to drive a car or motor cycle and must have a driving licence to drive on public roads.\n\n"
            "🇷🇺 *Перевод:* В UK с 17 лет можно учиться водить автомобиль или мотоцикл при наличии водительского удостоверения."
        ),
    },
    ],
    8: [
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Most shops in the UK open seven days a week.",
            "B — All shops in the UK close on Sundays."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Most shops in the UK open seven days a week, although trading hours on Sundays and public holidays are generally reduced.\n\n"
            "🇷🇺 *Перевод:* Большинство магазинов работают 7 дней в неделю, хотя в воскресенье часы работы сокращены."
        ),
    },
    {
        "question": "Which of these is a fundamental principle of British life?",
        "translation": "🇷🇺 Какой из этих принципов является основополагающим в британской жизни?",
        "options": [
            "A — Actively supporting your local football team",
            "B — Participation in community life",
            "C — Ignoring your neighbours",
            "D — Eating fish on a Friday"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Participation in community life is one of the fundamental values and principles which all those living in the UK should respect.\n\n"
            "🇷🇺 *Перевод:* Участие в жизни общества — один из основных принципов для всех живущих в UK."
        ),
    },
    {
        "question": "Who were the suffragettes?",
        "translation": "🇷🇺 Кто такие суфражистки?",
        "options": [
            "A — Women who left the UK to live in America",
            "B — Women who campaigned for women\'s votes",
            "C — Women who left their jobs when they got married",
            "D — Women who stayed at home to raise a family"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 In the late 19th and early 20th centuries, women campaigned for women\'s rights, in particular the right to vote. They became known as suffragettes.\n\n"
            "🇷🇺 *Перевод:* Суфражистки — женщины, боровшиеся за права женщин, особенно за право голоса."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Members of Parliament (MPs) are elected through a system called first past the post.",
            "B — MPs are elected through a system called proportional representation."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 MPs are elected through a system called first past the post — the candidate who gets the most votes is elected.\n\n"
            "🇷🇺 *Перевод:* Депутаты избираются по системе «первый к финишу» — побеждает кандидат с наибольшим числом голосов."
        ),
    },
    {
        "question": "Which TWO of the following are responsibilities of Members of Parliament (MPs)?",
        "translation": "🇷🇺 Какие ДВЕ из следующих обязанностей возложены на депутатов Парламента?",
        "options": [
            "A — Representing everyone in their constituency and supporting the government on all decisions",
            "B — Scrutinising what the government is doing and representing only those who voted for them",
            "C — Scrutinising what the government is doing and supporting the government on all decisions",
            "D — Representing everyone in their constituency and scrutinising what the government is doing"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 MPs represent everyone in their constituency and scrutinise and comment on what the government is doing.\n\n"
            "🇷🇺 *Перевод:* Депутаты представляют всех избирателей своего округа и контролируют действия правительства."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — National parks are areas of protected countryside that everyone can visit.",
            "B — National parks are national sports stadiums for people to hold sporting events."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 National parks are areas of protected countryside that everyone can visit, and where people live, work and look after the landscape.\n\n"
            "🇷🇺 *Перевод:* Национальные парки — охраняемые природные территории, открытые для всех. В UK их 15."
        ),
    },
    {
        "question": "TRUE or FALSE?\nNorthern Ireland and Scotland have their own banknotes.",
        "translation": "🇷🇺 Верно или нет?\nСеверная Ирландия и Шотландия имеют собственные банкноты.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Northern Ireland and Scotland have their own banknotes, which are valid everywhere in the UK.\n\n"
            "🇷🇺 *Перевод:* Северная Ирландия и Шотландия имеют собственные банкноты, действительные по всему UK."
        ),
    },
    {
        "question": "When you arrive at a polling station, the staff will ask for which of the following?",
        "translation": "🇷🇺 Что попросят предъявить при прибытии на избирательный участок?",
        "options": [
            "A — Photocopy of your passport",
            "B — Name, address and photo ID",
            "C — Life in the UK test certificate",
            "D — National Insurance number"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 When you arrive at the polling station, the staff will ask for your name, address and photo ID.\n\n"
            "🇷🇺 *Перевод:* На избирательном участке попросят назвать имя, адрес и предъявить удостоверение личности с фото."
        ),
    },
    {
        "question": "TRUE or FALSE?\nOn average, boys in the UK leave school with better qualifications than girls.",
        "translation": "🇷🇺 Верно или нет?\nВ среднем мальчики в UK заканчивают школу с лучшими оценками, чем девочки.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 On average, girls leave school with better qualifications than boys. Also, more women than men study at university.\n\n"
            "🇷🇺 *Перевод:* В среднем девочки заканчивают школу с лучшими оценками. Женщин в университетах больше, чем мужчин."
        ),
    },
    {
        "question": "Which of the following was Isambard Kingdom Brunel famous for building?",
        "translation": "🇷🇺 Чем знаменит Изамбард Кингдом Брюнель?",
        "options": [
            "A — Motor cars",
            "B — Aeroplanes",
            "C — Bridges",
            "D — Skyscrapers"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Isambard Kingdom Brunel was a famous Victorian engineer who built railway lines, bridges, tunnels and ships.\n\n"
            "🇷🇺 *Перевод:* Брюнель — знаменитый инженер эпохи Виктории, строивший железные дороги, мосты, туннели и корабли."
        ),
    },
    {
        "question": "Which TWO of the following do you have to pay tax on?",
        "translation": "🇷🇺 С каких ДВУХ источников нужно платить налог?",
        "options": [
            "A — Income from property, savings and dividends, and small amounts of money given as a gift",
            "B — Income from property, savings and dividends, and shopping vouchers given by family",
            "C — Profits from self-employment, and income from property, savings and dividends",
            "D — Profits from self-employment, and shopping vouchers given by family"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 People in the UK pay tax on profits from self-employment, and income from property, savings and dividends.\n\n"
            "🇷🇺 *Перевод:* Налог платится с прибыли от самозанятости и доходов от собственности, сбережений и дивидендов."
        ),
    },
    {
        "question": "TRUE or FALSE?\nPantomimes are plays based on fairy stories.",
        "translation": "🇷🇺 Верно или нет?\nПантомимы — это пьесы, основанные на сказках.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Pantomime plays are a British tradition. They are based on fairy stories and are light-hearted plays with music and comedy.\n\n"
            "🇷🇺 *Перевод:* Пантомимы — британская традиция, основанная на сказках, с музыкой и комедией."
        ),
    },
    {
        "question": "What must police officers do?",
        "translation": "🇷🇺 Что обязаны делать сотрудники полиции?",
        "options": [
            "A — Be rude and abusive",
            "B — Obey the law",
            "C — Make a false statement",
            "D — Commit racial discrimination"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Police officers must obey the law. They must not be rude or abusive, make a false statement, misuse their authority, or commit racial discrimination.\n\n"
            "🇷🇺 *Перевод:* Полицейские обязаны соблюдать закон и не должны быть грубыми, делать ложные заявления или дискриминировать."
        ),
    },
    {
        "question": "Why was the Magna Carta important?",
        "translation": "🇷🇺 Почему Великая хартия вольностей была важна?",
        "options": [
            "A — It gave all men the vote.",
            "B — It restricted the power of the monarch.",
            "C — It established a system of free education.",
            "D — It gave women legal rights."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 King John was forced to agree to the Magna Carta, which restricted the king\'s power to collect taxes or to make or change laws.\n\n"
            "🇷🇺 *Перевод:* Великая хартия вольностей ограничила власть короля собирать налоги и издавать законы."
        ),
    },
    {
        "question": "By joining a political party, what TWO activities might you be involved in?",
        "translation": "🇷🇺 Вступив в политическую партию, в каких ДВУХ видах деятельности можно участвовать?",
        "options": [
            "A — Violent clashes with other parties, and handing out leaflets in the street",
            "B — Joining your MP for sessions in the House of Commons, and handing out leaflets",
            "C — Handing out leaflets in the street, and knocking on people\'s doors asking for support",
            "D — Joining your MP in the House of Commons, and knocking on doors asking for support"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Political party members work to persuade people to vote — by handing out leaflets or knocking on doors. This is called canvassing.\n\n"
            "🇷🇺 *Перевод:* Члены партии агитируют избирателей: раздают листовки и стучатся в двери. Это называется канвассинг."
        ),
    },
    {
        "question": "TRUE or FALSE?\nIn the UK, there are now a record number of people aged 85 and over.",
        "translation": "🇷🇺 Верно или нет?\nВ UK сейчас рекордное число людей в возрасте 85 лет и старше.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 People in the UK are living longer than ever before. There are now a record number of people aged 85 and over.\n\n"
            "🇷🇺 *Перевод:* Жители UK живут дольше, чем когда-либо. Число людей старше 85 лет достигло рекорда."
        ),
    },
    {
        "question": "Which TWO of these figures were great Scottish thinkers of the Enlightenment?",
        "translation": "🇷🇺 Кто из перечисленных ДВОЕ был великими шотландскими мыслителями эпохи Просвещения?",
        "options": [
            "A — Robert Louis Stevenson and David Hume",
            "B — Adam Smith and David Hume",
            "C — Robert Burns and Robert Louis Stevenson",
            "D — Robert Burns and David Hume"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Adam Smith developed ideas about economics. David Hume wrote about human nature. Both were great Scottish Enlightenment thinkers.\n\n"
            "🇷🇺 *Перевод:* Адам Смит — экономика. Дэвид Юм — природа человека. Оба — великие шотландские мыслители Просвещения."
        ),
    },
    {
        "question": "TRUE or FALSE?\nMargaret Thatcher was the longest-serving UK Prime Minister of the 20th century.",
        "translation": "🇷🇺 Верно или нет?\nМаргарет Тэтчер была самым долгослужащим премьер-министром UK в 20 веке.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Margaret Thatcher was the longest-serving Prime Minister of the 20th century. She won her first General Election in 1979 and left office in 1990.\n\n"
            "🇷🇺 *Перевод:* Тэтчер — самый долгослужащий премьер 20 века. Победила на выборах в 1979 году, ушла в 1990-м."
        ),
    },
    {
        "question": "During which period did agriculture and the manufacturing of goods become mechanised?",
        "translation": "🇷🇺 В какой период сельское хозяйство и производство товаров стали механизированными?",
        "options": [
            "A — The Glorious Revolution",
            "B — The Industrial Revolution",
            "C — The Middle Ages",
            "D — The Bronze Age"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Industrial Revolution was the rapid development of industry in Britain in the 18th and 19th centuries. Agriculture and manufacturing became mechanised.\n\n"
            "🇷🇺 *Перевод:* Промышленная революция 18–19 веков — период механизации сельского хозяйства и производства."
        ),
    },
    {
        "question": "In 1999, what happened to hereditary peers in the House of Lords?",
        "translation": "🇷🇺 Что произошло с наследственными пэрами в Палате лордов в 1999 году?",
        "options": [
            "A — Their numbers were greatly increased.",
            "B — Their salaries were stopped.",
            "C — Women were allowed to inherit their titles.",
            "D — They lost their automatic right to attend the House of Lords."
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Since 1999, hereditary peers have lost the automatic right to attend the House of Lords. They now elect a few of their number to represent them.\n\n"
            "🇷🇺 *Перевод:* С 1999 года наследственные пэры утратили автоматическое право заседать в Палате лордов."
        ),
    },
    {
        "question": "TRUE or FALSE?\nPressure and lobby groups try to influence government policy.",
        "translation": "🇷🇺 Верно или нет?\nГруппы давления и лоббисты стараются влиять на государственную политику.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Pressure and lobby groups are organisations which try to influence government policy. They play an important role in politics.\n\n"
            "🇷🇺 *Перевод:* Группы давления и лоббисты влияют на государственную политику и играют важную роль."
        ),
    },
    {
        "question": "What is one of the roles of school governors?",
        "translation": "🇷🇺 Какова одна из ролей управляющих школой (school governors)?",
        "options": [
            "A — Setting the strategic direction of the school",
            "B — Marking students\' homework",
            "C — Giving teachers ideas for lesson plans",
            "D — Serving food and drink in the canteen"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 School governors have an important part to play in raising school standards, including setting the strategic direction of the school.\n\n"
            "🇷🇺 *Перевод:* Управляющие школой помогают повышать стандарты, в том числе определяют стратегическое направление школы."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Several British writers have won the Nobel Prize in Literature.",
            "B — No British writer has won the Nobel Prize in Literature."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Several British writers have won the Nobel Prize in Literature, including Sir William Golding, Seamus Heaney and Harold Pinter.\n\n"
            "🇷🇺 *Перевод:* Нобелевскую премию по литературе получили Уильям Голдинг, Шеймас Хини и Гарольд Пинтер."
        ),
    },
    {
        "question": "Which parts of the United Kingdom have devolved governments?",
        "translation": "🇷🇺 Какие части Соединённого Королевства имеют девolved (переданные) правительства?",
        "options": [
            "A — England and Wales",
            "B — Wales, England and Northern Ireland",
            "C — Only Northern Ireland",
            "D — Wales, Scotland and Northern Ireland"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Some powers have been devolved from central government to give people in Wales, Scotland and Northern Ireland more control over matters that directly affect them.\n\n"
            "🇷🇺 *Перевод:* Уэльс, Шотландия и Северная Ирландия имеют собственные девольвированные правительства."
        ),
    },
    ],
    9: [
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Mary, Queen of Scots was a Catholic.",
            "B — Mary, Queen of Scots was a Protestant."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The queen of Scotland, Mary Stuart (often called Mary, Queen of Scots) was a Catholic.\n\n"
            "🇷🇺 *Перевод:* Мария, королева Шотландии — была католичкой."
        ),
    },
    {
        "question": "How often does Prime Minister\'s Questions occur when Parliament is sitting?",
        "translation": "🇷🇺 Как часто проходят Вопросы к премьер-министру во время сессии Парламента?",
        "options": [
            "A — Every day",
            "B — Twice a week",
            "C — Once a week",
            "D — Once a month"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Prime Minister\'s Questions takes place every week while Parliament is sitting.\n\n"
            "🇷🇺 *Перевод:* Вопросы к премьер-министру проходят каждую неделю во время сессии Парламента."
        ),
    },
    {
        "question": "Which TWO of the following are recent British film actors that have won Oscars?",
        "translation": "🇷🇺 Кто из следующих ДВУХ — британские актёры, недавно получившие Оскар?",
        "options": [
            "A — Tilda Swinton and Jayne Torvill",
            "B — Colin Firth and Robert Louis Stevenson",
            "C — Jayne Torvill and Colin Firth",
            "D — Tilda Swinton and Colin Firth"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Recent British actors to have won Oscars include Colin Firth, Sir Anthony Hopkins, Dame Judi Dench, Kate Winslet and Tilda Swinton.\n\n"
            "🇷🇺 *Перевод:* Британские актёры с Оскаром: Колин Фёрт, Энтони Хопкинс, Джуди Денч, Кейт Уинслет, Тильда Суинтон."
        ),
    },
    {
        "question": "Who was given the title of Lord Protector in the 17th century?",
        "translation": "🇷🇺 Кому был присвоен титул лорда-протектора в 17 веке?",
        "options": [
            "A — King Charles II",
            "B — Samuel Pepys",
            "C — Oliver Cromwell",
            "D — Isaac Newton"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Oliver Cromwell was given the title of Lord Protector and ruled until his death in 1658.\n\n"
            "🇷🇺 *Перевод:* Оливер Кромвель получил титул лорда-протектора и правил до своей смерти в 1658 году."
        ),
    },
    {
        "question": "The term D-Day refers to which event in British history?",
        "translation": "🇷🇺 С каким событием в британской истории связан термин «День Д»?",
        "options": [
            "A — The Battle of Trafalgar",
            "B — Landing of allied troops in Normandy",
            "C — Dropping of the atom bomb on Japan",
            "D — End of the war in Europe in 1945"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 On 6 June 1944 (D-Day), allied forces landed in Normandy. Following victory there, they pressed through France and into Germany.\n\n"
            "🇷🇺 *Перевод:* 6 июня 1944 года — высадка союзных войск в Нормандии. Затем продвижение через Францию в Германию."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Proceedings in Parliament cannot be reported in the press.",
            "B — Proceedings in Parliament are broadcast on television."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Proceedings in Parliament are broadcast on television and published in official reports called Hansard.\n\n"
            "🇷🇺 *Перевод:* Заседания Парламента транслируются по телевидению и публикуются в официальных отчётах Hansard."
        ),
    },
    {
        "question": "Which TWO foods are associated with England?",
        "translation": "🇷🇺 Какие ДВА блюда ассоциируются с Англией?",
        "options": [
            "A — Ulster fry and roast beef",
            "B — Haggis and roast beef",
            "C — Roast beef, and fish and chips",
            "D — Haggis and Ulster fry"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Roast beef is served with potatoes, vegetables and Yorkshire puddings. Fish and chips are also popular in England.\n\n"
            "🇷🇺 *Перевод:* Ростбиф с йоркширским пудингом и рыба с жареным картофелем — традиционные английские блюда."
        ),
    },
    {
        "question": "Which jubilee did Queen Elizabeth II celebrate in 2012?",
        "translation": "🇷🇺 Какой юбилей отпраздновала королева Елизавета II в 2012 году?",
        "options": [
            "A — Platinum Jubilee (70 years as Queen)",
            "B — Diamond Jubilee (60 years as Queen)",
            "C — Silver Jubilee (25 years as Queen)",
            "D — Golden Jubilee (50 years as Queen)"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Queen Elizabeth II reigned from 1952 until her death in 2022. In 2012 she celebrated her Diamond Jubilee — 60 years as Queen.\n\n"
            "🇷🇺 *Перевод:* В 2012 году Елизавета II отпраздновала Бриллиантовый юбилей — 60 лет на троне."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Rugby was introduced to ancient Britain by Viking invaders.",
            "B — Rugby originated in England in the early 19th century."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Rugby originated in England in the early 19th century and is a very popular sport in the UK today.\n\n"
            "🇷🇺 *Перевод:* Регби возникло в Англии в начале 19 века и сегодня очень популярно в UK."
        ),
    },
    {
        "question": "Which queen is remembered for fighting against the Romans?",
        "translation": "🇷🇺 Какая королева известна своей борьбой против римлян?",
        "options": [
            "A — Elizabeth",
            "B — Boudicca",
            "C — Victoria",
            "D — Anne"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Boudicca was the queen of the Iceni in what is now eastern England. She fought against the Romans and is remembered with a statue on Westminster Bridge.\n\n"
            "🇷🇺 *Перевод:* Боудикка — королева иценов, сражавшаяся против римлян. Её статуя стоит на мосту Вестминстер."
        ),
    },
    {
        "question": "Which TWO of the following are Christian groups?",
        "translation": "🇷🇺 Какие ДВЕ из следующих групп являются христианскими?",
        "options": [
            "A — Roman Catholics and Baptists",
            "B — Hindus and Baptists",
            "C — Roman Catholics and Sikhs",
            "D — Roman Catholics and Buddhists"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Roman Catholics and Baptists are Christian groups. Baptists are a Protestant group. Other Protestant groups include the Church of England, Methodists, Presbyterians and Quakers.\n\n"
            "🇷🇺 *Перевод:* Католики и баптисты — христианские группы. Баптисты — протестанты."
        ),
    },
    {
        "question": "TRUE or FALSE?\nWhen Queen Anne died in 1714, parliament chose a German to be the next king.",
        "translation": "🇷🇺 Верно или нет?\nКогда королева Анна умерла в 1714 году, парламент выбрал немца следующим королём.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Queen Anne had no surviving children, so Parliament chose George I — a German — because he was Anne\'s nearest Protestant relative.\n\n"
            "🇷🇺 *Перевод:* У Анны не было детей, поэтому парламент выбрал Георга I — немца, ближайшего протестантского родственника."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — There is a yearly sailing race on the River Thames between Oxford and Cambridge Universities.",
            "B — There is a yearly rowing race on the River Thames between Oxford and Cambridge Universities."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 There is a popular yearly rowing race on the River Thames between Oxford and Cambridge Universities.\n\n"
            "🇷🇺 *Перевод:* Ежегодная гребная гонка по Темзе между Оксфордом и Кембриджем — популярное событие."
        ),
    },
    {
        "question": "TRUE or FALSE?\nYou can support your local community by becoming a school governor.",
        "translation": "🇷🇺 Верно или нет?\nВы можете поддержать местное сообщество, став управляющим школой.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 School governors are people from the local community who wish to make a positive contribution to children\'s education.\n\n"
            "🇷🇺 *Перевод:* Управляющие школой — жители местного сообщества, вносящие вклад в образование детей."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Richard Arkwright developed new farming methods in the UK.",
            "B — Richard Arkwright ran efficient and profitable factories."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Richard Arkwright is remembered for the efficient and profitable way that he ran his factories.\n\n"
            "🇷🇺 *Перевод:* Ричард Аркрайт известен эффективным и прибыльным управлением своими фабриками."
        ),
    },
    {
        "question": "What do Sir William Golding, Seamus Heaney and Harold Pinter have in common?",
        "translation": "🇷🇺 Что общего у Уильяма Голдинга, Шеймаса Хини и Гарольда Пинтера?",
        "options": [
            "A — They were all famous British athletes.",
            "B — They all became Prime Minister.",
            "C — They were part of the first British expedition to the North Pole.",
            "D — They have all won the Nobel Prize in Literature."
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Several British writers, including the novelist Sir William Golding, the poet Seamus Heaney, and the playwright Harold Pinter, have won the Nobel Prize in Literature.\n\n"
            "🇷🇺 *Перевод:* Голдинг, Хини и Пинтер — британские лауреаты Нобелевской премии по литературе."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The UK offers its citizens and permanent residents freedom of speech.",
            "B — The UK does not allow citizens or permanent residents to voice opinions publicly."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The UK offers citizens and permanent residents various freedoms and rights, including freedom of speech.\n\n"
            "🇷🇺 *Перевод:* UK предоставляет гражданам и постоянным резидентам свободу слова и другие права."
        ),
    },
    {
        "question": "Which part of the UK is associated with Robert Burns (1759–96)?",
        "translation": "🇷🇺 С какой частью UK связан Роберт Бёрнс (1759–1796)?",
        "options": [
            "A — England",
            "B — Scotland",
            "C — Wales",
            "D — Northern Ireland"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Robert Burns is associated with Scotland. He was a poet and one of his best-known works is the song Auld Lang Syne.\n\n"
            "🇷🇺 *Перевод:* Роберт Бёрнс — шотландский поэт. Его известнейшее произведение — песня Auld Lang Syne."
        ),
    },
    {
        "question": "TRUE or FALSE?\nHereditary peers have the automatic right to attend the House of Lords.",
        "translation": "🇷🇺 Верно или нет?\nНаследственные пэры имеют автоматическое право заседать в Палате лордов.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 Since 1999, hereditary peers have lost the automatic right to attend the House of Lords. They now elect a few of their number to represent them.\n\n"
            "🇷🇺 *Перевод:* С 1999 года наследственные пэры утратили автоматическое право заседать в Палате лордов."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Sake Dean Mahomet is famous for introducing tea-drinking and bungalows to Britain from India.",
            "B — Sake Dean Mahomet is famous for introducing curry houses to Britain from India."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Sake Dean Mahomet (1759–1851) opened the first curry house in Britain in 1810.\n\n"
            "🇷🇺 *Перевод:* Саке Дин Махомет открыл первый ресторан индийской кухни в Британии в 1810 году."
        ),
    },
    {
        "question": "The term suffragettes is associated with which group of people?",
        "translation": "🇷🇺 С какой группой людей связан термин «суфражистки»?",
        "options": [
            "A — Men",
            "B — Women",
            "C — Children",
            "D — Migrants"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Women who campaigned for greater rights and the right to vote formed the women\'s suffrage movement and became known as suffragettes.\n\n"
            "🇷🇺 *Перевод:* Суфражистки — женщины, боровшиеся за права женщин и право голоса."
        ),
    },
    {
        "question": "Which TWO of the following were famous Victorians?",
        "translation": "🇷🇺 Кто из следующих ДВУХ был знаменитыми викторианцами?",
        "options": [
            "A — Isambard Kingdom Brunel and Margaret Thatcher",
            "B — Isambard Kingdom Brunel and Florence Nightingale",
            "C — Margaret Thatcher and Dylan Thomas",
            "D — Margaret Thatcher and Florence Nightingale"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Isambard Kingdom Brunel was a famous Victorian engineer. Florence Nightingale is regarded as the founder of modern nursing.\n\n"
            "🇷🇺 *Перевод:* Брюнель — инженер викторианской эпохи. Флоренс Найтингейл — основатель современного сестринского дела."
        ),
    },
    {
        "question": "Which TWO of the following do pressure and lobby groups do?",
        "translation": "🇷🇺 Что делают группы давления и лобби?",
        "options": [
            "A — Organise violent protests and try to influence government policy",
            "B — Assist MPs in their constituency work and represent the views of British business",
            "C — Try to influence government policy and represent the views of British businesses",
            "D — Organise violent protests and assist MPs in their constituency work"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Pressure and lobby groups try to influence government policy and represent the views of British businesses and other interests.\n\n"
            "🇷🇺 *Перевод:* Группы давления влияют на государственную политику и представляют интересы бизнеса и других организаций."
        ),
    },
    {
        "question": "What is a fundamental principle of British life?",
        "translation": "🇷🇺 Что является основополагающим принципом британской жизни?",
        "options": [
            "A — The rule of law",
            "B — The rule of the upper classes",
            "C — The rule of the monarch",
            "D — The rule of your local Member of Parliament (MP)"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The rule of law is one of the fundamental principles of British life and democracy.\n\n"
            "🇷🇺 *Перевод:* Верховенство закона — один из основополагающих принципов британской жизни и демократии."
        ),
    },
    ],
    10: [
    {
        "question": "TRUE or FALSE?\nShakespeare was a playwright and actor.",
        "translation": "🇷🇺 Верно или нет?\nШекспир был драматургом и актёром.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Shakespeare was born in Stratford-upon-Avon. He was a playwright and actor and wrote many poems and plays.\n\n"
            "🇷🇺 *Перевод:* Шекспир родился в Стратфорде-на-Эйвоне, был драматургом и актёром."
        ),
    },
    {
        "question": "Which TWO of the following are famous British film directors?",
        "translation": "🇷🇺 Кто из следующих ДВУХ — знаменитые британские кинорежиссёры?",
        "options": [
            "A — Sir Alfred Hitchcock and Evelyn Waugh",
            "B — Evelyn Waugh and Thomas Gainsborough",
            "C — Sir Alfred Hitchcock and Sir Ridley Scott",
            "D — Evelyn Waugh and Sir Ridley Scott"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Sir Alfred Hitchcock and Sir Ridley Scott are British film directors who have had great success in the UK and internationally.\n\n"
            "🇷🇺 *Перевод:* Хичкок и Ридли Скотт — известные британские кинорежиссёры с международным успехом."
        ),
    },
    {
        "question": "TRUE or FALSE?\nSir Isaac Newton was a famous musician from the 18th century.",
        "translation": "🇷🇺 Верно или нет?\nСэр Исаак Ньютон был знаменитым музыкантом 18 века.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 Sir Isaac Newton was a famous scientist who showed how gravity applied to the whole universe.\n\n"
            "🇷🇺 *Перевод:* Ньютон — учёный, открывший закон всемирного тяготения, а не музыкант."
        ),
    },
    {
        "question": "Which TWO of the following would you contact for help on a legal matter?",
        "translation": "🇷🇺 К кому из следующих ДВУХ вы обратитесь за помощью по правовому вопросу?",
        "options": [
            "A — A solicitor and Citizens Advice",
            "B — A solicitor and a local councillor",
            "C — A local councillor and your local MP",
            "D — Citizens Advice and your local MP"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Solicitors are trained lawyers who give advice on legal matters. Citizens Advice can give you names of local solicitors and their specialisms.\n\n"
            "🇷🇺 *Перевод:* Солиситор — юрист по правовым вопросам. Citizens Advice поможет найти нужного специалиста."
        ),
    },
    {
        "question": "Which TWO new national bodies began operating in 1999?",
        "translation": "🇷🇺 Какие ДВА новых национальных органа начали работу в 1999 году?",
        "options": [
            "A — Welsh Assembly (now Senedd) and Scottish Parliament",
            "B — Scottish Parliament and English Parliament",
            "C — House of Lords and Welsh Assembly (now Senedd)",
            "D — House of Lords and Scottish Parliament"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Since 1997, powers have been devolved. There has been a Welsh Assembly (now called the Senedd) and a Scottish Parliament since 1999.\n\n"
            "🇷🇺 *Перевод:* С 1999 года работают Ассамблея Уэльса (ныне Сенедд) и Парламент Шотландии."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Sir Andy Murray is the first British man to sail around the world.",
            "B — Sir Andy Murray is the first British man to win a singles tennis title in a Grand Slam tournament since 1936."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Sir Andy Murray is a Scottish tennis player and the first British man to win a singles tennis title in a Grand Slam tournament since 1936.\n\n"
            "🇷🇺 *Перевод:* Энди Маррей — первый британец, выигравший одиночный теннисный титул на турнире Большого шлема с 1936 года."
        ),
    },
    {
        "question": "Which TWO are associated with Sir Francis Drake?",
        "translation": "🇷🇺 Что из следующего ДВУХ связано с сэром Фрэнсисом Дрейком?",
        "options": [
            "A — Defeating the Spanish Armada and early flight",
            "B — Defeating the Spanish Armada and sailing around the world",
            "C — Early flight and the Titanic",
            "D — The Titanic and sailing around the world"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Sir Francis Drake was one of the commanders who defeated the Spanish Armada. His ship, the Golden Hind, was one of the first to sail around the world.\n\n"
            "🇷🇺 *Перевод:* Дрейк участвовал в разгроме Армады и совершил одно из первых кругосветных плаваний на «Золотой лани»."
        ),
    },
    {
        "question": "Which of the following is a responsibility you will have as a citizen or permanent resident of the UK?",
        "translation": "🇷🇺 Какая из следующих обязанностей возлагается на гражданина или постоянного жителя UK?",
        "options": [
            "A — Using your car as much as possible",
            "B — Visiting your local pub regularly",
            "C — Keeping an allotment",
            "D — Looking after the area in which you live and the environment"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 There are responsibilities shared by all those living in the UK. These include looking after the area in which you live and the environment.\n\n"
            "🇷🇺 *Перевод:* Каждый житель UK обязан заботиться о своём районе и окружающей среде."
        ),
    },
    {
        "question": "Which TWO of the following are famous British authors?",
        "translation": "🇷🇺 Кто из следующих ДВУХ — знаменитые британские авторы?",
        "options": [
            "A — Gustav Holst and J K Rowling",
            "B — Sir Steve Redgrave and Sir Arthur Conan Doyle",
            "C — Sir Steve Redgrave and Gustav Holst",
            "D — Sir Arthur Conan Doyle and J K Rowling"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Sir Arthur Conan Doyle wrote stories about Sherlock Holmes. J K Rowling wrote the Harry Potter series.\n\n"
            "🇷🇺 *Перевод:* Конан Дойл — автор Шерлока Холмса. Дж. К. Роулинг — автор Гарри Поттера."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe British constitution is contained in a single written document.",
        "translation": "🇷🇺 Верно или нет?\nБританская конституция содержится в едином письменном документе.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The British constitution is not written down in any single document, and is therefore described as 'unwritten'.\n\n"
            "🇷🇺 *Перевод:* Британская конституция не записана в одном документе — она считается «неписаной»."
        ),
    },
    {
        "question": "Which TWO people are famous UK sports stars?",
        "translation": "🇷🇺 Кто из следующих ДВУХ — знаменитые британские спортсмены?",
        "options": [
            "A — Sir Chris Hoy and Dame Kelly Holmes",
            "B — Lucien Freud and Jane Austen",
            "C — Dame Kelly Holmes and Jane Austen",
            "D — Sir Chris Hoy and Lucien Freud"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Sir Chris Hoy is a Scottish cyclist who won six gold Olympic medals. Dame Kelly Holmes won two gold medals for running in the 2004 Olympics.\n\n"
            "🇷🇺 *Перевод:* Крис Хой — велогонщик, 6 золотых медалей. Келли Холмс — бегунья, 2 золота на Олимпиаде 2004 года."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The first person to use the title Prime Minister was Sir Robert Walpole.",
            "B — The first person to use the title Prime Minister was Sir Christopher Wren."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Sir Robert Walpole was the first person to be called Prime Minister. He served from 1721 until 1742.\n\n"
            "🇷🇺 *Перевод:* Сэр Роберт Уолпол — первый премьер-министр, занимавший пост с 1721 по 1742 год."
        ),
    },
    {
        "question": "Why is Sir Edwin Lutyens famous?",
        "translation": "🇷🇺 Чем знаменит сэр Эдвин Лаченс?",
        "options": [
            "A — He won a gold medal at the London 2012 Olympic Games.",
            "B — He was the first UK Prime Minister.",
            "C — He invented the World Wide Web.",
            "D — He was a 20th-century architect."
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Sir Edwin Lutyens was a famous 20th-century architect who designed the Cenotaph in Whitehall.\n\n"
            "🇷🇺 *Перевод:* Лаченс — знаменитый архитектор 20 века, спроектировавший Кенотаф на Уайтхолле."
        ),
    },
    {
        "question": "TRUE or FALSE?\nSir Mo Farah and Dame Jessica Ennis-Hill are well-known athletes who won gold medals at the 2012 London Olympics.",
        "translation": "🇷🇺 Верно или нет?\nМо Фара и Джессика Эннис-Хилл — спортсмены, выигравшие золото на Олимпиаде 2012 года в Лондоне.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Sir Mo Farah won gold in the 5,000 and 10,000 metres. Dame Jessica Ennis-Hill won gold in the heptathlon.\n\n"
            "🇷🇺 *Перевод:* Фара — золото на 5000 и 10000 м. Эннис-Хилл — золото в семиборье. Оба на Олимпиаде 2012 года."
        ),
    },
    {
        "question": "What did St Augustine and St Columba do during the Anglo-Saxon period?",
        "translation": "🇷🇺 Что сделали Св. Августин и Св. Колумба в эпоху англосаксов?",
        "options": [
            "A — They invented new farming techniques.",
            "B — They led an uprising in Wales.",
            "C — They helped to spread Christianity across Britain.",
            "D — They fought courageously against the Romans."
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 St Columba founded a monastery on Iona. St Augustine spread Christianity in the south and became the first Archbishop of Canterbury.\n\n"
            "🇷🇺 *Перевод:* Колумба основал монастырь на Ионе. Августин распространил христианство на юге и стал первым архиепископом Кентерберийским."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Chancellor of the Exchequer is responsible for crime, policing and immigration.",
            "B — The Chancellor of the Exchequer is responsible for the economy."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Chancellor of the Exchequer is the cabinet minister responsible for the economy.\n\n"
            "🇷🇺 *Перевод:* Канцлер казначейства — министр, ответственный за экономику страны."
        ),
    },
    {
        "question": "TRUE or FALSE?\nIn the 1830s and 1840s a group called the Chartists campaigned for reform to the voting system.",
        "translation": "🇷🇺 Верно или нет?\nВ 1830–1840-х годах группа чартистов выступала за реформу избирательной системы.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The Chartists campaigned for voting reform, including elections every year and equal electoral regions.\n\n"
            "🇷🇺 *Перевод:* Чартисты требовали ежегодных выборов и равного представительства регионов."
        ),
    },
    {
        "question": "Which of the following is a Stone Age monument in the UK?",
        "translation": "🇷🇺 Какой из следующих объектов является памятником каменного века в UK?",
        "options": [
            "A — Globe Theatre",
            "B — Nelson\'s Column",
            "C — Stonehenge",
            "D — Windsor Castle"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Stonehenge is a Stone Age monument in Wiltshire. It was probably a special gathering place for seasonal ceremonies.\n\n"
            "🇷🇺 *Перевод:* Стоунхендж — памятник каменного века в Уилтшире, вероятно использовавшийся для сезонных церемоний."
        ),
    },
    {
        "question": "TRUE or FALSE?\nSnowdonia is a national park in Northern Ireland.",
        "translation": "🇷🇺 Верно или нет?\nСноудония — национальный парк в Северной Ирландии.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 Snowdonia is a national park in North Wales. Its most well-known landmark is Snowdon, the highest mountain in Wales.\n\n"
            "🇷🇺 *Перевод:* Сноудония — национальный парк в Северном Уэльсе, а не в Северной Ирландии."
        ),
    },
    {
        "question": "Which TWO are famous gardens in the UK?",
        "translation": "🇷🇺 Какие ДВА из следующих — знаменитые сады в UK?",
        "options": [
            "A — Sissinghurst and Snowdonia",
            "B — London Eye and Sissinghurst",
            "C — London Eye and Snowdonia",
            "D — Sissinghurst and Bodnant Garden"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 Sissinghurst is in England and Bodnant Garden is in Wales.\n\n"
            "🇷🇺 *Перевод:* Сиссингхёрст — в Англии, сад Боднант — в Уэльсе."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The \'Swinging Sixties\' was a period of religious change.",
            "B — The \'Swinging Sixties\' was a period of social change."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The 1960s was a period of significant social change, known as the 'Swinging Sixties'. There was growth in fashion, cinema and popular music.\n\n"
            "🇷🇺 *Перевод:* «Свингующие шестидесятые» — эпоха социальных перемен: мода, кино, поп-музыка."
        ),
    },
    {
        "question": "Which TWO groups were associated with King Charles I and Parliament during the English Civil War?",
        "translation": "🇷🇺 Какие ДВЕ группы были связаны с Карлом I и Парламентом во время Гражданской войны?",
        "options": [
            "A — Tories and Roundheads",
            "B — Cavaliers and Luddites",
            "C — Roundheads and Cavaliers",
            "D — Roundheads and Luddites"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Supporters of the King were known as Cavaliers and supporters of Parliament were known as Roundheads.\n\n"
            "🇷🇺 *Перевод:* Кавалеры поддерживали короля, Круглоголовые — Парламент."
        ),
    },
    {
        "question": "St Andrew is the patron saint of which country?",
        "translation": "🇷🇺 Святой Андрей — покровитель какой страны?",
        "options": [
            "A — England",
            "B — Scotland",
            "C — Wales",
            "D — Northern Ireland"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 St Andrew is the patron saint of Scotland, celebrated on 30 November each year.\n\n"
            "🇷🇺 *Перевод:* Святой Андрей — покровитель Шотландии. День отмечается 30 ноября."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Plymouth, Norwich and Leeds are cities in England.",
            "B — Newport, Swansea and Cardiff are cities in Scotland."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Plymouth, Norwich and Leeds are cities in England. Newport, Swansea and Cardiff are cities in Wales.\n\n"
            "🇷🇺 *Перевод:* Плимут, Норидж и Лидс — города Англии. Ньюпорт, Суонси и Кардифф — города Уэльса."
        ),
    },
    ],
    11: [
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Sir Steve Redgrave is a famous rower who won gold medals in five consecutive Olympic Games.",
            "B — Sir Steve Redgrave is a famous film actor who has won several BAFTAs."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Sir Steve Redgrave won gold medals in rowing in five consecutive Olympic Games and is one of Britain\'s greatest Olympians.\n\n"
            "🇷🇺 *Перевод:* Стив Редгрейв — гребец, выигравший золото на пяти Олимпиадах подряд."
        ),
    },
    {
        "question": "Which TWO values are upheld by the Commonwealth association of countries?",
        "translation": "🇷🇺 Какие ДВЕ ценности отстаивает Содружество наций?",
        "options": [
            "A — Democracy and rule of law",
            "B — Violence and rule of law",
            "C — Democracy and communism",
            "D — Communism and rule of law"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Commonwealth is based on the core values of democracy, good government and the rule of law.\n\n"
            "🇷🇺 *Перевод:* Содружество основано на ценностях демократии, хорошего управления и верховенства закона."
        ),
    },
    {
        "question": "Which TWO are 20th-century British inventions?",
        "translation": "🇷🇺 Какие ДВА из следующих — британские изобретения 20 века?",
        "options": [
            "A — The World Wide Web and the diesel engine",
            "B — Television and the World Wide Web",
            "C — Mobile phones and the diesel engine",
            "D — Television and mobile phones"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Television was developed by John Logie Baird in the 1920s. Tim Berners-Lee invented the World Wide Web in 1990.\n\n"
            "🇷🇺 *Перевод:* Телевидение — Джон Лоуги Бэрд (1920-е). Всемирная паутина — Тим Бернерс-Ли (1990)."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Battle of Britain in 1940 was fought at sea.",
            "B — The Battle of Britain in 1940 was fought in the air."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Battle of Britain was fought in the air above Britain in 1940. The British won the crucial aerial battle against the Germans.\n\n"
            "🇷🇺 *Перевод:* Битва за Британию 1940 года велась в воздухе. Британцы выиграли решающее сражение."
        ),
    },
    {
        "question": "Which TWO issues can the devolved administrations pass laws on?",
        "translation": "🇷🇺 По каким ДВУМ вопросам деволюционные органы могут принимать законы?",
        "options": [
            "A — Health and foreign affairs",
            "B — Health and education",
            "C — Education and immigration",
            "D — Foreign affairs and immigration"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The devolved administrations in Scotland, Wales and Northern Ireland can pass laws on matters including health and education.\n\n"
            "🇷🇺 *Перевод:* Деволюционные органы могут принимать законы, в том числе в сферах здравоохранения и образования."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe Home Secretary is the government minister responsible for managing relationships with foreign countries.",
        "translation": "🇷🇺 Верно или нет?\nМинистр внутренних дел отвечает за отношения с иностранными государствами.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The Home Secretary is responsible for crime, policing and immigration. The Foreign Secretary manages relationships with foreign countries.\n\n"
            "🇷🇺 *Перевод:* МВД — полиция, преступность, иммиграция. Министр иностранных дел — отношения с другими странами."
        ),
    },
    {
        "question": "Textile and engineering firms found workers from which TWO countries after the Second World War?",
        "translation": "🇷🇺 Из каких ДВУХ стран текстильные и машиностроительные фирмы набирали рабочих после Второй мировой войны?",
        "options": [
            "A — Canada and India",
            "B — India and Pakistan",
            "C — South Africa and Pakistan",
            "D — South Africa and India"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Textile and engineering firms from the north of England and the Midlands sent agents to India and Pakistan to find workers.\n\n"
            "🇷🇺 *Перевод:* Фирмы севера Англии и Мидлендса вербовали рабочих в Индии и Пакистане."
        ),
    },
    {
        "question": "Which TWO are famous UK landmarks?",
        "translation": "🇷🇺 Какие ДВА из следующих — знаменитые достопримечательности UK?",
        "options": [
            "A — Loch Lomond and Notre Dame",
            "B — Snowdonia and Notre Dame",
            "C — Snowdonia and Loch Lomond",
            "D — Grand Canyon and Loch Lomond"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 Loch Lomond is the largest expanse of fresh water in mainland Britain. Snowdonia is a national park in North Wales.\n\n"
            "🇷🇺 *Перевод:* Лох-Ломонд — крупнейший пресноводный водоём. Сноудония — национальный парк в Северном Уэльсе."
        ),
    },
    {
        "question": "TRUE or FALSE?\nAll citizens and permanent residents of the UK can choose which laws they follow.",
        "translation": "🇷🇺 Верно или нет?\nВсе граждане и постоянные жители UK могут выбирать, какие законы соблюдать.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 There are responsibilities shared by all those living in the UK, including respecting and obeying the law.\n\n"
            "🇷🇺 *Перевод:* Все жители UK обязаны соблюдать законы — выбирать, какие из них исполнять, нельзя."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe House of Lords always acts as the government wishes.",
        "translation": "🇷🇺 Верно или нет?\nПалата лордов всегда действует так, как хочет правительство.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The House of Lords is normally more independent of the government than the House of Commons.\n\n"
            "🇷🇺 *Перевод:* Палата лордов обычно более независима от правительства, чем Палата общин."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Cricket matches can last up to five days.",
            "B — Cricket matches can last up to two weeks."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Some cricket games can last for up to five days and still result in a draw.\n\n"
            "🇷🇺 *Перевод:* Некоторые матчи по крикету длятся до пяти дней и всё равно могут завершиться ничьей."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe main political parties actively look for members of the public to help at elections and contribute to their costs.",
        "translation": "🇷🇺 Верно или нет?\nОсновные политические партии активно ищут общественных помощников и взносы на выборы.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The main political parties actively look for members of the public to join debates, contribute to costs, and help at elections.\n\n"
            "🇷🇺 *Перевод:* Партии приглашают граждан участвовать в дискуссиях, делать взносы и помогать на выборах."
        ),
    },
    {
        "question": "What type of government was formed after the General Election of 2010?",
        "translation": "🇷🇺 Какое правительство было сформировано после всеобщих выборов 2010 года?",
        "options": [
            "A — National",
            "B — All-party",
            "C — One-party",
            "D — Coalition"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The 2010 coalition was formed by the Conservative and Liberal Democrat parties. David Cameron became Prime Minister.\n\n"
            "🇷🇺 *Перевод:* В 2010 году консерваторы и либерал-демократы образовали коалицию. Дэвид Кэмерон стал премьером."
        ),
    },
    {
        "question": "TRUE or FALSE?\nIn 1707 the kingdoms of England and Scotland were united.",
        "translation": "🇷🇺 Верно или нет?\nВ 1707 году королевства Англии и Шотландии объединились.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The Act of Union (Treaty of Union in Scotland) was agreed in 1707 and created the Kingdom of Great Britain.\n\n"
            "🇷🇺 *Перевод:* Акт об унии 1707 года объединил Англию и Шотландию в Королевство Великобритания."
        ),
    },
    {
        "question": "Which TWO are political parties in the UK?",
        "translation": "🇷🇺 Какие ДВЕ из следующих — политические партии UK?",
        "options": [
            "A — Modern Party and Conservative Party",
            "B — Office Party and Labour Party",
            "C — Modern Party and Labour Party",
            "D — Conservative Party and Labour Party"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The major political parties in the UK include the Conservative Party, the Labour Party and the Liberal Democrats.\n\n"
            "🇷🇺 *Перевод:* Крупнейшие партии UK: Консервативная, Лейбористская и Либерал-демократы."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Anglo-Saxon kingdoms in England united under King Alfred the Great.",
            "B — The Anglo-Saxon kingdoms in England united under King Kenneth MacAlpin."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Anglo-Saxon kingdoms in England united under King Alfred the Great, who defeated the Vikings.\n\n"
            "🇷🇺 *Перевод:* Англосаксонские королевства объединились под властью Альфреда Великого, победившего викингов."
        ),
    },
    {
        "question": "TRUE or FALSE?\nWales, Scotland and Northern Ireland each have devolved administrations which give them total control over all policies and laws.",
        "translation": "🇷🇺 Верно или нет?\nУэльс, Шотландия и Северная Ирландия имеют полный контроль над всеми законами и политиками.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 Some powers have been devolved, but some policies and laws remain under central UK government control.\n\n"
            "🇷🇺 *Перевод:* Часть полномочий передана регионам, но часть законов и политик остаётся под контролем центрального правительства."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Decisions on government policies are made by the monarch.",
            "B — Decisions on government policies are made by the Prime Minister and cabinet."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The monarch can advise, warn and encourage, but decisions on government policies are made by the Prime Minister and cabinet.\n\n"
            "🇷🇺 *Перевод:* Монарх может советовать, но решения принимаются премьер-министром и кабинетом."
        ),
    },
    {
        "question": "Which TWO patron saints\' days occur in March?",
        "translation": "🇷🇺 Дни каких ДВУХ покровителей отмечаются в марте?",
        "options": [
            "A — St David and St George",
            "B — St David and St Patrick",
            "C — St David and St Andrew",
            "D — St Patrick and St Andrew"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 St David\'s Day is 1 March (Wales). St Patrick\'s Day is 17 March (Northern Ireland).\n\n"
            "🇷🇺 *Перевод:* День Св. Давида — 1 марта (Уэльс). День Св. Патрика — 17 марта (Северная Ирландия)."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — All Acts of Parliament are made in the monarch\'s name.",
            "B — All Acts of Parliament are made in the Prime Minister\'s name."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The monarch is the head of state. All Acts of Parliament are made in the monarch\'s name.\n\n"
            "🇷🇺 *Перевод:* Монарх — глава государства. Все Акты Парламента принимаются от его имени."
        ),
    },
    {
        "question": "St George is the patron saint of which country?",
        "translation": "🇷🇺 Святой Георгий — покровитель какой страны?",
        "options": [
            "A — England",
            "B — Scotland",
            "C — Wales",
            "D — Northern Ireland"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 St George is the patron saint of England, celebrated on 23 April each year.\n\n"
            "🇷🇺 *Перевод:* Святой Георгий — покровитель Англии. День отмечается 23 апреля."
        ),
    },
    {
        "question": "Which area of government policy is the responsibility of the Chancellor of the Exchequer?",
        "translation": "🇷🇺 За какую сферу государственной политики отвечает канцлер казначейства?",
        "options": [
            "A — Education",
            "B — Health",
            "C — Economy",
            "D — Legal affairs"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Chancellor of the Exchequer is responsible for the economy and is a member of the cabinet.\n\n"
            "🇷🇺 *Перевод:* Канцлер казначейства отвечает за экономику и входит в состав кабинета министров."
        ),
    },
    {
        "question": "What is the name of the Northern Ireland Assembly building?",
        "translation": "🇷🇺 Как называется здание Ассамблеи Северной Ирландии?",
        "options": [
            "A — The Houses of Parliament",
            "B — The Senedd",
            "C — Stormont",
            "D — Holyrood House"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Northern Ireland Assembly building is known as Stormont.\n\n"
            "🇷🇺 *Перевод:* Здание Ассамблеи Северной Ирландии называется Сторmont (Сторmonт)."
        ),
    },
    {
        "question": "When did the Battle of Hastings take place?",
        "translation": "🇷🇺 Когда произошла битва при Гастингсе?",
        "options": [
            "A — 1066",
            "B — 1415",
            "C — 1642",
            "D — 1940"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Battle of Hastings took place in 1066. William the Conqueror defeated King Harold II.\n\n"
            "🇷🇺 *Перевод:* Битва при Гастингсе — 1066 год. Вильгельм Завоеватель победил короля Гарольда II."
        ),
    },
    ],
    12: [
    {
        "question": "What is the title of the National Anthem of the UK?",
        "translation": "🇷🇺 Как называется национальный гимн UK?",
        "options": [
            "A — Long Live the King",
            "B — God Save the King",
            "C — Long Live the Monarch",
            "D — Almighty is the King"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The National Anthem of the UK is \'God Save the King\'. It is played at important national occasions and events attended by the Royal Family.\n\n"
            "🇷🇺 *Перевод:* Гимн UK — «Боже, храни короля». Исполняется на важных государственных мероприятиях."
        ),
    },
    {
        "question": "TRUE or FALSE?\nIn the UK you are expected to treat others with fairness.",
        "translation": "🇷🇺 Верно или нет?\nВ UK от вас ожидают справедливого отношения к другим.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 There are responsibilities shared by all those living in the UK, including treating others with fairness.\n\n"
            "🇷🇺 *Перевод:* Справедливое отношение к другим — одна из обязанностей всех жителей UK."
        ),
    },
    {
        "question": "Where is the Senedd based?",
        "translation": "🇷🇺 Где находится Сенедд?",
        "options": [
            "A — London",
            "B — Newport",
            "C — Glasgow",
            "D — Cardiff"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The Senedd is based in Cardiff, the capital city of Wales.\n\n"
            "🇷🇺 *Перевод:* Сенедд находится в Кардиффе — столице Уэльса."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — There are 50 pence in a pound.",
            "B — There are 10 pence in a pound.",
            "C — There are 100 pence in a pound.",
            "D — There are 20 pence in a pound."
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The currency in the UK is the pound sterling (£). There are 100 pence in a pound.\n\n"
            "🇷🇺 *Перевод:* Валюта UK — фунт стерлингов. В одном фунте 100 пенсов."
        ),
    },
    {
        "question": "Which TWO of the following were English Civil War battles?",
        "translation": "🇷🇺 Какие ДВЕ из следующих битв были сражениями Гражданской войны в Англии?",
        "options": [
            "A — Marston Moor and Hastings",
            "B — Waterloo and Marston Moor",
            "C — Hastings and Naseby",
            "D — Marston Moor and Naseby"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The Battles of Marston Moor and Naseby were English Civil War battles.\n\n"
            "🇷🇺 *Перевод:* Битвы при Марстон-Муре и Нейзби — сражения Английской гражданской войны."
        ),
    },
    {
        "question": "How is the Speaker of the House of Commons chosen?",
        "translation": "🇷🇺 Как выбирается Спикер Палаты общин?",
        "options": [
            "A — By the monarch",
            "B — Through a public election",
            "C — In a secret ballot",
            "D — By the Prime Minister"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Speaker is chosen by other MPs in a secret ballot. The Speaker keeps order during political debates.\n\n"
            "🇷🇺 *Перевод:* Спикер избирается депутатами тайным голосованием. Он следит за порядком во время дебатов."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The BBC is primarily funded by advertising.",
            "B — The BBC is partially funded by the state."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The BBC is a British public service broadcaster. Although it receives some state funding, it is independent of the government.\n\n"
            "🇷🇺 *Перевод:* BBC — общественный вещатель, получающий частичное государственное финансирование, но независимый от правительства."
        ),
    },
    {
        "question": "The Paralympics have their origin in the work of which of the following people?",
        "translation": "🇷🇺 В работе кого из следующих людей берут начало Паралимпийские игры?",
        "options": [
            "A — Sir Roger Bannister",
            "B — Sir Ludwig Guttman",
            "C — Sir Jackie Stewart",
            "D — Sir Andy Murray"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Paralympics originated in the work of Dr Ludwig Guttman at the Stoke Mandeville Hospital. He developed new treatments for spinal injuries and encouraged sport.\n\n"
            "🇷🇺 *Перевод:* Паралимпиада берёт начало в работе д-ра Людвига Гуттмана в больнице Сток-Мандевиль."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Proms is an eight-week summer season of classical orchestral music.",
            "B — The Proms is a series of tennis matches held every June in London."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Proms is an eight-week summer season of orchestral classical music, including at the Royal Albert Hall in London.\n\n"
            "🇷🇺 *Перевод:* Promс — восьминедельный летний сезон классической оркестровой музыки, включая выступления в Ройял Альберт Холле."
        ),
    },
    {
        "question": "Which TWO are influential British bands?",
        "translation": "🇷🇺 Какие ДВЕ из следующих — влиятельные британские группы?",
        "options": [
            "A — The National Trust and The Rolling Stones",
            "B — The National Trust and The Beatles",
            "C — The Rolling Stones and The Beatles",
            "D — The Rolling Stones and The Royal Family"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Beatles and The Rolling Stones are two British bands that continue to have an influence on music both in the UK and abroad.\n\n"
            "🇷🇺 *Перевод:* The Beatles и The Rolling Stones — влиятельные британские группы с мировым признанием."
        ),
    },
    {
        "question": "St David is the patron saint of which country of the UK?",
        "translation": "🇷🇺 Святой Давид — покровитель какой страны UK?",
        "options": [
            "A — England",
            "B — Scotland",
            "C — Wales",
            "D — Northern Ireland"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 St David is the patron saint of Wales. St David\'s Day is celebrated on 1 March each year.\n\n"
            "🇷🇺 *Перевод:* Святой Давид — покровитель Уэльса. День отмечается 1 марта."
        ),
    },
    {
        "question": "The Bill of Rights of 1689 limited whose powers?",
        "translation": "🇷🇺 Чьи полномочия ограничил Билль о правах 1689 года?",
        "options": [
            "A — The king\'s",
            "B — Parliament\'s",
            "C — Judges\'",
            "D — The Church\'s"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Bill of Rights of 1689 confirmed the rights of Parliament and the limits of the king\'s power.\n\n"
            "🇷🇺 *Перевод:* Билль о правах 1689 года подтвердил права Парламента и ограничил власть короля."
        ),
    },
    {
        "question": "Who elects Police and Crime Commissioners (PCCs)?",
        "translation": "🇷🇺 Кто избирает уполномоченных по полиции и борьбе с преступностью (PCCs)?",
        "options": [
            "A — The police",
            "B — The Home Office",
            "C — The public",
            "D — Members of Parliament"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The public elects Police and Crime Commissioners (PCCs) in England and Wales. PCCs are responsible for an efficient and effective police force.\n\n"
            "🇷🇺 *Перевод:* Уполномоченных по полиции избирает общественность в Англии и Уэльсе."
        ),
    },
    {
        "question": "In which part of the British Empire did the Boer War of 1899–1902 take place?",
        "translation": "🇷🇺 В какой части Британской империи проходила Англо-бурская война (1899–1902)?",
        "options": [
            "A — India",
            "B — Canada",
            "C — Australia",
            "D — South Africa"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The Boer War took place in South Africa between the British army and the Boer settlers, who originally came from the Netherlands.\n\n"
            "🇷🇺 *Перевод:* Англо-бурская война шла в Южной Африке между британской армией и бурами — потомками нидерландских переселенцев."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The capital city of Northern Ireland is Swansea.",
            "B — The capital city of Northern Ireland is Belfast."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The capital city of Northern Ireland is Belfast.\n\n"
            "🇷🇺 *Перевод:* Столица Северной Ирландии — Белфаст."
        ),
    },
    {
        "question": "Which TWO of the following issues can the Northern Ireland Assembly make decisions on?",
        "translation": "🇷🇺 По каким ДВУМ вопросам Ассамблея Северной Ирландии может принимать решения?",
        "options": [
            "A — Defence and foreign affairs",
            "B — Agriculture and social services",
            "C — Defence and agriculture",
            "D — Foreign affairs and social services"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Northern Ireland Assembly can make decisions on various issues, including agriculture and social services.\n\n"
            "🇷🇺 *Перевод:* Ассамблея Северной Ирландии принимает решения, в том числе в сфере сельского хозяйства и социальных услуг."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The official home of the Prime Minister is 10 Downing Street.",
            "B — The official home of the Prime Minister is Buckingham Palace."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The official home of the Prime Minister is 10 Downing Street in central London. He or she also has a country house called Chequers.\n\n"
            "🇷🇺 *Перевод:* Официальная резиденция премьер-министра — Даунинг-стрит, 10. Загородная резиденция — Чекерс."
        ),
    },
    {
        "question": "At what age can you vote in a General Election in the UK?",
        "translation": "🇷🇺 С какого возраста можно голосовать на всеобщих выборах в UK?",
        "options": [
            "A — 16",
            "B — 18",
            "C — 21",
            "D — 23"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The present voting age of 18 was set in 1969.\n\n"
            "🇷🇺 *Перевод:* Возраст для голосования — 18 лет. Установлен в 1969 году."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe flower that is particularly associated with England is the rose.",
        "translation": "🇷🇺 Верно или нет?\nЦветок, особо связанный с Англией, — роза.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The countries of the UK all have flowers associated with them. In England, the flower is the rose.\n\n"
            "🇷🇺 *Перевод:* У каждой страны UK есть свой цветок-символ. В Англии — роза."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The public can listen to debates in the House of Commons.",
            "B — No member of the public is allowed to attend debates in the House of Commons."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The public can listen to debates from public galleries in both the House of Commons and the House of Lords.\n\n"
            "🇷🇺 *Перевод:* Общественность может слушать дебаты с галерей как в Палате общин, так и в Палате лордов."
        ),
    },
    {
        "question": "What was the Beveridge Report of 1942 about?",
        "translation": "🇷🇺 О чём был доклад Бевериджа 1942 года?",
        "options": [
            "A — How to end the war in Europe",
            "B — How to treat the Germans and Japanese after the war",
            "C — Establishing a welfare state",
            "D — The coalition government"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Beveridge Report recommended the government fight five \'Giant Evils\': Want, Disease, Ignorance, Squalor and Idleness — laying the basis for the modern welfare state.\n\n"
            "🇷🇺 *Перевод:* Доклад Бевериджа предложил бороться с пятью «великими злами» и стал основой современного государства всеобщего благосостояния."
        ),
    },
    {
        "question": "On which date is St Patrick\'s Day celebrated?",
        "translation": "🇷🇺 Когда отмечается День Святого Патрика?",
        "options": [
            "A — 1 March",
            "B — 17 March",
            "C — 23 April",
            "D — 30 November"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 St Patrick, the patron saint of Northern Ireland (and Ireland), has a special day on 17 March.\n\n"
            "🇷🇺 *Перевод:* День Святого Патрика — покровителя Северной Ирландии — отмечается 17 марта."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Industrial Revolution is the name given to the rapid development of industry in Britain in the 20th century.",
            "B — The Industrial Revolution is the name given to the rapid development of industry that began in the 18th century."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Industrial Revolution refers to the rapid development of industry in Britain from the mid-18th century.\n\n"
            "🇷🇺 *Перевод:* Промышленная революция — стремительное развитие промышленности Британии, начавшееся в середине 18 века."
        ),
    },
    {
        "question": "What were TWO important aspects of the Reform Act of 1832?",
        "translation": "🇷🇺 Каковы были ДВА важных аспекта Акта о реформе 1832 года?",
        "options": [
            "A — It abolished rotten boroughs and gave women the vote.",
            "B — It decreased the power of the monarch and gave women the vote.",
            "C — It greatly increased the number of people who could vote and abolished rotten boroughs.",
            "D — It increased the power of the monarch and gave women the vote."
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Reform Act of 1832 greatly increased the number of people with the right to vote and abolished pocket and rotten boroughs.\n\n"
            "🇷🇺 *Перевод:* Акт о реформе 1832 года расширил избирательное право и упразднил «гнилые местечки»."
        ),
    },
    ],
    13: [
    {
        "question": "Which TWO rights are offered by the UK to citizens and permanent residents?",
        "translation": "🇷🇺 Какие ДВА права предоставляет UK гражданам и постоянным жителям?",
        "options": [
            "A — Free groceries for everyone and a right to a fair trial",
            "B — Long lunch breaks on Friday and a right to a fair trial",
            "C — Freedom of speech and a right to a fair trial",
            "D — Freedom of speech and free groceries for everyone"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 There are responsibilities and freedoms shared by all those living in the UK. These include freedom of speech and a right to a fair trial.\n\n"
            "🇷🇺 *Перевод:* Все живущие в UK разделяют свободу слова и право на справедливый суд."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The small claims procedure is an informal way of helping people to settle minor disputes.",
            "B — The small claims procedure helps people to make small home insurance claims."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The small claims procedure is an informal way of helping people to settle minor disputes without spending a lot of time and money using a lawyer.\n\n"
            "🇷🇺 *Перевод:* Упрощённая процедура мелких исков — неформальный способ урегулировать споры без адвоката."
        ),
    },
    {
        "question": "Which of the following is the capital city of Wales?",
        "translation": "🇷🇺 Какой из следующих городов является столицей Уэльса?",
        "options": [
            "A — Swansea",
            "B — Cardiff",
            "C — Edinburgh",
            "D — Belfast"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The capital city of Wales is Cardiff.\n\n"
            "🇷🇺 *Перевод:* Столица Уэльса — Кардифф."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — It is free to visit the Houses of Parliament to listen to debates.",
            "B — It costs £15 per person to visit the Houses of Parliament to listen to debates."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The public can listen to debates from public galleries in both the House of Commons and the House of Lords. Entrance is free.\n\n"
            "🇷🇺 *Перевод:* Посещение Парламента для слушания дебатов бесплатно."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe \'Swinging Sixties\' is a reference to the 1860s.",
        "translation": "🇷🇺 Верно или нет?\n«Лихие шестидесятые» — это отсылка к 1860-м годам.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The decade of the 1960s was a period of significant social change, known as \'the Swinging Sixties\'. There was growth in British fashion, cinema and popular music.\n\n"
            "🇷🇺 *Перевод:* «Лихие шестидесятые» — это 1960-е годы, время роста британской моды, кино и поп-музыки."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The official Church of state in England is the Church of England.",
            "B — There is no official Church of state in England."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Church of England is the official Church of state in England. The monarch is the head of the Church of England.\n\n"
            "🇷🇺 *Перевод:* Церковь Англии — официальная государственная церковь. Монарх — её глава."
        ),
    },
    {
        "question": "Which TWO of the following plants are particularly associated with the UK?",
        "translation": "🇷🇺 Какие ДВА растения особенно связаны с UK?",
        "options": [
            "A — Shamrock and rose",
            "B — Cactus and olive tree",
            "C — Rose and cactus",
            "D — Shamrock and cactus"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 In England, the flower is the rose; in Northern Ireland it is the shamrock.\n\n"
            "🇷🇺 *Перевод:* Роза — символ Англии, трилистник (шамрок) — символ Северной Ирландии."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — \'The Divine Right of Kings\' was the idea that the English king should rule France.",
            "B — \'The Divine Right of Kings\' was the idea that the king was directly appointed by God to rule."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The \'Divine Right of Kings\' was the idea that the king was directly appointed by God to rule.\n\n"
            "🇷🇺 *Перевод:* «Божественное право королей» — идея о том, что король назначен Богом для правления."
        ),
    },
    {
        "question": "Which TWO records tell us about England during the time of William the Conqueror?",
        "translation": "🇷🇺 Какие ДВА документа рассказывают об Англии времён Вильгельма Завоевателя?",
        "options": [
            "A — The Domesday Book and the Bayeux Tapestry",
            "B — The Diary of Samuel Pepys and the Bayeux Tapestry",
            "C — The Domesday Book and the Magna Carta",
            "D — The Diary of Samuel Pepys and the Magna Carta"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Domesday Book is a record of towns and villages in England. The Bayeux Tapestry tells the story of the Norman Conquest.\n\n"
            "🇷🇺 *Перевод:* Книга Судного дня — перепись Англии. Гобелен из Байё — история Нормандского завоевания."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Police and Crime Commissioners (PCCs) are appointed through a public election.",
            "B — Police and Crime Commissioners (PCCs) are appointed by the local council."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The public in England and Wales elect Police and Crime Commissioners (PCCs). The first elections for PCCs were held in November 2012.\n\n"
            "🇷🇺 *Перевод:* Комиссары полиции (PCCs) избираются населением. Первые выборы — ноябрь 2012 года."
        ),
    },
    {
        "question": "What is the name of the UK currency?",
        "translation": "🇷🇺 Как называется валюта UK?",
        "options": [
            "A — Dollar",
            "B — Euro",
            "C — Pound sterling",
            "D — Yen"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The currency in the UK is the pound sterling (symbol £). There are 100 pence in a pound.\n\n"
            "🇷🇺 *Перевод:* Валюта UK — фунт стерлингов (£). В одном фунте 100 пенсов."
        ),
    },
    {
        "question": "Which TWO of the following were introduced in the early 20th century?",
        "translation": "🇷🇺 Что из следующего было введено в начале 20 века?",
        "options": [
            "A — Child Benefit payments and free school meals",
            "B — The National Health Service (NHS) and Child Benefit payments",
            "C — The National Health Service (NHS) and old-age pensions",
            "D — Old-age pensions and free school meals"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The early 20th century was a time of social progress. Old-age pensions and free school meals were important measures introduced.\n\n"
            "🇷🇺 *Перевод:* В начале 20 века были введены пенсии по старости и бесплатные школьные обеды."
        ),
    },
    {
        "question": "Who opens the new parliamentary session each year?",
        "translation": "🇷🇺 Кто открывает новую парламентскую сессию каждый год?",
        "options": [
            "A — The Archbishop of Canterbury",
            "B — The Prime Minister",
            "C — The Speaker of the House of Commons",
            "D — The King"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The King has important ceremonial roles, such as the opening of the new parliamentary session each year.\n\n"
            "🇷🇺 *Перевод:* Король выполняет важные церемониальные функции, включая открытие парламентской сессии."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe Scottish Parliament can pass laws for Scotland on all matters.",
        "translation": "🇷🇺 Верно или нет?\nШотландский парламент может принимать законы по всем вопросам.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The Scottish Parliament can pass laws for Scotland on all matters that are not specifically reserved to the UK Parliament.\n\n"
            "🇷🇺 *Перевод:* Шотландский парламент принимает законы только по вопросам, не зарезервированным за UK Parliament."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The King is ceremonial head of the Commonwealth.",
            "B — The King is ceremonial head of the North Atlantic Treaty Organization (NATO)."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The King is the ceremonial head of the Commonwealth, which currently has 56 member states.\n\n"
            "🇷🇺 *Перевод:* Король — церемониальный глава Содружества наций (56 государств-членов)."
        ),
    },
    {
        "question": "Which significant change was introduced by the Education Act of 1944?",
        "translation": "🇷🇺 Какое важное изменение ввёл Закон об образовании 1944 года?",
        "options": [
            "A — New public examinations",
            "B — Free secondary education in England and Wales",
            "C — Primary education for all",
            "D — The requirement to wear school uniform"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Education Act of 1944 (often called \'The Butler Act\') introduced free secondary education in England and Wales.\n\n"
            "🇷🇺 *Перевод:* Закон 1944 года («Акт Батлера») ввёл бесплатное среднее образование в Англии и Уэльсе."
        ),
    },
    {
        "question": "Which of the following is a responsibility you will have as a citizen or permanent resident of the UK?",
        "translation": "🇷🇺 Какова одна из ваших обязанностей как гражданина или постоянного жителя UK?",
        "options": [
            "A — To keep your dog on a lead at all times",
            "B — To avoid shopping on a Sunday",
            "C — To look after yourself and your family",
            "D — To grow your own vegetables"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 There are responsibilities shared by all those living in the UK. These include looking after yourself and your family.\n\n"
            "🇷🇺 *Перевод:* Одна из обязанностей жителей UK — заботиться о себе и своей семье."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Hadrian\'s Wall was built by the Roman Emperor Hadrian.",
            "B — Hadrian\'s Wall was built by the Picts (ancestors of the Scottish people) to keep out the Romans."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Emperor Hadrian built a wall in the north of England to keep out the Picts (ancestors of the Scottish people).\n\n"
            "🇷🇺 *Перевод:* Вал Адриана построил римский император Адриан, чтобы сдерживать пиктов."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe England women\'s football team has won the European Championships twice.",
        "translation": "🇷🇺 Верно или нет?\nЖенская сборная Англии по футболу дважды выигрывала чемпионат Европы.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The England women\'s football team has won the European Championship twice — in 2022 and 2025.\n\n"
            "🇷🇺 *Перевод:* Женская сборная Англии выигрывала Евро дважды — в 2022 и 2025 годах."
        ),
    },
    {
        "question": "In everyday language, people may say \'rain stopped play\'. With which sport is this phrase associated?",
        "translation": "🇷🇺 «Дождь остановил игру» — с каким спортом связана эта фраза?",
        "options": [
            "A — Football",
            "B — Cricket",
            "C — Rugby league",
            "D — Horse racing"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The expression \'rain stopped play\' is associated with cricket. The phrase has now passed into everyday usage.\n\n"
            "🇷🇺 *Перевод:* Выражение «дождь остановил игру» связано с крикетом."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Battle of Agincourt is commemorated in the Bayeux Tapestry.",
            "B — The Battle of Hastings is commemorated in the Bayeux Tapestry."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Bayeux Tapestry commemorates the victory of William, Duke of Normandy at the Battle of Hastings in 1066.\n\n"
            "🇷🇺 *Перевод:* Гобелен из Байё посвящён победе Вильгельма Нормандского при Гастингсе (1066)."
        ),
    },
    {
        "question": "Which cross on the Union Flag represents the patron saint of Scotland?",
        "translation": "🇷🇺 Какой крест на флаге UK символизирует покровителя Шотландии?",
        "options": [
            "A — The diagonal white cross",
            "B — The diagonal red cross",
            "C — The upright red cross",
            "D — None of these"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The cross of St Andrew, patron saint of Scotland, is a diagonal white cross on a blue ground.\n\n"
            "🇷🇺 *Перевод:* Крест Святого Андрея — диагональный белый крест на синем фоне."
        ),
    },
    {
        "question": "Which TWO of the following are linked to football?",
        "translation": "🇷🇺 Какие ДВА из следующего связаны с футболом?",
        "options": [
            "A — The Premier League and The Open",
            "B — UEFA and the Premier League",
            "C — The Ashes and UEFA",
            "D — The Ashes and The Open"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The English Premier League attracts a huge international audience. UK teams also compete in UEFA Champions League.\n\n"
            "🇷🇺 *Перевод:* Премьер-лига и УЕФА связаны с футболом. UK-клубы участвуют в Лиге чемпионов."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe Lake District is England\'s largest national park.",
        "translation": "🇷🇺 Верно или нет?\nОзёрный край — крупнейший национальный парк Англии.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The Lake District is England\'s largest national park. It covers 912 square miles (2,362 square kilometres).\n\n"
            "🇷🇺 *Перевод:* Озёрный край — крупнейший национальный парк Англии (912 кв. миль)."
        ),
    },
    ],
    14: [
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Reform Act of 1832 greatly increased the number of people who had the right to vote.",
            "B — The Reform Act of 1832 increased the power of the House of Lords."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Reform Act of 1832 greatly increased the number of people with the right to vote. It also abolished the old pocket and rotten boroughs.\n\n"
            "🇷🇺 *Перевод:* Закон о реформе 1832 года расширил круг избирателей и упразднил «гнилые местечки»."
        ),
    },
    {
        "question": "Which cross on the Union Flag represents the patron saint of Ireland?",
        "translation": "🇷🇺 Какой крест на флаге UK символизирует покровителя Ирландии?",
        "options": [
            "A — The diagonal white cross",
            "B — The diagonal red cross",
            "C — The upright red cross",
            "D — None of these"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The cross of St Patrick, patron saint of Ireland, is a diagonal red cross on a white background.\n\n"
            "🇷🇺 *Перевод:* Крест Святого Патрика — диагональный красный крест на белом фоне."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The capital cities of the nations of the UK are London, Swansea, Glasgow and Dublin.",
            "B — The capital cities of the nations of the UK are London, Cardiff, Edinburgh and Belfast."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The capital cities of the nations of the UK are: London (England), Cardiff (Wales), Edinburgh (Scotland) and Belfast (Northern Ireland).\n\n"
            "🇷🇺 *Перевод:* Столицы UK: Лондон, Кардифф, Эдинбург, Белфаст."
        ),
    },
    {
        "question": "Which Scottish king defeated the English at the Battle of Bannockburn in 1314?",
        "translation": "🇷🇺 Какой шотландский король победил англичан при Баннокборне в 1314 году?",
        "options": [
            "A — William Wallace",
            "B — Robert the Bruce",
            "C — Malcolm",
            "D — Andrew"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The English were defeated at the Battle of Bannockburn by Robert the Bruce in 1314.\n\n"
            "🇷🇺 *Перевод:* В битве при Баннокборне (1314) Роберт Брюс разгромил английские войска."
        ),
    },
    {
        "question": "Which TWO points about slavery are correct?",
        "translation": "🇷🇺 Какие ДВА утверждения о рабстве верны?",
        "options": [
            "A — William Wilberforce was a leading abolitionist and the Royal Navy refused to stop ships carrying slaves.",
            "B — Quakers set up the first anti-slavery groups and the Royal Navy refused to stop ships carrying slaves.",
            "C — Slavery survived in the British Empire until the early 20th century and the Royal Navy refused to stop ships.",
            "D — William Wilberforce was a leading abolitionist and Quakers set up the first anti-slavery groups."
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The first formal anti-slavery groups were set up by the Quakers. William Wilberforce was a leading Christian abolitionist in Parliament.\n\n"
            "🇷🇺 *Перевод:* Квакеры создали первые антирабовладельческие группы. Уилберфорс — ведущий аболиционист в Парламенте."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe daffodil is the national flower of Wales.",
        "translation": "🇷🇺 Верно или нет?\nНарцисс — национальный цветок Уэльса.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The daffodil is the national flower of Wales.\n\n"
            "🇷🇺 *Перевод:* Нарцисс — национальный цветок Уэльса."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe First World War ended at 11.00 am on 11 November 1918.",
        "translation": "🇷🇺 Верно или нет?\nПервая мировая война закончилась в 11:00 11 ноября 1918 года.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The First World War ended at 11.00 am on 11 November 1918.\n\n"
            "🇷🇺 *Перевод:* Первая мировая война закончилась в 11:00 утра 11 ноября 1918 года."
        ),
    },
    {
        "question": "Where do the Laurence Olivier awards take place?",
        "translation": "🇷🇺 Где проходит церемония вручения премий Лоуренса Оливье?",
        "options": [
            "A — London",
            "B — Cardiff",
            "C — Edinburgh",
            "D — Belfast"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Laurence Olivier Awards take place annually at different venues in London.\n\n"
            "🇷🇺 *Перевод:* Премии Оливье ежегодно вручаются на различных площадках Лондона."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Speaker of the House of Commons remains a Member of Parliament (MP) after election as Speaker.",
            "B — The Speaker of the House of Commons has to give up being an MP when elected as Speaker."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Speaker is neutral and does not represent a political party, but he or she remains an MP and represents a constituency.\n\n"
            "🇷🇺 *Перевод:* Спикер остаётся депутатом и представляет свой избирательный округ, хотя является нейтральным."
        ),
    },
    {
        "question": "Which sport can be traced back to 15th-century Scotland?",
        "translation": "🇷🇺 Какой вид спорта берёт начало в Шотландии 15 века?",
        "options": [
            "A — Surfing",
            "B — Formula 1",
            "C — Golf",
            "D — Motorbike racing"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The modern game of golf can be traced back to 15th century Scotland.\n\n"
            "🇷🇺 *Перевод:* Современный гольф берёт начало в Шотландии 15 века."
        ),
    },
    {
        "question": "Why was the Habeas Corpus Act of 1679 so important?",
        "translation": "🇷🇺 Почему Закон об Habeas Corpus 1679 года так важен?",
        "options": [
            "A — It ensured no person could be held prisoner unlawfully.",
            "B — It allowed people to bury the dead where they wished.",
            "C — It ensured that those who died could only be buried by a relative.",
            "D — It ended capital punishment in England."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Habeas Corpus Act guaranteed that no one could be held prisoner unlawfully. Habeas corpus is Latin for \'you must present the person in court\'.\n\n"
            "🇷🇺 *Перевод:* Акт Habeas Corpus гарантировал, что никто не может быть незаконно задержан."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe British Broadcasting Corporation (BBC) is financed by income tax.",
        "translation": "🇷🇺 Верно или нет?\nBBC финансируется за счёт подоходного налога.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The money from TV licences is used to pay for the BBC. Everyone with a device for watching live TV must have a television licence.\n\n"
            "🇷🇺 *Перевод:* BBC финансируется за счёт телевизионных лицензий, а не подоходного налога."
        ),
    },
    {
        "question": "What system of government does the UK have?",
        "translation": "🇷🇺 Какая система правления в UK?",
        "options": [
            "A — Communist government",
            "B — Dictatorship",
            "C — Parliamentary democracy",
            "D — Federal government"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The system of government in the UK is a parliamentary democracy.\n\n"
            "🇷🇺 *Перевод:* Система правления UK — парламентская демократия."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Highland Clearances took place in Scotland.",
            "B — The Highland Clearances took place in Ireland."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Highland Clearances took place in Scotland. Many Scottish landlords destroyed individual small farms (\'crofts\') to make space for large flocks.\n\n"
            "🇷🇺 *Перевод:* Горные расчистки происходили в Шотландии. Лендлорды уничтожали малые фермы (крофты)."
        ),
    },
    {
        "question": "Which TWO responsibilities do you have as a resident of the UK?",
        "translation": "🇷🇺 Какие ДВЕ обязанности у вас есть как жителя UK?",
        "options": [
            "A — Respect and obey the law, and take in and look after wild animals.",
            "B — Treat others with fairness and vote for the government in power.",
            "C — Treat others with fairness, and take in and look after wild animals.",
            "D — Respect and obey the law and treat others with fairness."
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 There are responsibilities shared by all those living in the UK. These include respecting and obeying the law, and treating others with fairness.\n\n"
            "🇷🇺 *Перевод:* Обязанности жителей UK: уважать закон и справедливо относиться к другим."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — A free press means that what is written in newspapers is free from government control.",
            "B — A free press means that newspapers are given out free of charge."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The UK has a free press. This means that what is written in newspapers is free from government control.\n\n"
            "🇷🇺 *Перевод:* Свобода прессы означает, что содержание газет не контролируется правительством."
        ),
    },
    {
        "question": "To which TWO international associations or agreements does the UK belong?",
        "translation": "🇷🇺 К каким ДВУМ международным организациям принадлежит UK?",
        "options": [
            "A — The North Atlantic Treaty Organization (NATO) and the North American Free Trade Agreement (NAFTA)",
            "B — The North Atlantic Treaty Organization (NATO) and the Commonwealth",
            "C — The Commonwealth and the Arab League",
            "D — The Commonwealth and the North American Free Trade Agreement (NAFTA)"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The UK belongs to many international bodies including NATO and the Commonwealth.\n\n"
            "🇷🇺 *Перевод:* UK входит в НАТО и Содружество наций."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Mousetrap is a play that has been running in London\'s West End since 1952.",
            "B — The Mousetrap is an environmental policy aiming to prevent mice from destroying crops."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Mousetrap, a murder-mystery play by Dame Agatha Christie, has been running in the West End since 1952.\n\n"
            "🇷🇺 *Перевод:* «Мышеловка» Агаты Кристи — пьеса, идущая на Вест-Энде с 1952 года."
        ),
    },
    {
        "question": "Which TWO were 20th-century British discoveries or inventions?",
        "translation": "🇷🇺 Какие ДВА открытия/изобретения были сделаны британцами в 20 веке?",
        "options": [
            "A — Radium and the printing press",
            "B — The hovercraft and radium",
            "C — Penicillin and the printing press",
            "D — The hovercraft and penicillin"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The hovercraft was invented by Sir Christopher Cockerell and penicillin was discovered by Sir Alexander Fleming.\n\n"
            "🇷🇺 *Перевод:* Судно на воздушной подушке — Кокерелл. Пенициллин — Флеминг."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The National Trust is a charity that works to preserve important buildings in the UK.",
            "B — The National Trust is a government-run organisation that provides funding for charities."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The National Trust in England, Wales and Northern Ireland works to preserve important buildings, coastline and countryside.\n\n"
            "🇷🇺 *Перевод:* National Trust — благотворительная организация, сохраняющая здания, побережья и природу UK."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Industrial Revolution was the rapid development of industry in the 18th and 19th centuries.",
            "B — The Industrial Revolution introduced changes in the banking system in the 1970s."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Industrial Revolution was the rapid development of industry in Britain in the 18th and 19th centuries, driven by machinery and steam power.\n\n"
            "🇷🇺 *Перевод:* Промышленная революция — стремительное развитие промышленности в 18–19 веках."
        ),
    },
    {
        "question": "TRUE or FALSE?\nSt Helena is a Crown dependency.",
        "translation": "🇷🇺 Верно или нет?\nСвятая Елена является зависимой территорией Короны.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 St Helena is a British overseas territory and not a Crown dependency.\n\n"
            "🇷🇺 *Перевод:* Остров Святой Елены — заморская территория Британии, а не зависимая территория Короны."
        ),
    },
    {
        "question": "Which of the following is part of the UK?",
        "translation": "🇷🇺 Что из следующего является частью UK?",
        "options": [
            "A — The Channel Islands",
            "B — Northern Ireland",
            "C — The Isle of Man",
            "D — The Falkland Islands"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Northern Ireland is part of the UK, along with England, Wales and Scotland.\n\n"
            "🇷🇺 *Перевод:* Северная Ирландия — часть UK вместе с Англией, Уэльсом и Шотландией."
        ),
    },
    {
        "question": "Which of the following do you need to do in order to get a full driving licence?",
        "translation": "🇷🇺 Что нужно сделать для получения полных водительских прав?",
        "options": [
            "A — Pass a driving test",
            "B — Buy a car or van",
            "C — Pay income tax",
            "D — Find a full-time job"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 To get a full UK driving licence, you must pass a driving test, which tests both your knowledge and your practical skills.\n\n"
            "🇷🇺 *Перевод:* Для получения полных прав нужно сдать экзамен на знание правил и практическое вождение."
        ),
    },
    ],    15: [
    {
        "question": "Which cross on the Union Flag represents the patron saint of England?",
        "translation": "🇷🇺 Какой крест на флаге UK символизирует покровителя Англии?",
        "options": [
            "A — The diagonal white cross",
            "B — The diagonal red cross",
            "C — The upright red cross",
            "D — None of these"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The cross of St George, patron saint of England, is an upright red cross on a white ground.\n\n"
            "🇷🇺 *Перевод:* Крест Святого Георгия — вертикальный красный крест на белом фоне."
        ),
    },
    {
        "question": "What is the aim of the United Nations?",
        "translation": "🇷🇺 Какова цель Организации Объединённых Наций?",
        "options": [
            "A — To create a single free trade market",
            "B — To prevent war and promote international peace and security",
            "C — To examine decisions made by the European Union",
            "D — To promote dictatorship"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The UK is part of the United Nations (UN). The UN was set up after the Second World War and aims to prevent war and promote international peace and security.\n\n"
            "🇷🇺 *Перевод:* ООН создана после Второй мировой войны с целью предотвращения войн и поддержания мира."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The capital city of Scotland is Edinburgh.",
            "B — The capital city of Scotland is Glasgow."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The capital city of Scotland is Edinburgh.\n\n"
            "🇷🇺 *Перевод:* Столица Шотландии — Эдинбург."
        ),
    },
    {
        "question": "What was the name given to supporters of King Charles I during the Civil War?",
        "translation": "🇷🇺 Как назывались сторонники короля Карла I во время Гражданской войны?",
        "options": [
            "A — Luddites",
            "B — Roundheads",
            "C — Cavaliers",
            "D — Levellers"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The king's supporters during the Civil War were called Cavaliers. Those who supported Parliament were called Roundheads.\n\n"
            "🇷🇺 *Перевод:* Сторонники короля — «кавалеры». Сторонники Парламента — «круглоголовые»."
        ),
    },
    {
        "question": "Which season of orchestral classical music has been organised by the BBC since 1927?",
        "translation": "🇷🇺 Какой сезон классической оркестровой музыки организует BBC с 1927 года?",
        "options": [
            "A — The Eisteddfod",
            "B — Aldeburgh Festival",
            "C — The Proms",
            "D — Glastonbury"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Proms is an eight-week summer season of orchestral classical music that takes place in various venues, including the Royal Albert Hall in London. It has been organised by the BBC since 1927.\n\n"
            "🇷🇺 *Перевод:* «Промс» — восьминедельный летний сезон классической музыки, организуемый BBC с 1927 года."
        ),
    },
    {
        "question": "Which TWO chambers form the UK Parliament?",
        "translation": "🇷🇺 Какие ДВЕ палаты образуют Парламент UK?",
        "options": [
            "A — House of Lords and House of Representatives",
            "B — House of Fraser and House of Commons",
            "C — House of Commons and House of Representatives",
            "D — House of Lords and House of Commons"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The UK Parliament is formed by the House of Commons and the House of Lords.\n\n"
            "🇷🇺 *Перевод:* Парламент UK состоит из Палаты общин и Палаты лордов."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe shamrock is the national flower of Scotland.",
        "translation": "🇷🇺 Верно или нет?\nТрилистник (шамрок) — национальный цветок Шотландии.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The shamrock is the national flower of Northern Ireland, and the thistle is the national flower of Scotland.\n\n"
            "🇷🇺 *Перевод:* Шамрок — символ Северной Ирландии. Чертополох — национальный символ Шотландии."
        ),
    },
    {
        "question": "To apply for UK citizenship or permanent residency, which TWO things do you need?",
        "translation": "🇷🇺 Что из следующего нужно для подачи заявки на гражданство или ПМЖ UK?",
        "options": [
            "A — An ability to speak and read English, and a good knowledge of life in the UK",
            "B — A UK bank account and an ability to speak and read English",
            "C — A UK bank account and a good understanding of life in the UK",
            "D — An ability to speak and read English, and a driving licence"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 To apply to become a permanent resident or a naturalised citizen of the UK, you must be able to speak and read English and have a good understanding of life in the UK.\n\n"
            "🇷🇺 *Перевод:* Для ПМЖ/гражданства нужны: знание английского языка и знание жизни в UK."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — There are a few Members of Parliament who do not represent any of the main political parties.",
            "B — All Members of Parliament have to belong to a political party."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 There are a few Members of Parliament (MPs) who do not represent any of the main political parties. They are called 'independents'.\n\n"
            "🇷🇺 *Перевод:* Некоторые депутаты не представляют крупные партии — их называют независимыми."
        ),
    },
    {
        "question": "Which TWO of the following were major welfare changes introduced from 1945 to 1950?",
        "translation": "🇷🇺 Какие ДВА крупных социальных изменения были введены с 1945 по 1950 год?",
        "options": [
            "A — The National Health Service (NHS) and a national system of benefits",
            "B — The State retirement pension and employment exchanges",
            "C — The National Health Service (NHS) and employment exchanges",
            "D — Employment exchanges and free school meals"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The Labour government elected in 1945 established the National Health Service (NHS) and a national system of benefits.\n\n"
            "🇷🇺 *Перевод:* Лейбористское правительство 1945 года создало NHS и национальную систему пособий."
        ),
    },
    {
        "question": "Which language was spoken by people during the Iron Age?",
        "translation": "🇷🇺 На каком языке говорили люди в железном веке?",
        "options": [
            "A — Latin",
            "B — A language that was part of the Celtic family",
            "C — English",
            "D — Anglo-Saxon"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The language Iron Age people spoke was part of the Celtic language family.\n\n"
            "🇷🇺 *Перевод:* Люди железного века говорили на языке кельтской языковой группы."
        ),
    },
    {
        "question": "Which TWO of the following are part of the UK government?",
        "translation": "🇷🇺 Какие ДВЕ структуры являются частью правительства UK?",
        "options": [
            "A — The cabinet and the civil service",
            "B — The civil service and FIFA",
            "C — The National Trust and FIFA",
            "D — The cabinet and the National Trust"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 There are several different parts of government in the UK, including the cabinet and the civil service.\n\n"
            "🇷🇺 *Перевод:* В состав правительства UK входят кабинет министров и государственная служба."
        ),
    },
    {
        "question": "Who first built the Tower of London?",
        "translation": "🇷🇺 Кто первым построил Лондонский Тауэр?",
        "options": [
            "A — Oliver Cromwell",
            "B — Queen Elizabeth II",
            "C — William the Conqueror",
            "D — Winston Churchill"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Tower of London was first built by William the Conqueror after he became king in 1066.\n\n"
            "🇷🇺 *Перевод:* Лондонский Тауэр впервые построил Вильгельм Завоеватель после того, как стал королём в 1066 году."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe criminal court systems in England, Wales, Scotland and Northern Ireland are identical.",
        "translation": "🇷🇺 Верно или нет?\nСистемы уголовного суда в Англии, Уэльсе, Шотландии и Северной Ирландии одинаковы.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 There are some differences between the criminal court systems in different parts of the UK.\n\n"
            "🇷🇺 *Перевод:* Системы уголовного судопроизводства в разных частях UK имеют различия."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe Wimbledon Championships are associated with motor sports.",
        "translation": "🇷🇺 Верно или нет?\nЧемпионат Уимблдона связан с автоспортом.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The Wimbledon Championships is the oldest tennis tournament in the world.\n\n"
            "🇷🇺 *Перевод:* Уимблдон — старейший теннисный турнир в мире, не связанный с автоспортом."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — By the middle of the 17th century the last Welsh rebellions had been defeated.",
            "B — By the middle of the 15th century the last Welsh rebellions had been defeated."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The last Welsh rebellions were defeated by the middle of the 15th century.\n\n"
            "🇷🇺 *Перевод:* Последние валлийские восстания были подавлены к середине 15 века."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThere are many variations in language in the different parts of the UK.",
        "translation": "🇷🇺 Верно или нет?\nВ разных частях UK существуют многочисленные языковые различия.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 There are many variations in language in the different parts of the UK. In Wales many people speak Welsh; in parts of Scotland, Gaelic is spoken; in Northern Ireland some people speak Irish Gaelic.\n\n"
            "🇷🇺 *Перевод:* В Уэльсе говорят по-валлийски, в Шотландии — на гэльском, в Северной Ирландии — на ирландском гэльском."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe Scottish Parliament sits in Edinburgh.",
        "translation": "🇷🇺 Верно или нет?\nШотландский парламент заседает в Эдинбурге.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 The Scottish Parliament was formed in 1999. It sits in Edinburgh, the capital city of Scotland.\n\n"
            "🇷🇺 *Перевод:* Шотландский парламент основан в 1999 году и заседает в Эдинбурге."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThe jet engine and radar were developed in Britain in the 1830s.",
        "translation": "🇷🇺 Верно или нет?\nРеактивный двигатель и радар были разработаны в Британии в 1830-х годах.",
        "options": ["TRUE", "FALSE"],
        "answer": 1,
        "explanation": (
            "❌ *Неверно! / False!*\n\n"
            "📖 The jet engine and the radar were both developed in Britain in the 1930s, not the 1830s.\n\n"
            "🇷🇺 *Перевод:* Реактивный двигатель и радар разработаны в 1930-х, а не 1830-х годах."
        ),
    },
    {
        "question": "What must you do in order to vote in elections?",
        "translation": "🇷🇺 Что нужно сделать, чтобы иметь право голосовать на выборах?",
        "options": [
            "A — Pay income tax in the year before the election.",
            "B — Put your name on the electoral register.",
            "C — Register your identity with the police.",
            "D — Pass an electoral test."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 To be able to vote in a parliamentary or local election, you must have your name on the electoral register.\n\n"
            "🇷🇺 *Перевод:* Чтобы голосовать, необходимо внести своё имя в список избирателей."
        ),
    },
    {
        "question": "In which period of British history did people live in roundhouses and bury their dead in tombs called round barrows?",
        "translation": "🇷🇺 В какой период истории Британии люди жили в круглых домах и хоронили умерших в курганах?",
        "options": [
            "A — The Middle Ages",
            "B — The Bronze Age",
            "C — The Stone Age",
            "D — The Victorian Age"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Around 4,000 years ago, people learned to make bronze. We call this period the Bronze Age. People lived in roundhouses and buried their dead in tombs called round barrows.\n\n"
            "🇷🇺 *Перевод:* В бронзовом веке (ок. 4000 лет назад) люди жили в круглых домах и хоронили умерших в курганах."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The UK is a member of NATO.",
            "B — The UK has never been a member of NATO."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The UK is a member of NATO (North Atlantic Treaty Organization), a group of European and North American countries that have agreed to help each other if they come under attack.\n\n"
            "🇷🇺 *Перевод:* UK входит в НАТО — организацию, члены которой обязуются помогать друг другу в случае нападения."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — The Roman army left England after 100 years to defend other parts of their Empire.",
            "B — The Roman army left England after 400 years to defend other parts of their Empire."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Romans left England in AD 410 to defend other parts of their Empire. They had remained in Britain for 400 years.\n\n"
            "🇷🇺 *Перевод:* Римляне покинули Британию в 410 году н.э., пробыв там около 400 лет."
        ),
    },
    {
        "question": "Which of the following is a British overseas territory?",
        "translation": "🇷🇺 Что из следующего является заморской территорией Британии?",
        "options": [
            "A — Northern Ireland",
            "B — Falkland Islands",
            "C — France",
            "D — USA"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 There are several British overseas territories in other parts of the world, such as the Falkland Islands.\n\n"
            "🇷🇺 *Перевод:* Фолклендские острова — одна из заморских территорий Великобритании."
        ),
    },
    ],
    16: [
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Wales and Northern Ireland each have their own Church of state.",
            "B — There is no established Church in Wales or Northern Ireland."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 There is no established Church in Wales or Northern Ireland.\n\n"
            "🇷🇺 *Перевод:* В Уэльсе и Северной Ирландии нет официальной государственной церкви."
        ),
    },
    {
        "question": "TRUE or FALSE?\nThomas Hardy was a famous author who wrote Far from the Madding Crowd.",
        "translation": "🇷🇺 Верно или нет?\nТомас Гарди — известный писатель, автор романа «Вдали от обезумевшей толпы».",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 Thomas Hardy (1840–1928) was an author and poet. His best-known novels include Far from the Madding Crowd and Jude the Obscure.\n\n"
            "🇷🇺 *Перевод:* Томас Гарди (1840–1928) — писатель и поэт. Его известные романы: «Вдали от обезумевшей толпы» и «Джуд Незаметный»."
        ),
    },
    {
        "question": "What was the Reformation?",
        "translation": "🇷🇺 Что такое Реформация?",
        "options": [
            "A — A reduction in the power of the nobles",
            "B — A movement against the authority of the Pope",
            "C — A part of the Wars of the Roses",
            "D — A bill of rights"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Reformation occurred across Europe. It was a movement against the authority of the Pope and the ideas and practices of the Roman Catholic Church.\n\n"
            "🇷🇺 *Перевод:* Реформация — общеевропейское движение против власти Папы и Католической церкви."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — In the UK, pregnant women have the same right to work as anyone else.",
            "B — In the UK, employers have the right not to employ pregnant women."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 UK laws ensure people are not treated unfairly because of pregnancy and maternity, among other protected characteristics.\n\n"
            "🇷🇺 *Перевод:* Законы UK защищают от дискриминации по беременности и материнству."
        ),
    },
    {
        "question": "Hadrian's Wall was built to keep out whom?",
        "translation": "🇷🇺 Для сдерживания кого был построен Вал Адриана?",
        "options": [
            "A — The Irish",
            "B — The Welsh",
            "C — The Picts",
            "D — The Vikings"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Roman Emperor Hadrian built the wall in the north of England to keep out the Picts (ancestors of the Scottish people).\n\n"
            "🇷🇺 *Перевод:* Вал Адриана построен для сдерживания пиктов — предков шотландцев."
        ),
    },
    {
        "question": "Where did the Vikings come from?",
        "translation": "🇷🇺 Откуда пришли викинги?",
        "options": [
            "A — Germany and Austria",
            "B — Belgium and Holland",
            "C — Denmark, Norway and Sweden",
            "D — France and Luxembourg"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Vikings first raided Britain in AD 789. They came from Denmark, Norway and Sweden.\n\n"
            "🇷🇺 *Перевод:* Первые набеги викингов на Британию — 789 год н.э. Они пришли из Дании, Норвегии и Швеции."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Volunteering is a good way to earn additional money.",
            "B — Volunteering is a way of helping others without receiving payment."
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Volunteering is working for good causes without payment. There are many activities you can do as a volunteer, such as working with the homeless or helping improve the environment.\n\n"
            "🇷🇺 *Перевод:* Волонтёрство — помощь другим без оплаты. Можно помогать бездомным, улучшать окружающую среду и т.д."
        ),
    },
    {
        "question": "TRUE or FALSE?\nPeople can see the Crown Jewels at the Tower of London.",
        "translation": "🇷🇺 Верно или нет?\nКоронные регалии можно увидеть в Лондонском Тауэре.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 People can see the Crown Jewels at the Tower of London.\n\n"
            "🇷🇺 *Перевод:* Коронные регалии выставлены в Лондонском Тауэре."
        ),
    },
    {
        "question": "For which TWO types of literature is William Shakespeare famous?",
        "translation": "🇷🇺 Какими ДВУМЯ видами литературы известен Уильям Шекспир?",
        "options": [
            "A — Plays and sonnets",
            "B — Biographies and sonnets",
            "C — Novels and biographies",
            "D — Novels and plays"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 William Shakespeare was a famous playwright and sonnet writer.\n\n"
            "🇷🇺 *Перевод:* Шекспир известен как автор пьес и сонетов."
        ),
    },
    {
        "question": "For which TWO reasons is Henry VIII remembered?",
        "translation": "🇷🇺 По каким ДВУМ причинам помнят Генриха VIII?",
        "options": [
            "A — Married six times and fought in the Battle of Agincourt",
            "B — Married six times and broke away from the Church of Rome",
            "C — Introduced the game of croquet and married six times",
            "D — Introduced the game of croquet and fought in the Battle of Agincourt"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Henry VIII is remembered for breaking away from the Catholic Church of Rome and marrying six times.\n\n"
            "🇷🇺 *Перевод:* Генрих VIII известен разрывом с Католической церковью и шестью браками."
        ),
    },
    {
        "question": "For approximately how many years did the Romans remain in Britain?",
        "translation": "🇷🇺 Приблизительно сколько лет римляне оставались в Британии?",
        "options": [
            "A — 50 years",
            "B — 100 years",
            "C — 400 years",
            "D — 600 years"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Romans remained in Britain for almost 400 years, from AD 43 to AD 410.\n\n"
            "🇷🇺 *Перевод:* Римляне оставались в Британии около 400 лет — с 43 по 410 год н.э."
        ),
    },
    {
        "question": "TRUE or FALSE?\nUK population growth has been faster in more recent years.",
        "translation": "🇷🇺 Верно или нет?\nРост населения UK ускорился в последние годы.",
        "options": ["TRUE", "FALSE"],
        "answer": 0,
        "explanation": (
            "✅ *Верно! / True!*\n\n"
            "📖 UK population growth has been faster in more recent years. Migration into the UK and longer life expectancy have played a part in this.\n\n"
            "🇷🇺 *Перевод:* Рост населения UK ускорился — из-за миграции и увеличения продолжительности жизни."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — When buying a car, you must pay an annual vehicle tax.",
            "B — When buying a car, you do not need to pay vehicle tax if the previous owner has already paid it."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 When you buy a car, you must pay an annual vehicle tax, which cannot be passed on when a vehicle changes hands.\n\n"
            "🇷🇺 *Перевод:* При покупке автомобиля необходимо платить ежегодный транспортный налог — он не переходит к новому владельцу."
        ),
    },
    {
        "question": "The Union Flag consists of three crosses. One is the cross of St George. Who do the other TWO crosses represent?",
        "translation": "🇷🇺 Флаг UK состоит из трёх крестов. Один — крест Святого Георгия. Кого представляют два других?",
        "options": [
            "A — St David and St Piran",
            "B — St David and St Andrew",
            "C — St Patrick and St Andrew",
            "D — St Patrick and St Piran"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Union Flag consists of the crosses of Saints George, Andrew and Patrick.\n\n"
            "🇷🇺 *Перевод:* Флаг UK объединяет кресты Святых Георгия, Андрея и Патрика."
        ),
    },
    {
        "question": "Which of the following statements is correct?",
        "translation": "🇷🇺 Какое из следующих утверждений верно?",
        "options": [
            "A — Charles, king of Scotland, was crowned King Charles II of England in 1660.",
            "B — Bonnie Prince Charlie became King Charles II of England in 1660."
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 In May 1660, Parliament invited Charles to come back from exile. He was crowned King Charles II of England, Wales, Scotland and Ireland.\n\n"
            "🇷🇺 *Перевод:* В 1660 году Карл II вернулся из изгнания и был коронован королём Англии, Уэльса, Шотландии и Ирландии."
        ),
    },
    {
        "question": "Which TWO of the following types of case are held in Crown Courts?",
        "translation": "🇷🇺 Дела каких ДВУХ категорий рассматриваются в Королевских судах?",
        "options": [
            "A — Theft and murder",
            "B — Serious and minor criminal offences",
            "C — All criminal offences and breaches of contract",
            "D — Serious breaches of contract"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Crown Courts deal with serious criminal cases such as theft and murder.\n\n"
            "🇷🇺 *Перевод:* Королевские суды рассматривают серьёзные уголовные дела, например кражи и убийства."
        ),
    },
    {
        "question": "Which is a famous landmark in Wales?",
        "translation": "🇷🇺 Что является знаменитой достопримечательностью Уэльса?",
        "options": [
            "A — Snowdonia",
            "B — The Giant's Causeway",
            "C — Loch Lomond",
            "D — The Lake District"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Snowdonia is a national park in North Wales. Its most well-known landmark is Snowdon, which is the highest mountain in Wales.\n\n"
            "🇷🇺 *Перевод:* Сноудония — национальный парк в Северном Уэльсе. Сноудон — высочайшая гора Уэльса."
        ),
    },
    {
        "question": "What celebration takes place each year on 14 February?",
        "translation": "🇷🇺 Какой праздник отмечается ежегодно 14 февраля?",
        "options": [
            "A — Valentine's Day",
            "B — Bonfire Night",
            "C — Halloween",
            "D — Hogmanay"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 Valentine's Day, on 14 February, is when lovers exchange cards and gifts. Sometimes people send anonymous cards to someone they secretly admire.\n\n"
            "🇷🇺 *Перевод:* День святого Валентина — 14 февраля. Влюблённые обмениваются открытками и подарками."
        ),
    },
    {
        "question": "Which TWO of the following were British inventions?",
        "translation": "🇷🇺 Какие ДВА из следующего являются британскими изобретениями?",
        "options": [
            "A — Television and the jet engine",
            "B — The jet engine and radio",
            "C — Television and the diesel engine",
            "D — Radio and the diesel engine"
        ],
        "answer": 0,
        "explanation": (
            "✅ *Верно — A!*\n\n"
            "📖 The television and jet engine are two of many important inventions by Britons in the 20th century.\n\n"
            "🇷🇺 *Перевод:* Телевидение и реактивный двигатель — два важных британских изобретения 20 века."
        ),
    },
    {
        "question": "Henry VII established the House of Tudor. What colour rose became the Tudor emblem?",
        "translation": "🇷🇺 Генрих VII основал династию Тюдоров. Какого цвета роза стала их эмблемой?",
        "options": [
            "A — White",
            "B — Red and white",
            "C — Red",
            "D — Pink"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 The Tudor rose was a red rose with a white rose inside it, showing the alliance between the Houses of York and Lancaster.\n\n"
            "🇷🇺 *Перевод:* Роза Тюдоров — красная роза с белой внутри, символизирующая союз Йорков и Ланкастеров."
        ),
    },
    {
        "question": "Which countries make up 'Great Britain'?",
        "translation": "🇷🇺 Какие страны входят в состав «Великобритании»?",
        "options": [
            "A — Just England",
            "B — England, Scotland and Wales",
            "C — England and Scotland",
            "D — England, Scotland and Northern Ireland"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 'Great Britain' refers only to England, Scotland and Wales, not to Northern Ireland. The official name of the country is the United Kingdom of Great Britain and Northern Ireland.\n\n"
            "🇷🇺 *Перевод:* «Великобритания» — только Англия, Шотландия и Уэльс. Официальное название страны включает и Северную Ирландию."
        ),
    },
    {
        "question": "Which TWO of the following are traditional British foods?",
        "translation": "🇷🇺 Какие ДВА из следующего являются традиционными британскими блюдами?",
        "options": [
            "A — Strudel and haggis",
            "B — Welsh cakes and haggis",
            "C — Sushi and Welsh cakes",
            "D — Sushi and haggis"
        ],
        "answer": 1,
        "explanation": (
            "✅ *Верно — B!*\n\n"
            "📖 Welsh cakes are a traditional Welsh snack. Haggis is a traditional Scottish food made from sheep's stomach stuffed with offal, suet, onions and oatmeal.\n\n"
            "🇷🇺 *Перевод:* Валлийские кексы — традиционная закуска Уэльса. Хаггис — традиционное шотландское блюдо из бараньего желудка."
        ),
    },
    {
        "question": "Which of the following is the capital city of the UK?",
        "translation": "🇷🇺 Какой из следующих городов является столицей UK?",
        "options": [
            "A — Westminster",
            "B — Birmingham",
            "C — Windsor",
            "D — London"
        ],
        "answer": 3,
        "explanation": (
            "✅ *Верно — D!*\n\n"
            "📖 The capital city of the UK is London, which is in England.\n\n"
            "🇷🇺 *Перевод:* Столица UK — Лондон, расположенный в Англии."
        ),
    },
    {
        "question": "Which of the following is a Crown dependency?",
        "translation": "🇷🇺 Что из следующего является зависимой территорией Короны?",
        "options": [
            "A — England",
            "B — Northern Ireland",
            "C — Channel Islands",
            "D — Scotland"
        ],
        "answer": 2,
        "explanation": (
            "✅ *Верно — C!*\n\n"
            "📖 The Channel Islands are closely linked with the UK but are not part of it. These islands have their own governments and are called 'Crown dependencies'.\n\n"
            "🇷🇺 *Перевод:* Нормандские острова — зависимые территории Короны со своим управлением, не часть UK."
        ),
    },
    ],

17: [
{
"question": "TRUE or FALSE?\nThe Union Flag consists of four crosses.",
"translation": "🇷🇺 Верно или нет?\nФлаг Союза состоит из четырёх крестов.",
"options": ["TRUE", "FALSE"],
"answer": 1,
"explanation": (
"❌ *Неверно! / False!*\n\n"
"📖 The Union Flag consists of three crosses — the crosses of St George (England), St Andrew (Scotland) and St Patrick (Ireland).\n\n"
"🇷🇺 *Перевод:* Флаг Союза состоит из трёх крестов — Святого Георгия, Святого Андрея и Святого Патрика."
),
},
{
"question": "Which of the following statements is correct?",
"translation": "🇷🇺 Какое из следующих утверждений верно?",
"options": [
"A — To become a permanent resident, you must be able to speak and read English",
"B — To become a permanent resident, you must be able to speak French"
],
"answer": 0,
"explanation": (
"✅ *Верно — A!*\n\n"
"📖 To apply to become a permanent resident or naturalised citizen of the UK, you must be able to speak and read English and have a good understanding of life in the UK.\n\n"
"🇷🇺 *Перевод:* Для постоянного проживания нужно говорить и читать по-английски и знать жизнь в UK."
),
},
{
"question": "Which of the following statements is correct?",
"translation": "🇷🇺 Какое из следующих утверждений верно?",
"options": [
"A — Women in Britain make up about a quarter of the workforce",
"B — Women in Britain make up about half of the workforce"
],
"answer": 1,
"explanation": (
"✅ *Верно — B!*\n\n"
"📖 Women in Britain make up about half of the workforce. Employment opportunities for women are much greater than they were in the past.\n\n"
"🇷🇺 *Перевод:* Женщины составляют около половины рабочей силы Великобритании."
),
},
{
"question": "When did wives first get the right to keep their own earnings and property?",
"translation": "🇷🇺 Когда жёны впервые получили право сохранять собственные доходы и имущество?",
"options": [
"A — 1800 and 1820",
"B — 1900 and 1920",
"C — 1870 and 1882",
"D — 1950 and 1960"
],
"answer": 2,
"explanation": (
"✅ *Верно — C!*\n\n"
"📖 Until 1870, a married woman's earnings and property automatically belonged to her husband. Acts of Parliament in 1870 and 1882 gave wives the right to keep their own earnings and property.\n\n"
"🇷🇺 *Перевод:* До 1870 года имущество жены принадлежало мужу. Законы 1870 и 1882 годов изменили это."
),
},
{
"question": "Which TWO are traditional pub games?",
"translation": "🇷🇺 Какие ДВА — традиционные игры в пабе?",
"options": [
"A — Chess and darts",
"B — Pool and darts",
"C — Chess and snooker",
"D — Pool and snooker"
],
"answer": 1,
"explanation": (
"✅ *Верно — B!*\n\n"
"📖 Pool and darts are traditional pub games. Pub quizzes are also popular.\n\n"
"🇷🇺 *Перевод:* Пул и дартс — традиционные игры в пабах."
),
},
{
"question": "TRUE or FALSE?\nHenry VIII established the Church of England because the Pope refused to grant him a divorce.",
"translation": "🇷🇺 Верно или нет?\nГенрих VIII основал Церковь Англии, потому что Папа отказал ему в разводе.",
"options": ["TRUE", "FALSE"],
"answer": 0,
"explanation": (
"✅ *Верно! / True!*\n\n"
"📖 To divorce his first wife Catherine of Aragon, Henry needed the approval of the Pope. When the Pope refused, Henry established the Church of England.\n\n"
"🇷🇺 *Перевод:* Папа отказал Генриху в разводе, поэтому тот основал Церковь Англии."
),
},
{
"question": "TRUE or FALSE?\nThe British team was the first to successfully clone a mammal.",
"translation": "🇷🇺 Верно или нет?\nБританская команда первой успешно клонировала млекопитающее.",
"options": ["TRUE", "FALSE"],
"answer": 0,
"explanation": (
"✅ *Верно! / True!*\n\n"
"📖 The British team was the first to succeed in cloning a mammal — Dolly the sheep.\n\n"
"🇷🇺 *Перевод:* Британская команда первой клонировала млекопитающее — овцу Долли."
),
},
{
"question": "What are bank holidays?",
"translation": "🇷🇺 Что такое bank holidays?",
"options": [
"A — Public holidays when banks and many businesses close",
"B — Days when only banks are open",
"C — Days when schools are closed but businesses open",
"D — Religious holidays only"
],
"answer": 0,
"explanation": (
"✅ *Верно — A!*\n\n"
"📖 There are public holidays each year, called bank holidays, when banks and many other businesses close for the day.\n\n"
"🇷🇺 *Перевод:* Банковские праздники — государственные выходные, когда банки и многие предприятия закрыты."
),
},
{
"question": "TRUE or FALSE?\nThe Welsh dragon appears on the Union Flag.",
"translation": "🇷🇺 Верно или нет?\nВаллийский дракон изображён на Флаге Союза.",
"options": ["TRUE", "FALSE"],
"answer": 1,
"explanation": (
"❌ *Неверно! / False!*\n\n"
"📖 Wales has its own flag showing a dragon, but the Welsh dragon does not appear on the Union Flag because Wales was already united with England when the first Union Flag was created in 1606.\n\n"
"🇷🇺 *Перевод:* Валлийский дракон не входит в Флаг Союза, так как Уэльс уже был частью Англии в 1606 году."
),
},
{
"question": "Why did Britain declare war on Germany in 1939?",
"translation": "🇷🇺 Почему Британия объявила войну Германии в 1939 году?",
"options": [
"A — Because Germany attacked France",
"B — Because Germany attacked Britain",
"C — Because Hitler invaded Poland",
"D — Because Germany invaded Russia"
],
"answer": 2,
"explanation": (
"✅ *Верно — C!*\n\n"
"📖 When Adolf Hitler invaded Poland in 1939, Britain and France declared war on Germany in order to stop his aggression.\n\n"
"🇷🇺 *Перевод:* Когда Гитлер вторгся в Польшу в 1939 году, Британия и Франция объявили войну Германии."
),
},
{
"question": "Which of the following statements is correct?",
"translation": "🇷🇺 Какое из следующих утверждений верно?",
"options": [
"A — William Shakespeare (1564-1616) was a playwright and actor",
"B — William Shakespeare (1564-1616) was a scientist and explorer"
],
"answer": 0,
"explanation": (
"✅ *Верно — A!*\n\n"
"📖 William Shakespeare (1564-1616) was a playwright and actor. His plays and poems are still performed and studied in Britain and other countries today.\n\n"
"🇷🇺 *Перевод:* Шекспир (1564–1616) — драматург и актёр, его произведения изучают по всему миру."
),
},
{
"question": "Who was the British Prime Minister from 1940 to 1945?",
"translation": "🇷🇺 Кто был премьер-министром Великобритании с 1940 по 1945 год?",
"options": [
"A — Margaret Thatcher",
"B — Winston Churchill",
"C — Tony Blair",
"D — Clement Attlee"
],
"answer": 1,
"explanation": (
"✅ *Верно — B!*\n\n"
"📖 Winston Churchill was the British Prime Minister from 1940 to 1945, during the Second World War.\n\n"
"🇷🇺 *Перевод:* Уинстон Черчилль был премьер-министром Великобритании с 1940 по 1945 год."
),
},
{
"question": "Which of the following are British overseas territories?",
"translation": "🇷🇺 Какой из следующих является британской заморской территорией?",
"options": [
"A — Canada and Australia",
"B — St Helena and the Falkland Islands",
"C — India and Jamaica",
"D — France and Germany"
],
"answer": 1,
"explanation": (
"✅ *Верно — B!*\n\n"
"📖 There are several British overseas territories in other parts of the world, such as St Helena and the Falkland Islands. They are linked to the UK but are not part of it.\n\n"
"🇷🇺 *Перевод:* Острова Святой Елены и Фолклендские острова — британские заморские территории."
),
},
{
"question": "After the Bill of Rights in 1689, what were the two main groups in Parliament called?",
"translation": "🇷🇺 Как назывались две главные политические группы в Парламенте после Билля о правах 1689 года?",
"options": [
"A — Whigs and Tories",
"B — Labour and Conservatives",
"C — Liberals and Nationalists",
"D — Roundheads and Cavaliers"
],
"answer": 0,
"explanation": (
"✅ *Верно — A!*\n\n"
"📖 After the Bill of Rights was declared in 1689, there were two main groups in Parliament — the Whigs and the Tories. The modern Conservative Party is still sometimes referred to as the Tories.\n\n"
"🇷🇺 *Перевод:* После Билля о правах в Парламенте появились виги и тори."
),
},
{
"question": "Where were the 2012 Paralympic Games hosted?",
"translation": "🇷🇺 Где проходили Паралимпийские игры 2012 года?",
"options": [
"A — Edinburgh",
"B — Cardiff",
"C — Manchester",
"D — London"
],
"answer": 3,
"explanation": (
"✅ *Верно — D!*\n\n"
"📖 The Paralympic Games for 2012 were hosted in London.\n\n"
"🇷🇺 *Перевод:* Паралимпийские игры 2012 года проходили в Лондоне."
),
},
{
"question": "TRUE or FALSE?\nSome people rent additional land called an allotment to grow fruit and vegetables.",
"translation": "🇷🇺 Верно или нет?\nНекоторые люди арендуют землю (allotment) для выращивания овощей и фруктов.",
"options": ["TRUE", "FALSE"],
"answer": 0,
"explanation": (
"✅ *Верно! / True!*\n\n"
"📖 A lot of people have gardens at home. Some people rent additional land called 'an allotment' where they grow fruit and vegetables.\n\n"
"🇷🇺 *Перевод:* Некоторые британцы арендуют землю (allotment) для выращивания овощей и фруктов."
),
},
{
"question": "What must all dogs in public places wear?",
"translation": "🇷🇺 Что обязаны носить все собаки в общественных местах?",
"options": [
"A — A muzzle at all times",
"B — A lead at all times",
"C — A lead and muzzle at all times",
"D — A collar showing the name and address of the owner"
],
"answer": 3,
"explanation": (
"✅ *Верно — D!*\n\n"
"📖 All dogs in public places must wear a collar showing the name and address of the owner.\n\n"
"🇷🇺 *Перевод:* Все собаки в общественных местах должны носить ошейник с именем и адресом владельца."
),
},
{
"question": "TRUE or FALSE?\nWales became formally united with England during the reign of Henry VIII.",
"translation": "🇷🇺 Верно или нет?\nУэльс официально объединился с Англией во время правления Генриха VIII.",
"options": ["TRUE", "FALSE"],
"answer": 0,
"explanation": (
"✅ *Верно! / True!*\n\n"
"📖 During the reign of Henry VIII, Wales became formally united with England by the Act for the Government of Wales.\n\n"
"🇷🇺 *Перевод:* При Генрихе VIII Уэльс официально объединился с Англией по Акту об управлении Уэльсом."
),
},
{
"question": "Which of the following statements is correct?",
"translation": "🇷🇺 Какое из следующих утверждений верно?",
"options": [
"A — The UK is governed by the parliament sitting in Westminster",
"B — The UK is governed only by the Scottish Parliament"
],
"answer": 0,
"explanation": (
"✅ *Верно — A!*\n\n"
"📖 The UK is governed by the parliament sitting in Westminster. Scotland, Wales and Northern Ireland also have parliaments or assemblies with devolved powers.\n\n"
"🇷🇺 *Перевод:* UK управляется Парламентом в Вестминстере. У Шотландии, Уэльса и Северной Ирландии есть собственные ассамблеи."
),
},
{
"question": "What is volunteering?",
"translation": "🇷🇺 Что такое волонтёрство?",
"options": [
"A — Paid community work",
"B — Mandatory government service",
"C — Working for good causes without payment",
"D — Part-time employment for charities"
],
"answer": 2,
"explanation": (
"✅ *Верно — C!*\n\n"
"📖 Volunteering is working for good causes without payment. There are many benefits to volunteering, including meeting new people and helping make your community a better place.\n\n"
"🇷🇺 *Перевод:* Волонтёрство — работа на благо общества без оплаты."
),
},
{
"question": "TRUE or FALSE?\nUlster fry is a traditional food in Wales.",
"translation": "🇷🇺 Верно или нет?\nАльстерская жарёнка — традиционное блюдо Уэльса.",
"options": ["TRUE", "FALSE"],
"answer": 1,
"explanation": (
"❌ *Неверно! / False!*\n\n"
"📖 Ulster fry is a traditional food in Northern Ireland. It is a fried meal with bacon, eggs, sausage, black pudding, white pudding, tomatoes, mushrooms, soda bread and potato bread.\n\n"
"🇷🇺 *Перевод:* Альстерская жарёнка — традиционное блюдо Северной Ирландии, а не Уэльса."
),
},
{
"question": "Which of the following statements is correct about Thomas Hardy?",
"translation": "🇷🇺 Какое утверждение верно о Томасе Харди?",
"options": [
"A — Thomas Hardy wrote Far from the Madding Crowd and Jude the Obscure",
"B — Thomas Hardy wrote The Heart of the Matter and Brighton Rock"
],
"answer": 0,
"explanation": (
"✅ *Верно — A!*\n\n"
"📖 Thomas Hardy's best-known novels include Far from the Madding Crowd and Jude the Obscure. Graham Greene's novels include The Heart of the Matter and Brighton Rock.\n\n"
"🇷🇺 *Перевод:* «Вдали от безумной толпы» и «Джуд Незаметный» — романы Томаса Харди."
),
},
{
"question": "How are local councils funded?",
"translation": "🇷🇺 Как финансируются местные советы?",
"options": [
"A — Through money raised from local fundraising events",
"B — Through donations from local people",
"C — By central government and local taxes",
"D — From local businesses"
],
"answer": 2,
"explanation": (
"✅ *Верно — C!*\n\n"
"📖 Towns, cities and rural areas in the UK are governed by democratically elected councils. These are funded by money from central government and by local taxes.\n\n"
"🇷🇺 *Перевод:* Местные советы финансируются центральным правительством и местными налогами."
),
},
{
"question": "TRUE or FALSE?\nWilliam Blake, Lord Byron and Robert Browning were all famous golfers.",
"translation": "🇷🇺 Верно или нет?\nУильям Блейк, лорд Байрон и Роберт Браунинг были знаменитыми гольфистами.",
"options": ["TRUE", "FALSE"],
"answer": 1,
"explanation": (
"❌ *Неверно! / False!*\n\n"
"📖 William Blake, Lord Byron and Robert Browning were all poets, not golfers.\n\n"
"🇷🇺 *Перевод:* Блейк, Байрон и Браунинг — поэты, а не гольфисты."
),
},
],

}


def split_explanation(explanation):
    """Returns (english_text, russian_text_or_None) — strips verdict line and splits by 🇷🇺"""
    lines = explanation.strip().split("\n")
    eng_lines = []
    rus_lines = []
    for line in lines[1:]:  # skip first ✅/❌ verdict line
        s = line.strip()
        if not s:
            continue
        if s.startswith("🇷🇺"):
            rus_lines.append(s)
        else:
            eng_lines.append(s)
    eng = "\n".join(eng_lines).strip()
    rus = "\n".join(rus_lines).strip() if rus_lines else None
    return eng, rus


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Test 1", callback_data="test_1"),
         InlineKeyboardButton("📝 Test 2", callback_data="test_2")],
        [InlineKeyboardButton("📝 Test 3", callback_data="test_3"),
         InlineKeyboardButton("📝 Test 4", callback_data="test_4")],
        [InlineKeyboardButton("📝 Test 5", callback_data="test_5"),
         InlineKeyboardButton("📝 Test 6", callback_data="test_6")],
        [InlineKeyboardButton("📝 Test 7", callback_data="test_7"),
         InlineKeyboardButton("📝 Test 8", callback_data="test_8")],
        [InlineKeyboardButton("📝 Test 9", callback_data="test_9"),
         InlineKeyboardButton("📝 Test 10", callback_data="test_10")],
        [InlineKeyboardButton("📝 Test 11", callback_data="test_11"),
         InlineKeyboardButton("📝 Test 12", callback_data="test_12")],
        [InlineKeyboardButton("📝 Test 13", callback_data="test_13"),
         InlineKeyboardButton("📝 Test 14", callback_data="test_14")],
        [InlineKeyboardButton("📝 Test 15", callback_data="test_15"),
         InlineKeyboardButton("📝 Test 16", callback_data="test_16")],
        [InlineKeyboardButton("📝 Test 17", callback_data="test_17")],
    ]
    await update.message.reply_text(
        "👋 Welcome to the *Life in the UK* Bot!\n\nSelect a test:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_menu(query):
    keyboard = [
        [InlineKeyboardButton("📝 Test 1", callback_data="test_1"),
         InlineKeyboardButton("📝 Test 2", callback_data="test_2")],
        [InlineKeyboardButton("📝 Test 3", callback_data="test_3"),
         InlineKeyboardButton("📝 Test 4", callback_data="test_4")],
        [InlineKeyboardButton("📝 Test 5", callback_data="test_5"),
         InlineKeyboardButton("📝 Test 6", callback_data="test_6")],
        [InlineKeyboardButton("📝 Test 7", callback_data="test_7"),
         InlineKeyboardButton("📝 Test 8", callback_data="test_8")],
        [InlineKeyboardButton("📝 Test 9", callback_data="test_9"),
         InlineKeyboardButton("📝 Test 10", callback_data="test_10")],
        [InlineKeyboardButton("📝 Test 11", callback_data="test_11"),
         InlineKeyboardButton("📝 Test 12", callback_data="test_12")],
        [InlineKeyboardButton("📝 Test 13", callback_data="test_13"),
         InlineKeyboardButton("📝 Test 14", callback_data="test_14")],
        [InlineKeyboardButton("📝 Test 15", callback_data="test_15"),
         InlineKeyboardButton("📝 Test 16", callback_data="test_16")],
        [InlineKeyboardButton("📝 Test 17", callback_data="test_17")],
    ]
    await query.edit_message_text(
        "👋 Welcome to the *Life in the UK* Bot!\n\nSelect a test:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def send_question(query, context):
    test_num = context.user_data["test"]
    q_index = context.user_data["question"]
    question = TESTS[test_num][q_index]
    total = len(TESTS[test_num])

    options_text = "\n".join([f"*{chr(65+i)})* {opt}" for i, opt in enumerate(question["options"])])

    keyboard = [
        [InlineKeyboardButton(chr(65+i), callback_data=str(i)) for i in range(len(question["options"]))],
        [InlineKeyboardButton("🇷🇺 Show translation", callback_data="show_q_tr")],
    ]

    await query.edit_message_text(
        f"📝 *Question {q_index + 1} of {total}* — Test {test_num}\n\n"
        f"*{question['question']}*\n\n"
        f"{options_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await show_menu(query)

    elif data.startswith("test_"):
        test_num = int(data.split("_")[1])
        context.user_data["test"] = test_num
        context.user_data["question"] = 0
        context.user_data["score"] = 0
        await send_question(query, context)

    elif data == "next":
        await send_question(query, context)

    elif data == "show_q_tr":
        # Show Russian translation of question, remove translation button
        test_num = context.user_data["test"]
        q_index = context.user_data["question"]
        question = TESTS[test_num][q_index]
        total = len(TESTS[test_num])
        options_text = "\n".join([f"*{chr(65+i)})* {opt}" for i, opt in enumerate(question["options"])])
        keyboard = [[InlineKeyboardButton(chr(65+i), callback_data=str(i)) for i in range(len(question["options"]))]]
        await query.edit_message_text(
            f"📝 *Question {q_index + 1} of {total}* — Test {test_num}\n\n"
            f"*{question['question']}*\n"
            f"_{question['translation']}_\n\n"
            f"{options_text}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "show_ans_tr":
        # Show Russian translation of answer, remove translation button
        test_num = context.user_data["test"]
        q_index = context.user_data["question"] - 1
        chosen = context.user_data.get("last_chosen", 0)
        question = TESTS[test_num][q_index]
        correct = question["answer"]
        correct_option = question["options"][correct]
        eng_part, rus_part = split_explanation(question["explanation"])

        if chosen == correct:
            result_text = f"✅ *Correct!*\nCorrect answer: *{correct_option}*\n\n📖 {eng_part}"
        else:
            result_text = f"❌ *Incorrect!*\nCorrect answer: *{correct_option}*\n\n📖 {eng_part}"

        if rus_part:
            result_text += f"\n\n{rus_part}"

        total = len(TESTS[test_num])
        next_index = context.user_data["question"]
        if next_index < total:
            keyboard = [[InlineKeyboardButton("➡️ Next question", callback_data="next")]]
        else:
            keyboard = [[InlineKeyboardButton("🏠 Main menu", callback_data="menu")]]
        await query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.isdigit():
        chosen = int(data)
        test_num = context.user_data["test"]
        q_index = context.user_data["question"]
        question = TESTS[test_num][q_index]
        correct = question["answer"]
        correct_option = question["options"][correct]
        context.user_data["last_chosen"] = chosen

        eng_part, rus_part = split_explanation(question["explanation"])

        if chosen == correct:
            context.user_data["score"] += 1
            result_text = f"✅ *Correct!*\nCorrect answer: *{correct_option}*\n\n📖 {eng_part}"
        else:
            result_text = f"❌ *Incorrect!*\nCorrect answer: *{correct_option}*\n\n📖 {eng_part}"

        context.user_data["question"] += 1
        total = len(TESTS[test_num])
        next_index = context.user_data["question"]

        keyboard = []
        if rus_part:
            keyboard.append([InlineKeyboardButton("🇷🇺 Show translation", callback_data="show_ans_tr")])

        if next_index < total:
            keyboard.append([InlineKeyboardButton("➡️ Next question", callback_data="next")])
            await query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        else:
            score = context.user_data["score"]
            passed = "🎉 *PASSED!*" if score >= 18 else "😔 *Not passed. Try again!*"
            keyboard.append([InlineKeyboardButton("🏠 Main menu", callback_data="menu")])
            await query.edit_message_text(
                f"{result_text}\n\n━━━━━━━━━━━━━━━\n"
                f"📊 *Result: {score} out of {total}*\n{passed}\n_(You need 18 out of 24 to pass)_",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()


if __name__ == "__main__":
    main()
