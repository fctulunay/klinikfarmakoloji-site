from batch1 import D
CARDS = {}

# Antidepressants in older adults (author's infographic): Nelson 2008 response rates, risks, dosing message
T = {
 'en': ("BITTER MEDICINE", "ANTIDEPRESSANT USE IN OLDER ADULTS", "How much benefit? Which risks?"),
 'de': ("BITTERE MEDIZIN", "ANTIDEPRESSIVA BEI ÄLTEREN MENSCHEN", "Wie viel Nutzen? Welche Risiken?"),
 'es': ("MEDICINA AMARGA", "USO DE ANTIDEPRESIVOS EN PERSONAS MAYORES", "¿Cuánto beneficio? ¿Qué riesgos?"),
 'ru': ("ГОРЬКОЕ ЛЕКАРСТВО", "АНТИДЕПРЕССАНТЫ У ПОЖИЛЫХ", "Насколько велика польза? Каковы риски?"),
 'zh': ("苦药", "老年人使用抗抑郁药", "获益有多大？有哪些风险？"),
 'hi': ("कड़वी दवा", "बुज़ुर्गों में अवसादरोधी दवाओं का उपयोग", "कितना लाभ? कौन-से जोखिम?"),
 'ja': ("苦い薬", "高齢者における抗うつ薬の使用", "効果はどれほどか？どんなリスクがあるか？"),
}
S = {
 'en': [("44.4%", "Treatment response: antidepressant"), ("34.7%", "Treatment response: placebo")],
 'de': [("44,4 %", "Ansprechen: Antidepressivum"), ("34,7 %", "Ansprechen: Placebo")],
 'es': [("44,4 %", "Respuesta al tratamiento: antidepresivo"), ("34,7 %", "Respuesta al tratamiento: placebo")],
 'ru': [("44,4%", "Ответ на лечение: антидепрессант"), ("34,7%", "Ответ на лечение: плацебо")],
 'zh': [("44.4%", "治疗应答：抗抑郁药"), ("34.7%", "治疗应答：安慰剂")],
 'hi': [("44.4%", "उपचार प्रतिक्रिया: अवसादरोधी"), ("34.7%", "उपचार प्रतिक्रिया: प्लेसीबो")],
 'ja': [("44.4%", "治療反応率：抗うつ薬"), ("34.7%", "治療反応率：プラセボ")],
}
P = {
 'en': ["Falls and fractures", "Low sodium (hyponatraemia)", "Bleeding", "QT prolongation", "Drug interactions"],
 'de': ["Stürze und Knochenbrüche", "Niedriges Natrium (Hyponatriämie)", "Blutungen", "QT-Verlängerung", "Arzneimittelwechselwirkungen"],
 'es': ["Caídas y fracturas", "Sodio bajo (hiponatremia)", "Hemorragias", "Prolongación del QT", "Interacciones farmacológicas"],
 'ru': ["Падения и переломы", "Низкий натрий (гипонатриемия)", "Кровотечения", "Удлинение интервала QT", "Лекарственные взаимодействия"],
 'zh': ["跌倒和骨折", "低钠血症", "出血", "QT间期延长", "药物相互作用"],
 'hi': ["गिरना और फ्रैक्चर", "सोडियम की कमी (हाइपोनेट्रीमिया)", "रक्तस्राव", "QT का लंबा होना", "दवाओं की पारस्परिक क्रिया"],
 'ja': ["転倒と骨折", "低ナトリウム（低Na血症）", "出血", "QT延長", "薬物相互作用"],
}
RISK = {'en':'RISKS','de':'RISIKEN','es':'RIESGOS','ru':'РИСКИ','zh':'风险','hi':'जोखिम','ja':'リスク'}
P = {l: [(f"⚠ {RISK[l]}:" if i==0 else "⚠", x) for i,x in enumerate(v)] for l,v in P.items()}
M = {
 'en': "Start low, go slow, monitor closely.",
 'de': "Niedrig beginnen, langsam steigern, eng überwachen.",
 'es': "Empezar con dosis baja, subir despacio, vigilar de cerca.",
 'ru': "Начинать с малой дозы, повышать медленно, внимательно наблюдать.",
 'zh': "低剂量起始，缓慢加量，密切监测。",
 'hi': "कम खुराक से शुरू करें, धीरे बढ़ाएँ, नज़दीकी निगरानी रखें।",
 'ja': "低用量で始め、ゆっくり増量し、注意深く観察する。",
}
SRC = {
 'en': "Age 60 and over, major depression · Nelson et al., 2008",
 'de': "60 Jahre und älter, Major Depression · Nelson et al., 2008",
 'es': "60 años o más, depresión mayor · Nelson et al., 2008",
 'ru': "60 лет и старше, большое депрессивное расстройство · Nelson et al., 2008",
 'zh': "60岁及以上，重性抑郁症 · Nelson等，2008",
 'hi': "60 वर्ष और उससे अधिक, मेजर डिप्रेशन · Nelson et al., 2008",
 'ja': "60歳以上、大うつ病 · Nelson ら、2008",
}
CARDS['b32_yasli_antidepresan'] = ('teal', {l: D(T[l][0], T[l][1], T[l][2], S[l], None, P[l], M[l], SRC[l]) for l in T})
