from batch1 import D
CARDS = {}

# Vykat XR (diazoxide choline) in Prader-Willi syndrome: evidence, cost, safety (cover + infographic card)
K = {
 'tr': ("HABER", "YENİ BİR KANDIRMACA MI? VYKAT XR", "Duygu sömürüsü ve lobiciler iş başında"),
 'en': ("NEWS", "ANOTHER DECEPTION? VYKAT XR", "Emotional exploitation and lobbyists at work"),
 'de': ("NACHRICHTEN", "EINE NEUE TÄUSCHUNG? VYKAT XR", "Ausnutzung von Gefühlen und Lobbyisten am Werk"),
 'es': ("NOTICIAS", "¿UN NUEVO ENGAÑO? VYKAT XR", "Explotación emocional y grupos de presión en acción"),
 'ru': ("НОВОСТИ", "НОВЫЙ ОБМАН? VYKAT XR", "Игра на чувствах и работа лоббистов"),
 'zh': ("新闻", "又一场骗局？VYKAT XR", "情感利用与游说者在行动"),
 'hi': ("समाचार", "एक और छल? VYKAT XR", "भावनाओं का शोषण और लॉबिस्ट सक्रिय"),
 'ja': ("ニュース", "新たなごまかしか？VYKAT XR", "感情の利用とロビイストの暗躍"),
}

T = {
 'en': ("DIAZOXIDE CHOLINE · HYPERPHAGIA TREATMENT", "VYKAT XR: HALF A MILLION DOLLARS A YEAR", "Evidence, cost and safety debate in Prader-Willi syndrome"),
 'de': ("DIAZOXIDCHOLIN · BEHANDLUNG DER HYPERPHAGIE", "VYKAT XR: EINE HALBE MILLION DOLLAR PRO JAHR", "Evidenz, Kosten und Sicherheitsdebatte beim Prader-Willi-Syndrom"),
 'es': ("COLINA DE DIAZÓXIDO · TRATAMIENTO DE LA HIPERFAGIA", "VYKAT XR: MEDIO MILLÓN DE DÓLARES AL AÑO", "Evidencia, coste y debate sobre seguridad en el síndrome de Prader-Willi"),
 'ru': ("ДИАЗОКСИД ХОЛИН · ЛЕЧЕНИЕ ГИПЕРФАГИИ", "VYKAT XR: ПОЛМИЛЛИОНА ДОЛЛАРОВ В ГОД", "Доказательства, стоимость и споры о безопасности при синдроме Прадера-Вилли"),
 'zh': ("二氮嗪胆碱 · 食欲亢进治疗", "VYKAT XR：每年50万美元", "普拉德-威利综合征中的证据、费用与安全性争议"),
 'hi': ("डायज़ॉक्साइड कोलीन · हाइपरफेजिया उपचार", "VYKAT XR: साल में आधा मिलियन डॉलर", "प्रेडर-विली सिंड्रोम में साक्ष्य, लागत और सुरक्षा पर बहस"),
 'ja': ("ジアゾキシドコリン · 過食症状の治療", "VYKAT XR：年間50万ドル", "プラダー・ウィリー症候群における根拠、費用、安全性をめぐる議論"),
}
S = {
 'en': [("≈$466,000 / year", "estimated average annual cost in the US (varies with body weight; not a Turkish price)"), ("−1.67 points, p=0.198", "first phase III trial: primary endpoint not met"), ("77 patients", "basis for approval: 16-week randomized withdrawal; 5 points less worsening"), ("7 deaths · ≈100 hospitalizations", "reports cited in the October 2026 news")],
 'de': [("≈466.000 $ / Jahr", "geschätzte durchschnittliche Jahreskosten in den USA (abhängig vom Körpergewicht; kein türkischer Preis)"), ("−1,67 Punkte, p=0,198", "erste Phase-III-Studie: primärer Endpunkt verfehlt"), ("77 Patienten", "Grundlage der Zulassung: 16-wöchige randomisierte Absetzstudie; 5 Punkte weniger Verschlechterung"), ("7 Todesfälle · ≈100 Klinikaufnahmen", "Meldungen aus den Nachrichten vom Oktober 2026")],
 'es': [("≈466.000 $ / año", "coste anual medio estimado en EE. UU. (varía con el peso; no es un precio de Turquía)"), ("−1,67 puntos, p=0,198", "primer ensayo de fase III: no alcanzó la variable principal"), ("77 pacientes", "base de la aprobación: retirada aleatorizada de 16 semanas; 5 puntos menos de empeoramiento"), ("7 muertes · ≈100 hospitalizaciones", "notificaciones citadas en la noticia de octubre de 2026")],
 'ru': [("≈466 000 $ / год", "оценочная средняя годовая стоимость в США (зависит от массы тела; не цена в Турции)"), ("−1,67 балла, p=0,198", "первое исследование III фазы: первичная конечная точка не достигнута"), ("77 пациентов", "основа одобрения: 16-недельная рандомизированная отмена; ухудшение на 5 баллов меньше"), ("7 смертей · ≈100 госпитализаций", "сообщения, приведённые в новостях за октябрь 2026 г.")],
 'zh': [("约466,000美元/年", "美国估计年均费用（随体重而变；非土耳其价格）"), ("−1.67分，p=0.198", "首个III期试验：未达到主要终点"), ("77名患者", "获批依据：16周随机撤药研究；恶化少5分"), ("7例死亡 · 约100例住院", "2026年10月新闻中引用的报告")],
 'hi': [("≈4,66,000 $ / वर्ष", "अमेरिका में अनुमानित औसत वार्षिक लागत (वज़न के अनुसार बदलती है; तुर्की की कीमत नहीं)"), ("−1.67 अंक, p=0.198", "पहला चरण III परीक्षण: प्राथमिक लक्ष्य पूरा नहीं हुआ"), ("77 मरीज़", "मंज़ूरी का आधार: 16 सप्ताह का यादृच्छिक विदड्रॉल अध्ययन; 5 अंक कम बिगड़ना"), ("7 मौतें · ≈100 अस्पताल भर्ती", "अक्टूबर 2026 की खबर में उद्धृत रिपोर्टें")],
 'ja': [("年間約46万6000ドル", "米国での推定平均年間費用（体重により異なる。トルコの価格ではない）"), ("−1.67点、p=0.198", "最初の第III相試験：主要評価項目を達成せず"), ("77人の患者", "承認の根拠：16週間の無作為化中止試験。悪化が5点少ない"), ("死亡7件 · 入院約100件", "2026年10月の報道で引用された報告")],
}
P = {
 'en': [("Design:", "patients had already taken the drug for 3.3 years on average; the study compared continuing with switching to placebo."), ("Limit:", "it does not directly show the effect in patients starting treatment."), ("Reports:", "spontaneous reports do not prove that the drug caused the events."), ("Known risk:", "fluid retention and edema.")],
 'de': [("Design:", "Die Patienten hatten das Mittel bereits durchschnittlich 3,3 Jahre eingenommen; verglichen wurde Weiternehmen mit Wechsel auf Placebo."), ("Grenze:", "Die Wirkung bei Patienten, die neu beginnen, wird nicht direkt gezeigt."), ("Meldungen:", "Spontanmeldungen beweisen nicht, dass das Mittel die Ereignisse verursacht hat."), ("Bekanntes Risiko:", "Flüssigkeitsretention und Ödeme.")],
 'es': [("Diseño:", "los pacientes ya tomaban el fármaco desde hacía 3,3 años de media; se comparó continuar con pasar a placebo."), ("Límite:", "no muestra directamente el efecto en quienes empiezan el tratamiento."), ("Notificaciones:", "las notificaciones espontáneas no prueban que el fármaco causara los eventos."), ("Riesgo conocido:", "retención de líquidos y edema.")],
 'ru': [("Дизайн:", "пациенты уже принимали препарат в среднем 3,3 года; сравнивали продолжение приёма и переход на плацебо."), ("Ограничение:", "эффект у начинающих лечение напрямую не показан."), ("Сообщения:", "спонтанные сообщения не доказывают, что события вызвал препарат."), ("Известный риск:", "задержка жидкости и отёки.")],
 'zh': [("设计：", "患者此前平均已用药3.3年；研究比较继续用药与改用安慰剂。"), ("局限：", "不能直接说明新开始治疗患者的效果。"), ("报告：", "自发报告不能证明事件由药物引起。"), ("已知风险：", "液体潴留和水肿。")],
 'hi': [("डिज़ाइन:", "मरीज़ पहले से औसतन 3.3 वर्ष दवा ले रहे थे; दवा जारी रखने और प्लेसीबो पर जाने की तुलना की गई।"), ("सीमा:", "इलाज शुरू करने वाले मरीज़ों में असर सीधे नहीं दिखाता।"), ("रिपोर्टें:", "स्वैच्छिक रिपोर्टें यह साबित नहीं करतीं कि घटनाएँ दवा से हुईं।"), ("ज्ञात जोखिम:", "द्रव प्रतिधारण और सूजन।")],
 'ja': [("試験デザイン：", "患者はすでに平均3.3年服用しており、継続とプラセボへの切り替えを比較した。"), ("限界：", "新たに治療を始める患者での効果を直接示すものではない。"), ("報告：", "自発報告は、薬が事象の原因であることを証明しない。"), ("既知のリスク：", "体液貯留と浮腫。")],
}
M = {
 'en': "The open question: at this cost, have long-term clinical benefit and safety been adequately shown? Independent comparative trials and transparent safety data are needed.",
 'de': "Die offene Frage: Sind langfristiger klinischer Nutzen und Sicherheit zu diesem Preis ausreichend belegt? Nötig sind unabhängige Vergleichsstudien und transparente Sicherheitsdaten.",
 'es': "La pregunta pendiente: ¿se han demostrado suficientemente el beneficio clínico y la seguridad a largo plazo a este coste? Hacen falta ensayos comparativos independientes y datos de seguridad transparentes.",
 'ru': "Открытый вопрос: доказаны ли при такой цене долгосрочная клиническая польза и безопасность? Нужны независимые сравнительные исследования и прозрачные данные о безопасности.",
 'zh': "悬而未决的问题：以这样的费用，长期临床获益和安全性是否已得到充分证明？需要独立的对照研究和透明的安全性数据。",
 'hi': "खुला प्रश्न: इस लागत पर क्या दीर्घकालिक नैदानिक लाभ और सुरक्षा पर्याप्त रूप से सिद्ध हुई है? स्वतंत्र तुलनात्मक अध्ययन और पारदर्शी सुरक्षा आँकड़े ज़रूरी हैं।",
 'ja': "残された問い：この費用に見合う長期的な臨床的利益と安全性は十分に示されたのか。独立した比較試験と透明な安全性データが必要だ。",
}
SRC = {l: "FDA label (2025) · C601/C602 · STAT, 13.10.2026" for l in T}
CARDS['b28_vykat_info'] = ('burg', {l: D(T[l][0], T[l][1], T[l][2], S[l], None, P[l], M[l], SRC[l]) for l in T})
