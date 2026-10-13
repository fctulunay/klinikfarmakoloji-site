from batch1 import D
CARDS = {}

# Free meals for doctors: the hospitality goes to the doctor, the bill to the patient (cover poster + infographic card)
T = {
 'en': ("NEWS", "Free meals for doctors", "The doctor gets the meal, the patient gets the bill"),
 'de': ("NACHRICHTEN", "Gratisessen für Ärzte", "Die Bewirtung bekommt der Arzt, die Rechnung der Patient"),
 'es': ("NOTICIAS", "Comidas gratis para médicos", "La invitación para el médico, la factura para el paciente"),
 'ru': ("НОВОСТИ", "Бесплатные обеды для врачей", "Угощение получает врач, счёт оплачивает пациент"),
 'zh': ("新闻", "给医生的免费餐", "宴请归医生，账单归患者"),
 'hi': ("समाचार", "डॉक्टरों के लिए मुफ़्त भोजन", "दावत डॉक्टर की, बिल मरीज़ का"),
 'ja': ("ニュース", "医師への無料の食事", "もてなしは医師に、請求書は患者に"),
}
CARDS['b26_yemek_kapak'] = ('navy', {l: D(*v) for l, v in T.items()})

S = {
 'en': [("93 studies", "Cochrane 2026: gifts and payments linked to more and less appropriate prescribing"), ("$2,016", "Washington: dinner for 3, plus $1,000 to the speaker (Novartis, 2013)"), ("$3,127", "Iowa: dinner for 3 (Novartis, 2013)"), ("$678M", "Novartis 2020 settlement over sham speaker programs")],
 'de': [("93 Studien", "Cochrane 2026: Geschenke und Zahlungen gehen mit mehr und weniger angemessenen Verordnungen einher"), ("2.016 $", "Washington: Essen für 3 Personen, dazu 1.000 $ für den Referenten (Novartis, 2013)"), ("3.127 $", "Iowa: Essen für 3 Personen (Novartis, 2013)"), ("678 Mio. $", "Novartis-Vergleich 2020 wegen Schein-Referentenprogrammen")],
 'es': [("93 estudios", "Cochrane 2026: regalos y pagos asociados a más prescripciones y menos adecuadas"), ("2.016 $", "Washington: cena para 3, más 1.000 $ al ponente (Novartis, 2013)"), ("3.127 $", "Iowa: cena para 3 (Novartis, 2013)"), ("678 M$", "Acuerdo de Novartis de 2020 por programas de ponentes ficticios")],
 'ru': [("93 исследования", "Cochrane 2026: подарки и выплаты связаны с более частыми и менее обоснованными назначениями"), ("2 016 $", "Вашингтон: ужин на троих и ещё 1 000 $ докладчику (Novartis, 2013)"), ("3 127 $", "Айова: ужин на троих (Novartis, 2013)"), ("678 млн $", "Соглашение Novartis 2020 года по фиктивным программам докладчиков")],
 'zh': [("93项研究", "Cochrane 2026：礼品和付款与更多、更不恰当的处方相关"), ("2016美元", "华盛顿：3人晚餐，另付讲者1000美元（诺华，2013年）"), ("3127美元", "艾奥瓦：3人晚餐（诺华，2013年）"), ("6.78亿美元", "诺华2020年就虚假讲者项目达成和解")],
 'hi': [("93 अध्ययन", "Cochrane 2026: उपहार और भुगतान अधिक और कम उपयुक्त पर्चों से जुड़े"), ("2,016 $", "वॉशिंगटन: 3 लोगों का भोजन, वक्ता को अलग से 1,000 $ (Novartis, 2013)"), ("3,127 $", "आयोवा: 3 लोगों का भोजन (Novartis, 2013)"), ("67.8 करोड़ $", "फ़र्ज़ी वक्ता कार्यक्रमों पर Novartis का 2020 समझौता")],
 'ja': [("93件の研究", "Cochrane 2026：贈答品や支払いは、より多く、より不適切な処方と関連"), ("2,016ドル", "ワシントン：3人分の夕食、講演者に別途1,000ドル（ノバルティス、2013年）"), ("3,127ドル", "アイオワ：3人分の夕食（ノバルティス、2013年）"), ("6億7800万ドル", "偽の講演会プログラムをめぐるノバルティスの2020年和解")],
}
P = {
 'en': [("New York:", "Masa, Daniel, Le Bernardin and Eleven Madison Park appeared in the 2020 settlement announcement."),
        ("Turkey, more than meals:", "phones, TVs, computers, white goods and congress support including spouses."),
        ("Even small meals:", "a single company meal under $20 was linked to more prescribing of the promoted drug (JAMA Intern Med 2016)."),
        ("Caution:", "an association is not, in every case, proof of causation or of legal bribery.")],
 'de': [("New York:", "Masa, Daniel, Le Bernardin und Eleven Madison Park wurden in der Vergleichsmitteilung von 2020 genannt."),
        ("Türkei, mehr als Essen:", "Telefone, Fernseher, Computer, Haushaltsgeräte und Kongressunterstützung mit Ehepartnern."),
        ("Schon kleine Essen:", "Ein einziges Firmenessen unter 20 $ ging mit häufigeren Verordnungen des beworbenen Medikaments einher (JAMA Intern Med 2016)."),
        ("Vorsicht:", "Ein Zusammenhang ist nicht in jedem Fall ein Beweis für Kausalität oder strafbare Bestechung.")],
 'es': [("Nueva York:", "Masa, Daniel, Le Bernardin y Eleven Madison Park aparecieron en el anuncio del acuerdo de 2020."),
        ("Turquía, más que comidas:", "teléfonos, televisores, ordenadores, electrodomésticos y apoyo a congresos con cónyuges."),
        ("Incluso comidas pequeñas:", "una sola comida de empresa de menos de 20 $ se asoció a más prescripción del fármaco promocionado (JAMA Intern Med 2016)."),
        ("Precaución:", "una asociación no es, en todos los casos, prueba de causalidad ni de soborno legal.")],
 'ru': [("Нью-Йорк:", "Masa, Daniel, Le Bernardin и Eleven Madison Park упомянуты в сообщении о соглашении 2020 года."),
        ("Турция, не только обеды:", "телефоны, телевизоры, компьютеры, бытовая техника и поддержка участия в конгрессах с супругами."),
        ("Даже недорогие обеды:", "один обед от компании дешевле 20 $ был связан с более частым назначением продвигаемого препарата (JAMA Intern Med 2016)."),
        ("Оговорка:", "связь не во всех случаях доказывает причинность или взятку в юридическом смысле.")],
 'zh': [("纽约：", "Masa、Daniel、Le Bernardin和Eleven Madison Park出现在2020年的和解公告中。"),
        ("土耳其，不止是餐饭：", "手机、电视、电脑、大型家电，以及携配偶参会的资助。"),
        ("即使是小餐：", "一次不到20美元的企业餐也与被推广药物的处方增加相关（JAMA Intern Med 2016）。"),
        ("注意：", "关联并非在每个案例中都证明因果关系或法律意义上的贿赂。")],
 'hi': [("न्यूयॉर्क:", "Masa, Daniel, Le Bernardin और Eleven Madison Park का नाम 2020 की समझौता घोषणा में आया।"),
        ("तुर्की, भोजन से आगे:", "फ़ोन, टीवी, कंप्यूटर, घरेलू उपकरण और जीवनसाथी सहित कांग्रेस यात्रा का खर्च।"),
        ("छोटा भोजन भी:", "20 $ से कम का एक कंपनी भोजन भी प्रचारित दवा के अधिक पर्चों से जुड़ा मिला (JAMA Intern Med 2016)।"),
        ("सावधानी:", "हर मामले में संबंध कारण-संबंध या क़ानूनी रिश्वत का प्रमाण नहीं है।")],
 'ja': [("ニューヨーク：", "Masa、Daniel、Le Bernardin、Eleven Madison Parkが2020年の和解発表に登場した。"),
        ("トルコ、食事だけではない：", "携帯電話、テレビ、パソコン、白物家電、配偶者同伴の学会参加支援。"),
        ("少額の食事でも：", "20ドル未満の企業提供の食事1回でも、宣伝された薬の処方増加と関連（JAMA Intern Med 2016）。"),
        ("注意：", "関連はすべての事例で因果関係や法的な贈賄の証拠となるわけではない。")],
}
M = {
 'en': "The prescription should be decided by the patient's need.",
 'de': "Über die Verordnung sollte der Bedarf des Patienten entscheiden.",
 'es': "La receta debe decidirla la necesidad del paciente.",
 'ru': "Назначение должно определяться потребностями пациента.",
 'zh': "处方应由患者的需要决定。",
 'hi': "पर्चा मरीज़ की ज़रूरत तय करे।",
 'ja': "処方は患者の必要性によって決められるべきだ。",
}
SRC = {
 'en': "Sources: Cochrane, 9.10.2026 · US Department of Justice, 2013/2020 · Vurdum Duymazlar, 2026",
 'de': "Quellen: Cochrane, 9.10.2026 · US-Justizministerium, 2013/2020 · Vurdum Duymazlar, 2026",
 'es': "Fuentes: Cochrane, 9.10.2026 · Departamento de Justicia de EE. UU., 2013/2020 · Vurdum Duymazlar, 2026",
 'ru': "Источники: Cochrane, 9.10.2026 · Министерство юстиции США, 2013/2020 · Vurdum Duymazlar, 2026",
 'zh': "来源：Cochrane，2026.10.9 · 美国司法部，2013/2020 · Vurdum Duymazlar，2026",
 'hi': "स्रोत: Cochrane, 9.10.2026 · अमेरिकी न्याय विभाग, 2013/2020 · Vurdum Duymazlar, 2026",
 'ja': "出典：Cochrane、2026.10.9 · 米国司法省、2013/2020 · Vurdum Duymazlar、2026",
}
CARDS['b26_yemek_info'] = ('burg', {l: D(T[l][0], T[l][1], T[l][2], S[l], None, P[l], M[l], SRC[l]) for l in T})
