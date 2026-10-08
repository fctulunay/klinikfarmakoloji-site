from batch1 import D
CARDS = {}

# The new deception: longevity clinics and longevity coaching (cover poster + infographic card)
T = {
 'en': ("THE NEW DECEPTION", "Longevity clinics and longevity coaching", "Measuring is not the same as extending life"),
 'de': ("DIE NEUE TÄUSCHUNG", "Longevity-Kliniken und Longevity-Coaching", "Messen heißt nicht, das Leben zu verlängern"),
 'es': ("EL NUEVO ENGAÑO", "Clínicas de longevidad y coaching de longevidad", "Medir no es lo mismo que alargar la vida"),
 'ru': ("НОВЫЙ ОБМАН", "Клиники долголетия и коучинг долголетия", "Измерить не значит продлить жизнь"),
 'zh': ("新的骗局", "长寿诊所与长寿教练", "能测量，不等于能延长寿命"),
 'hi': ("नया छलावा", "लॉन्जेविटी क्लिनिक और लॉन्जेविटी कोचिंग", "नापना, उम्र बढ़ाना नहीं है"),
 'ja': ("新たなまやかし", "長寿クリニックと長寿コーチング", "測定できることと、寿命を延ばせることは別である"),
}
CARDS['b24_longevity_kapak'] = ('burg', {l: D(*v) for l, v in T.items()})

S = {
 'en': [("$5,500", "Northwestern's yearly longevity package (STAT)"), ("233,298", "people in 11 randomised trials of general health checks"), ("RR 1.00", "no fall in total deaths (95% CI 0.97-1.03)")],
 'de': [("5.500 $", "Jahrespaket der Longevity-Klinik von Northwestern (STAT)"), ("233.298", "Personen in 11 randomisierten Studien zu allgemeinen Gesundheitschecks"), ("RR 1,00", "kein Rückgang der Gesamtsterblichkeit (95 %-KI 0,97-1,03)")],
 'es': [("5.500 $", "paquete anual de longevidad de Northwestern (STAT)"), ("233.298", "personas en 11 ensayos aleatorizados de chequeos generales"), ("RR 1,00", "sin reducción de la mortalidad total (IC 95 % 0,97-1,03)")],
 'ru': [("5 500 $", "годовой пакет клиники долголетия Northwestern (STAT)"), ("233 298", "человек в 11 рандомизированных исследованиях общих проверок здоровья"), ("ОР 1,00", "общая смертность не снизилась (95 % ДИ 0,97-1,03)")],
 'zh': [("5500美元", "Northwestern长寿诊所的年度套餐（STAT）"), ("233,298", "11项常规体检随机试验的受试者人数"), ("RR 1.00", "总死亡率未降低（95%置信区间0.97-1.03）")],
 'hi': [("5,500 डॉलर", "Northwestern का सालाना लॉन्जेविटी पैकेज (STAT)"), ("2,33,298", "सामान्य स्वास्थ्य जाँच के 11 रैंडमाइज़्ड परीक्षणों में लोग"), ("RR 1.00", "कुल मृत्यु में कोई कमी नहीं (95% CI 0.97-1.03)")],
 'ja': [("5,500ドル", "Northwesternの長寿クリニックの年間パッケージ（STAT）"), ("233,298人", "一般健診に関する11件のランダム化試験の参加者"), ("RR 1.00", "総死亡は減らなかった（95%信頼区間0.97-1.03）")],
}
P = {
 'en': [("Biological age is not lifespan:", "looking younger on a test is not proof that you will live longer."),
        ("More tests are not better health:", "unclear finding, repeat test, extra procedure, anxiety and cost."),
        ("A hospital's name is not evidence:", "academic prestige does not prove that the package works."),
        ("Coaching:", "support with diet and exercise is one thing; a claim to reverse ageing needs its own evidence."),
        ("Turkey:", "clinic and hospital pages list IV drips, ozone, stem cells and exosomes as anti-ageing; none cites a trial.")],
 'de': [("Biologisches Alter ist nicht Lebensdauer:", "in einem Test jünger zu wirken beweist nicht, dass man länger lebt."),
        ("Mehr Tests sind nicht mehr Gesundheit:", "unklarer Befund, Wiederholungstest, Zusatzeingriff, Angst und Kosten."),
        ("Der Name der Klinik ist kein Beleg:", "akademisches Ansehen beweist nicht, dass das Paket wirkt."),
        ("Coaching:", "Hilfe bei Ernährung und Bewegung ist das eine; die Behauptung, das Altern umzukehren, braucht eigene Belege."),
        ("Türkei:", "Klinikseiten führen Infusionen, Ozon, Stammzellen und Exosomen als Anti-Aging auf; keine nennt eine Studie.")],
 'es': [("La edad biológica no es la duración de la vida:", "parecer más joven en una prueba no demuestra que se vivirá más."),
        ("Más pruebas no es mejor salud:", "hallazgo dudoso, prueba repetida, procedimiento adicional, ansiedad y coste."),
        ("El nombre del hospital no es una prueba:", "el prestigio académico no demuestra que el paquete funcione."),
        ("Coaching:", "apoyar la dieta y el ejercicio es una cosa; afirmar que se revierte el envejecimiento exige sus propias pruebas."),
        ("Turquía:", "las páginas de clínicas y hospitales ofrecen sueros, ozono, células madre y exosomas como antienvejecimiento; ninguna cita un ensayo.")],
 'ru': [("Биологический возраст не равен продолжительности жизни:", "выглядеть моложе в тесте не значит прожить дольше."),
        ("Больше анализов не значит больше здоровья:", "неясная находка, повторный тест, лишняя процедура, тревога и расходы."),
        ("Имя больницы не доказательство:", "академический престиж не доказывает пользу пакета."),
        ("Коучинг:", "помощь с питанием и движением одно дело; обещание обратить старение вспять требует своих доказательств."),
        ("Турция:", "сайты клиник предлагают капельницы, озон, стволовые клетки и экзосомы как средства против старения; ни один не ссылается на исследование.")],
 'zh': [("生物学年龄不等于寿命：", "检测结果显得年轻，并不能证明会活得更久。"),
        ("检查更多不等于更健康：", "不明确的发现、重复检查、额外操作、焦虑和花费。"),
        ("医院的名字不是证据：", "学术声誉不能证明套餐有效。"),
        ("教练服务：", "饮食和运动指导是一回事；声称逆转衰老则需要另外的证据。"),
        ("土耳其：", "诊所和医院的网页把静脉输液、臭氧、干细胞和外泌体列为抗衰老手段，却没有引用任何试验。")],
 'hi': [("जैविक उम्र, जीवन की लंबाई नहीं है:", "किसी जाँच में जवान दिखना ज़्यादा जीने का सबूत नहीं है।"),
        ("ज़्यादा जाँच, बेहतर सेहत नहीं:", "अस्पष्ट नतीजा, दोबारा जाँच, अतिरिक्त प्रक्रिया, चिंता और ख़र्च।"),
        ("अस्पताल का नाम सबूत नहीं है:", "अकादमिक प्रतिष्ठा यह साबित नहीं करती कि पैकेज काम करता है।"),
        ("कोचिंग:", "खानपान और व्यायाम में मदद एक बात है; बुढ़ापा पलटने के दावे के लिए अलग सबूत चाहिए।"),
        ("तुर्की:", "क्लिनिक और अस्पतालों के पन्ने ड्रिप, ओज़ोन, स्टेम सेल और एक्सोसोम को एंटी-एजिंग बताते हैं; कोई भी किसी परीक्षण का हवाला नहीं देता।")],
 'ja': [("生物学的年齢は寿命ではない：", "検査で若く見えても、長生きできる証拠にはならない。"),
        ("検査を増やしても健康になるわけではない：", "不明確な所見、再検査、追加の処置、不安と費用。"),
        ("病院の名前は証拠ではない：", "学術的な権威は、パッケージの有効性を証明しない。"),
        ("コーチング：", "食事や運動の支援と、老化を逆転させるという主張は別であり、後者には独自の証拠が必要である。"),
        ("トルコ：", "クリニックや病院のページは点滴、オゾン、幹細胞、エクソソームを抗加齢として掲げるが、臨床試験を示すものはない。")],
}
M = {
 'en': "A hospital's sign does not lighten the burden of proof; it makes it heavier.",
 'de': "Das Klinikschild verringert die Beweislast nicht; es erhöht sie.",
 'es': "El rótulo del hospital no reduce la carga de la prueba; la aumenta.",
 'ru': "Вывеска больницы не уменьшает бремя доказательства, а увеличивает его.",
 'zh': "医院的招牌不会减轻举证责任，只会加重它。",
 'hi': "अस्पताल का बोर्ड सबूत का बोझ घटाता नहीं, बढ़ाता है।",
 'ja': "病院の看板は立証責任を軽くしない。むしろ重くする。",
}
SRC = {
 'en': "Sources: STAT, 6 Oct 2026; Cochrane, 2019; Nature Medicine, 2024",
 'de': "Quellen: STAT, 6.10.2026; Cochrane, 2019; Nature Medicine, 2024",
 'es': "Fuentes: STAT, 6 oct. 2026; Cochrane, 2019; Nature Medicine, 2024",
 'ru': "Источники: STAT, 6.10.2026; Cochrane, 2019; Nature Medicine, 2024",
 'zh': "来源：STAT，2026年10月6日；Cochrane，2019；Nature Medicine，2024",
 'hi': "स्रोत: STAT, 6 अक्टूबर 2026; Cochrane, 2019; Nature Medicine, 2024",
 'ja': "出典：STAT（2026年10月6日）、Cochrane（2019）、Nature Medicine（2024）",
}
CARDS['b24_longevity_info'] = ('burg', {l: D(T[l][0], T[l][1], T[l][2], S[l], None, P[l], M[l], SRC[l]) for l in T})
