import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8669298087:AAH1Oyl-M47xwLzuUvaq2lbSNkIsM5PyLQQ"

logging.basicConfig(level=logging.INFO)

TESTS = {
    1: [
        {
            "question": "TRUE or FALSE?\nCharles Dickens was famous for writing musicals.",
            "translation": "🇷🇺 Верно или нет?\nЧарльз Диккенс был известен написанием мюзиклов.",
            "options": ["TRUE", "FALSE"],
            "answer": 1,
            "explanation": (
                "❌ *Неверно! / False!*\n\n"
                "📖 *Из книги:* Charles Dickens wrote a number of famous novels, including Oliver Twist and Great Expectations. Many of his stories are still popular today.\n\n"
                "🇷🇺 *Перевод:* Чарльз Диккенс написал множество известных романов, включая «Оливер Твист» и «Большие надежды». Многие его истории популярны до сих пор."
            )
        },
        {
            "question": "TRUE or FALSE?\nA General Election is held at least every five years.",
            "translation": "🇷🇺 Верно или нет?\nВсеобщие выборы проводятся не реже одного раза в пять лет.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "✅ *Верно! / True!*\n\n"
                "📖 *Из книги:* A General Election is held at least every five years. The Prime Minister can ask the King to hold an election sooner if they want to.\n\n"
                "🇷🇺 *Перевод:* Всеобщие выборы проводятся не реже одного раза в пять лет. Премьер-министр может попросить короля назначить выборы раньше."
            )
        },
        {
            "question": "TRUE or FALSE?\nIn the UK you are expected to respect the rights of others to have their own opinions.",
            "translation": "🇷🇺 Верно или нет?\nВ Великобритании вы обязаны уважать право других иметь собственное мнение.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "✅ *Верно! / True!*\n\n"
                "📖 *Из книги:* There are responsibilities and freedoms which are shared by all those living in the UK. These include respecting the rights of others to have their own opinions.\n\n"
                "🇷🇺 *Перевод:* Все живущие в Великобритании разделяют общие обязанности и свободы. Сюда входит уважение права других иметь собственное мнение."
            )
        },
        {
            "question": "TRUE or FALSE?\nOn the 1st of April, people in the UK play jokes on each other until midday.",
            "translation": "🇷🇺 Верно или нет?\n1 апреля люди в Великобритании разыгрывают друг друга до полудня.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "✅ *Верно! / True!*\n\n"
                "📖 *Из книги:* April Fool's Day is the 1st of April. People play jokes on each other until midday. After midday, it is considered bad luck to play a joke.\n\n"
                "🇷🇺 *Перевод:* День дурака — 1 апреля. Люди разыгрывают друг друга до полудня. После полудня розыгрыш считается плохой приметой."
            )
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое из следующих утверждений верно?",
            "options": [
                "A — Shakespeare wrote 'To be or not to be'",
                "B — Shakespeare wrote 'We shall fight on the beaches'"
            ],
            "answer": 0,
            "explanation": (
                "✅ *Верно — A!*\n\n"
                "📖 *Из книги:* William Shakespeare wrote 'To be or not to be' in the play Hamlet. 'We shall fight on the beaches' was said by Winston Churchill during World War II.\n\n"
                "🇷🇺 *Перевод:* Шекспир написал «Быть или не быть» в пьесе «Гамлет». «Мы будем сражаться на пляжах» — слова Уинстона Черчилля во время Второй мировой войны."
            )
        },
        {
            "question": "How can you reduce your carbon footprint?",
            "translation": "🇷🇺 Как можно уменьшить свой углеродный след?",
            "options": [
                "A — Shop locally for products",
                "B — Buy duty-free products when abroad",
                "C — Do all your shopping online",
                "D — Drive to the supermarket"
            ],
            "answer": 0,
            "explanation": (
                "✅ *Верно — A!*\n\n"
                "📖 *Из книги:* You can reduce your carbon footprint by shopping locally, which reduces the need for transportation and lowers CO2 emissions.\n\n"
                "🇷🇺 *Перевод:* Вы можете уменьшить углеродный след, делая покупки у местных производителей — это снижает потребность в транспортировке и выбросы CO2."
            )
        },
        {
            "question": "Which of the following statements is correct?",
            "translation": "🇷🇺 Какое из следующих утверждений верно?",
            "options": [
                "A — The civil service largely consists of political appointees",
                "B — The civil service is politically neutral"
            ],
            "answer": 1,
            "explanation": (
                "✅ *Верно — B!*\n\n"
                "📖 *Из книги:* Civil servants are managers and administrators who carry out government policy. They are politically neutral and do not support any political party.\n\n"
                "🇷🇺 *Перевод:* Государственные служащие — это менеджеры и администраторы, проводящие государственную политику. Они политически нейтральны и не поддерживают ни одну партию."
            )
        },
        {
            "question": "Which TWO are Protestant Christian groups in the UK?",
            "translation": "🇷🇺 Какие ДВЕ из перечисленных групп являются протестантскими христианскими группами в Великобритании?",
            "options": [
                "A — Methodists and Roman Catholics",
                "B — Baptists and Methodists",
                "C — Baptists and Hindus",
                "D — Roman Catholics and Sikhs"
            ],
            "answer": 1,
            "explanation": (
                "✅ *Верно — B!*\n\n"
                "📖 *Из книги:* Baptists and Methodists are Protestant Christian groups in the UK. Other Protestant groups include Presbyterians and Quakers. Roman Catholics are Christian but not Protestant.\n\n"
                "🇷🇺 *Перевод:* Баптисты и методисты — протестантские христианские группы в Великобритании. Другие протестанты — пресвитериане и квакеры. Католики — христиане, но не протестанты."
            )
        },
        {
            "question": "What is the role of a jury at a court trial?",
            "translation": "🇷🇺 Какова роль присяжных на судебном процессе?",
            "options": [
                "A — To decide whether evidence should be allowed to be heard",
                "B — To decide the sentence that the accused should be given",
                "C — To decide who the judge should be",
                "D — To decide a verdict based on what they have heard"
            ],
            "answer": 3,
            "explanation": (
                "✅ *Верно — D!*\n\n"
                "📖 *Из книги:* A jury is made up of members of the public. The jury has to listen to the evidence presented at the trial and decide a verdict of 'guilty' or 'not guilty' based on what they have heard. The judge decides the sentence.\n\n"
                "🇷🇺 *Перевод:* Присяжные — это обычные граждане. Они слушают доказательства и выносят вердикт «виновен» или «невиновен». Приговор выносит судья."
            )
        },
        {
            "question": "Which form of comedy became famous in the 19th century?",
            "translation": "🇷🇺 Какая форма комедии стала знаменитой в 19 веке?",
            "options": [
                "A — Sitcoms",
                "B — Satirical magazines",
                "C — Progressive comedy",
                "D — Court jesters"
            ],
            "answer": 1,
            "explanation": (
                "✅ *Верно — B!*\n\n"
                "📖 *Из книги:* In the 19th century, satirical magazines became increasingly popular. The most famous was Punch, which was published for the first time in 1841.\n\n"
                "🇷🇺 *Перевод:* В 19 веке сатирические журналы стали всё более популярными. Самым известным был Punch, впервые опубликованный в 1841 году."
            )
        },
        {
            "question": "During which period did John Barbour and other poets begin to write poetry in the Scots language?",
            "translation": "🇷🇺 В какой период Джон Барбур и другие поэты начали писать стихи на шотландском языке?",
            "options": [
                "A — The 19th century",
                "B — The 20th century",
                "C — The Middle Ages",
                "D — The Bronze Age"
            ],
            "answer": 2,
            "explanation": (
                "✅ *Верно — C!*\n\n"
                "📖 *Из книги:* In the Middle Ages, a number of poets began to write in the Scots language. One example is John Barbour, who wrote The Bruce about the Battle of Bannockburn.\n\n"
                "🇷🇺 *Перевод:* В Средние века ряд поэтов начал писать на шотландском языке. Один из примеров — Джон Барбур, написавший «Брюс» о битве при Баннокберне."
            )
        },
        {
            "question": "What are Beowulf, The Tyger and She Walks in Beauty?",
            "translation": "🇷🇺 Что такое «Беовульф», «Тигр» и «Она идёт во всей красе»?",
            "options": [
                "A — Plays",
                "B — Films",
                "C — Poems",
                "D — Novels"
            ],
            "answer": 2,
            "explanation": (
                "✅ *Верно — C!*\n\n"
                "📖 *Из книги:* Beowulf is an Anglo-Saxon poem. The Tyger was written by William Blake and She Walks in Beauty by Lord Byron. All three are famous poems in British literature.\n\n"
                "🇷🇺 *Перевод:* «Беовульф» — англосаксонская поэма. «Тигр» написал Уильям Блейк, «Она идёт во всей красе» — лорд Байрон. Все три — известные поэмы британской литературы."
            )
        },
        {
            "question": "What is a jury made up of?",
            "translation": "🇷🇺 Из кого состоят присяжные?",
            "options": [
                "A — People working in high-powered jobs",
                "B — People randomly chosen from the electoral register",
                "C — People who have submitted an application form",
                "D — People who are members of political parties"
            ],
            "answer": 1,
            "explanation": (
                "✅ *Верно — B!*\n\n"
                "📖 *Из книги:* A jury is made up of members of the public who are randomly chosen from the electoral register.\n\n"
                "🇷🇺 *Перевод:* Присяжные — это члены общества, случайно выбранные из списка избирателей (electoral register)."
            )
        },
        {
            "question": "Which TWO fought in wars against Napoleon?",
            "translation": "🇷🇺 Кто из перечисленных ДВУХ воевал против Наполеона?",
            "options": [
                "A — Winston Churchill and the Duke of Wellington",
                "B — Margaret Thatcher and the Duke of Wellington",
                "C — Margaret Thatcher and Admiral Nelson",
                "D — Admiral Nelson and the Duke of Wellington"
            ],
            "answer": 3,
            "explanation": (
                "✅ *Верно — D!*\n\n"
                "📖 *Из книги:* Admiral Nelson commanded the British fleet at the Battle of Trafalgar in 1805. The Duke of Wellington defeated Napoleon at the Battle of Waterloo in 1815.\n\n"
                "🇷🇺 *Перевод:* Адмирал Нельсон командовал британским флотом в битве при Трафальгаре в 1805 году. Герцог Веллингтон разгромил Наполеона при Ватерлоо в 1815 году."
            )
        },
        {
            "question": "After slavery was abolished in the British Empire, more than 2 million migrants came from which TWO countries?",
            "translation": "🇷🇺 После отмены рабства в Британской империи более 2 миллионов мигрантов приехали из каких ДВУХ стран?",
            "options": [
                "A — India and China",
                "B — Russia and China",
                "C — India and Australia",
                "D — Russia and Australia"
            ],
            "answer": 0,
            "explanation": (
                "✅ *Верно — A!*\n\n"
                "📖 *Из книги:* After 1833, 2 million Indian and Chinese workers were employed to replace the freed slaves in the British Empire.\n\n"
                "🇷🇺 *Перевод:* После 1833 года 2 миллиона рабочих из Индии и Китая были наняты на замену освобождённым рабам в Британской империи."
            )
        },
        {
            "question": "Which group of adults is NOT eligible to vote in all UK elections?",
            "translation": "🇷🇺 Какая группа взрослых НЕ имеет права голосовать на всех выборах в Великобритании?",
            "options": [
                "A — Citizens of the USA",
                "B — Adult citizens of the UK",
                "C — Qualifying Commonwealth citizens resident in the UK",
                "D — Citizens of Ireland resident in the UK"
            ],
            "answer": 0,
            "explanation": (
                "✅ *Верно — A!*\n\n"
                "📖 *Из книги:* Adult citizens of the UK, qualifying citizens of the Commonwealth and citizens of the Irish Republic who are resident in the UK can vote in all public elections. Citizens of other countries cannot.\n\n"
                "🇷🇺 *Перевод:* Голосовать могут граждане UK, квалифицированные граждане Содружества и граждане Ирландии, проживающие в UK. Граждане других стран, включая США, не могут."
            )
        },
        {
            "question": "Which statement about Big Ben is correct?",
            "translation": "🇷🇺 Какое утверждение о Биг Бене верно?",
            "options": [
                "A — Big Ben is a mountain in eastern England",
                "B — Big Ben is the nickname for the great bell of the clock at the Houses of Parliament"
            ],
            "answer": 1,
            "explanation": (
                "✅ *Верно — B!*\n\n"
                "📖 *Из книги:* Big Ben is the nickname for the great bell of the clock at the Houses of Parliament in London. Many people call the clock Big Ben as well.\n\n"
                "🇷🇺 *Перевод:* Биг Бен — прозвище большого колокола часов в здании Парламента в Лондоне. Многие также называют Биг Беном сами часы."
            )
        },
        {
            "question": "Bobby Moore is famous for his achievements in which sport?",
            "translation": "🇷🇺 Бобби Мур известен своими достижениями в каком виде спорта?",
            "options": [
                "A — Football",
                "B — Rugby union",
                "C — Horse racing",
                "D — Motor racing"
            ],
            "answer": 0,
            "explanation": (
                "✅ *Верно — A!*\n\n"
                "📖 *Из книги:* Bobby Moore captained the England football team that won the World Cup in 1966.\n\n"
                "🇷🇺 *Перевод:* Бобби Мур был капитаном сборной Англии по футболу, выигравшей Чемпионат мира в 1966 году."
            )
        },
        {
            "question": "TRUE or FALSE?\nIf you are a qualifying Commonwealth citizen resident in the UK, you can vote in all public elections.",
            "translation": "🇷🇺 Верно или нет?\nЕсли вы являетесь квалифицированным гражданином Содружества, проживающим в Великобритании, вы можете голосовать на всех публичных выборах.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "✅ *Верно! / True!*\n\n"
                "📖 *Из книги:* Qualifying citizens of the Commonwealth who are resident in the UK can vote in all public elections.\n\n"
                "🇷🇺 *Перевод:* Квалифицированные граждане Содружества, проживающие в Великобритании, могут голосовать на всех публичных выборах."
            )
        },
        {
            "question": "Which TWO of the following were important 20th-century inventors?",
            "translation": "🇷🇺 Кто из перечисленных ДВУХ был важным изобретателем 20 века?",
            "options": [
                "A — Alan Turing and Tim Berners-Lee",
                "B — Tim Berners-Lee and Isambard Kingdom Brunel",
                "C — George Stephenson and Isambard Brunel",
                "D — Alan Turing and George Stephenson"
            ],
            "answer": 0,
            "explanation": (
                "✅ *Верно — A!*\n\n"
                "📖 *Из книги:* Alan Turing (1912–54) invented a theoretical mathematical device called the Turing Machine, contributing to the development of the modern-day computer. Tim Berners-Lee invented the World Wide Web.\n\n"
                "🇷🇺 *Перевод:* Алан Тьюринг изобрёл теоретическую машину Тьюринга, что привело к созданию современного компьютера. Тим Бернерс-Ли изобрёл Всемирную паутину (WWW)."
            )
        },
        {
            "question": "Which statement is correct about applying for UK citizenship?",
            "translation": "🇷🇺 Какое утверждение верно относительно подачи заявки на гражданство Великобритании?",
            "options": [
                "A — When you apply you can choose which laws to accept",
                "B — When you apply to become a permanent resident, you agree to accept the responsibilities, values and traditions of the UK"
            ],
            "answer": 1,
            "explanation": (
                "✅ *Верно — B!*\n\n"
                "📖 *Из книги:* Applying to become a permanent resident or citizen of the UK is an important decision. You will be agreeing to accept the values and responsibilities which go with permanent residence and the commitment.\n\n"
                "🇷🇺 *Перевод:* Подача заявки на постоянное проживание или гражданство UK — важное решение. Вы соглашаетесь принять ценности и обязанности, связанные с постоянным проживанием."
            )
        },
        {
            "question": "Which TWO are plays by William Shakespeare?",
            "translation": "🇷🇺 Какие ДВЕ из перечисленных пьес написал Уильям Шекспир?",
            "options": [
                "A — A Midsummer Night's Dream and Oliver Twist",
                "B — Romeo and Juliet and Oliver Twist",
                "C — A Midsummer Night's Dream and Romeo and Juliet",
                "D — Pride and Prejudice and Romeo and Juliet"
            ],
            "answer": 2,
            "explanation": (
                "✅ *Верно — C!*\n\n"
                "📖 *Из книги:* Among the many plays that Shakespeare wrote are A Midsummer Night's Dream and Romeo and Juliet. Oliver Twist is by Dickens; Pride and Prejudice is by Jane Austen.\n\n"
                "🇷🇺 *Перевод:* Среди пьес Шекспира — «Сон в летнюю ночь» и «Ромео и Джульетта». «Оливер Твист» написал Диккенс; «Гордость и предубеждение» — Джейн Остин."
            )
        },
        {
            "question": "Which TWO commemorations are held in November each year?",
            "translation": "🇷🇺 Какие ДВА памятных события отмечаются в ноябре каждого года?",
            "options": [
                "A — Remembrance Day and Bonfire Night",
                "B — Valentine's Day and Remembrance Day",
                "C — Valentine's Day and Father's Day",
                "D — Father's Day and Bonfire Night"
            ],
            "answer": 0,
            "explanation": (
                "✅ *Верно — A!*\n\n"
                "📖 *Из книги:* Bonfire Night is on 5 November, commemorating those who died fighting for the UK and its allies. Remembrance Day is on 11 November.\n\n"
                "🇷🇺 *Перевод:* Ночь костров — 5 ноября. День памяти — 11 ноября. День Валентина — февраль, День отца — июнь."
            )
        },
        {
            "question": "TRUE or FALSE?\nAll young people in the UK are sent a National Insurance number just before their 16th birthday.",
            "translation": "🇷🇺 Верно или нет?\nВсем молодым людям в Великобритании отправляют номер национального страхования незадолго до их 16-летия.",
            "options": ["TRUE", "FALSE"],
            "answer": 0,
            "explanation": (
                "✅ *Верно! / True!*\n\n"
                "📖 *Из книги:* All young people in the UK are sent a National Insurance number just before their 16th birthday. It makes sure that the tax and National Insurance Contributions you pay are recorded against your name.\n\n"
                "🇷🇺 *Перевод:* Все молодые люди в UK получают номер национального страхования до 16 лет. Это нужно чтобы налоги и взносы записывались на ваше имя."
            )
        }
    ]
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📝 Practice Test 1", callback_data="test_1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Привет! Я помогу тебе подготовиться к тесту *Life in the UK*!\n\n"
        "Выбери тест чтобы начать:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("test_"):
        test_num = int(data.split("_")[1])
        context.user_data["test"] = test_num
        context.user_data["question"] = 0
        context.user_data["score"] = 0
        await send_question(query, context)

    elif data.startswith("answer_"):
        chosen = int(data.split("_")[1])
        test_num = context.user_data["test"]
        q_index = context.user_data["question"]
        question = TESTS[test_num][q_index]
        correct = question["answer"]
        explanation = question["explanation"]

        if chosen == correct:
            context.user_data["score"] += 1
            result_text = f"✅ *ПРАВИЛЬНО!*\n\n{explanation}"
        else:
            correct_option = question["options"][correct]
            result_text = f"❌ *НЕВЕРНО!*\nПравильный ответ: *{correct_option}*\n\n{explanation}"

        context.user_data["question"] += 1
        total = len(TESTS[test_num])
        next_index = context.user_data["question"]

        if next_index < total:
            keyboard = [[InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                result_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            score = context.user_data["score"]
            passed = "🎉 *СДАЛ(А)!*" if score >= 18 else "😔 *Не сдал(а). Попробуй ещё раз!*"
            keyboard = [[InlineKeyboardButton("🔄 Пройти ещё раз", callback_data="test_1")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"{result_text}\n\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📊 *Результат: {score} из {total}*\n"
                f"{passed}\n"
                f"_(Для сдачи нужно 18 из 24)_",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )

    elif data == "next":
        await send_question(query, context)


async def send_question(query, context):
    test_num = context.user_data["test"]
    q_index = context.user_data["question"]
    question = TESTS[test_num][q_index]
    total = len(TESTS[test_num])

    options_text = "\n".join(
    [f"*{chr(65+i)})* {opt}" for i, opt in enumerate(question["options"])]
)

keyboard = [
    [InlineKeyboardButton(chr(65+i), callback_data=str(i))
     for i in range(len(question["options"]))]
]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
    f"📝 *Вопрос {q_index + 1} из {total}*\n\n"
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
