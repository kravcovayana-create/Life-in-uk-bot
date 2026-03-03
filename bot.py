import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8669298087:AAH1Oyl-M47xwLzuUvaq2lbSNkIsM5PyLQQ"

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
                "\U0001f4d6 *Из книги:* Charles Dickens wrote a number of famous novels, including Oliver Twist and Great Expectations.\n\n"
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
                "\U0001f4d6 *Из книги:* A General Election is held at least every five years.\n\n"
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
                "\U0001f4d6 *Из книги:* There are responsibilities and freedoms which are shared by all those living in the UK.\n\n"
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
                "\U0001f4d6 *Из книги:* April Fool\'s Day is the 1st of April. People play jokes on each other until midday.\n\n"
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
                "\U0001f4d6 *Из книги:* William Shakespeare wrote \'To be or not to be\' in the play Hamlet.\n\n"
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
                "\U0001f4d6 *Из книги:* You can reduce your carbon footprint by shopping locally.\n\n"
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
                "\U0001f4d6 *Из книги:* Civil servants are politically neutral and do not support any political party.\n\n"
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
                "\U0001f4d6 *Из книги:* Baptists and Methodists are Protestant Christian groups in the UK.\n\n"
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
                "\U0001f4d6 *Из книги:* The jury decides a verdict of \'guilty\' or \'not guilty\'. The judge decides the sentence.\n\n"
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
                "\U0001f4d6 *Из книги:* In the 19th century, satirical magazines became popular. The most famous was Punch, first published in 1841.\n\n"
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
                "\U0001f4d6 *Из книги:* In the Middle Ages, poets began to write in the Scots language. John Barbour wrote The Bruce about the Battle of Bannockburn.\n\n"
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
                "\U0001f4d6 *Из книги:* Beowulf is an Anglo-Saxon poem. The Tyger was written by William Blake and She Walks in Beauty by Lord Byron.\n\n"
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
                "\U0001f4d6 *Из книги:* A jury is made up of members of the public who are randomly chosen from the electoral register.\n\n"
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
                "\U0001f4d6 *Из книги:* Admiral Nelson commanded the British fleet at Trafalgar in 1805. The Duke of Wellington defeated Napoleon at Waterloo in 1815.\n\n"
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
                "\U0001f4d6 *Из книги:* After 1833, 2 million Indian and Chinese workers were employed to replace the freed slaves.\n\n"
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
                "\U0001f4d6 *Из книги:* Adult citizens of the UK, qualifying Commonwealth citizens and Irish citizens resident in the UK can vote. Citizens of other countries cannot.\n\n"
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
                "\U0001f4d6 *Из книги:* Big Ben is the nickname for the great bell of the clock at the Houses of Parliament in London.\n\n"
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
                "\U0001f4d6 *Из книги:* Bobby Moore captained the England football team that won the World Cup in 1966.\n\n"
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
                "\U0001f4d6 *Из книги:* Qualifying citizens of the Commonwealth who are resident in the UK can vote in all public elections.\n\n"
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
                "\U0001f4d6 *Из книги:* Alan Turing contributed to the development of the modern computer. Tim Berners-Lee invented the World Wide Web.\n\n"
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
                "\U0001f4d6 *Из книги:* Applying to become a permanent resident or citizen of the UK means agreeing to accept the values and responsibilities.\n\n"
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
                "\U0001f4d6 *Из книги:* Among Shakespeare\'s plays are A Midsummer Night\'s Dream and Romeo and Juliet.\n\n"
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
                "\U0001f4d6 *Из книги:* Bonfire Night is on 5 November. Remembrance Day is on 11 November.\n\n"
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
                "\U0001f4d6 *Из книги:* All young people in the UK are sent a National Insurance number just before their 16th birthday.\n\n"
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
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("\U0001f4dd Test 1", callback_data="test_1"),
         InlineKeyboardButton("\U0001f4dd Test 2", callback_data="test_2"),
         InlineKeyboardButton("\U0001f4dd Test 3", callback_data="test_3")],
        [InlineKeyboardButton("\U0001f4dd Test 4", callback_data="test_4"),
         InlineKeyboardButton("\U0001f4dd Test 5", callback_data="test_5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "\U0001f44b Привет! Я помогу тебе подготовиться к тесту *Life in the UK*!\n\n"
        "Выбери тест чтобы начать:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def show_menu(query):
    keyboard = [
        [InlineKeyboardButton("\U0001f4dd Test 1", callback_data="test_1"),
         InlineKeyboardButton("\U0001f4dd Test 2", callback_data="test_2"),
         InlineKeyboardButton("\U0001f4dd Test 3", callback_data="test_3")],
        [InlineKeyboardButton("\U0001f4dd Test 4", callback_data="test_4"),
         InlineKeyboardButton("\U0001f4dd Test 5", callback_data="test_5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "\U0001f3e0 *Главное меню*\n\nВыбери тест:",
        reply_markup=reply_markup,
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

    elif data.isdigit():
        chosen = int(data)
        test_num = context.user_data["test"]
        q_index = context.user_data["question"]
        question = TESTS[test_num][q_index]
        correct = question["answer"]
        explanation = question["explanation"]

        correct_option = question["options"][correct]

        if chosen == correct:
            context.user_data["score"] += 1
            result_text = (
                f"✅ *Правильно!*\n"
                f"Правильный ответ: *{correct_option}*\n\n"
                f"{explanation}"
            )
        else:
            result_text = (
                f"❌ *Неверно!*\n"
                f"Правильный ответ: *{correct_option}*\n\n"
                f"{explanation}"
            )

        context.user_data["question"] += 1
        total = len(TESTS[test_num])
        next_index = context.user_data["question"]

        if next_index < total:
            keyboard = [[InlineKeyboardButton("\u27a1\ufe0f Следующий вопрос", callback_data="next")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                result_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            score = context.user_data["score"]
            passed = "\U0001f389 *СДАЛ(А)!*" if score >= 18 else "\U0001f614 *Не сдал(а). Попробуй ещё раз!*"
            keyboard = [[InlineKeyboardButton("\U0001f3e0 Главное меню", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"{result_text}\n\n"
                f"━━━━━━━━━━━━━━━\n"
                f"\U0001f4ca *Результат: {score} из {total}*\n"
                f"{passed}\n"
                f"_(Для сдачи нужно 18 из 24)_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )


async def send_question(query, context):
    test_num = context.user_data["test"]
    q_index = context.user_data["question"]
    question = TESTS[test_num][q_index]
    total = len(TESTS[test_num])

    options_text = "\n".join(
        [f"*{chr(65+i)})* {opt}" for i, opt in enumerate(question["options"])]
    )

    keyboard = [[InlineKeyboardButton(chr(65+i), callback_data=str(i)) for i in range(len(question["options"]))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"\U0001f4dd *Вопрос {q_index + 1} из {total}* — Тест {test_num}\n\n"
        f"*{question['question']}*\n"
        f"_{question['translation']}_\n\n"
        f"{options_text}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()


if __name__ == "__main__":
    main()
