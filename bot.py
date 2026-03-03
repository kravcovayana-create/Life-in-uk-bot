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
