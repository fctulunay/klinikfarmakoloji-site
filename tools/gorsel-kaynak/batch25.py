from batch1 import D
CARDS = {}

# Johnson & Johnson file: bribery, improper payments and multi-billion-dollar settlements (cover poster + infographic card)
T = {
 'en': ("JOHNSON & JOHNSON", "The Johnson & Johnson file", "Bribery, improper payments and multi-billion-dollar settlements"),
 'de': ("JOHNSON & JOHNSON", "Die Johnson-&-Johnson-Akte", "Bestechung, unzulässige Zahlungen und Vergleiche in Milliardenhöhe"),
 'es': ("JOHNSON & JOHNSON", "El expediente Johnson & Johnson", "Sobornos, pagos indebidos y acuerdos de miles de millones de dólares"),
 'ru': ("JOHNSON & JOHNSON", "Досье Johnson & Johnson", "Взятки, неправомерные выплаты и мировые соглашения на миллиарды долларов"),
 'zh': ("JOHNSON & JOHNSON", "强生档案", "贿赂、不当付款与数十亿美元的和解"),
 'hi': ("JOHNSON & JOHNSON", "जॉनसन एंड जॉनसन की फ़ाइल", "रिश्वत, अनुचित भुगतान और अरबों डॉलर के समझौते"),
 'ja': ("JOHNSON & JOHNSON", "ジョンソン・エンド・ジョンソンの記録", "贈賄、不正な支払い、そして数十億ドル規模の和解"),
}
CARDS['b25_jj_kapak'] = ('navy', {l: D(*v) for l, v in T.items()})

S = {
 'en': [("$70M+", "2011 · international bribery: Greece, Poland, Romania, Iraq"), ("$2.2B+", "2013 · Risperdal, Invega, Natrecor marketing"), ("up to $5B", "2022 · opioids, national settlement"), ("$5.5B", "2026 · talc powder, conditional settlement")],
 'de': [("70 Mio. $+", "2011 · Auslandsbestechung: Griechenland, Polen, Rumänien, Irak"), ("2,2 Mrd. $+", "2013 · Vermarktung von Risperdal, Invega, Natrecor"), ("bis 5 Mrd. $", "2022 · Opioide, landesweiter Vergleich"), ("5,5 Mrd. $", "2026 · Talkumpuder, bedingter Vergleich")],
 'es': [("70 M$+", "2011 · sobornos internacionales: Grecia, Polonia, Rumanía, Irak"), ("2.200 M$+", "2013 · promoción de Risperdal, Invega, Natrecor"), ("hasta 5.000 M$", "2022 · opioides, acuerdo nacional"), ("5.500 M$", "2026 · talco, acuerdo condicionado")],
 'ru': [("70 млн $+", "2011 · взятки за рубежом: Греция, Польша, Румыния, Ирак"), ("2,2 млрд $+", "2013 · продвижение Risperdal, Invega, Natrecor"), ("до 5 млрд $", "2022 · опиоиды, общенациональное соглашение"), ("5,5 млрд $", "2026 · тальк, условное соглашение")],
 'zh': [("7000万美元+", "2011年 · 海外贿赂：希腊、波兰、罗马尼亚、伊拉克"), ("22亿美元+", "2013年 · Risperdal、Invega、Natrecor的推广"), ("最高50亿美元", "2022年 · 阿片类药物，全国和解"), ("55亿美元", "2026年 · 滑石粉，附条件和解")],
 'hi': [("7 करोड़ $+", "2011 · विदेश में रिश्वत: ग्रीस, पोलैंड, रोमानिया, इराक"), ("2.2 अरब $+", "2013 · Risperdal, Invega, Natrecor का प्रचार"), ("5 अरब $ तक", "2022 · ओपिओइड, राष्ट्रीय समझौता"), ("5.5 अरब $", "2026 · टैल्क पाउडर, सशर्त समझौता")],
 'ja': [("7000万ドル超", "2011年 · 海外贈賄：ギリシャ、ポーランド、ルーマニア、イラク"), ("22億ドル超", "2013年 · Risperdal、Invega、Natrecorの販売促進"), ("最大50億ドル", "2022年 · オピオイド、全国和解"), ("55億ドル", "2026年 · タルクパウダー、条件付き和解")],
}
P = {
 'en': [("2011 bribery:", "the company accepted responsibility under a deferred prosecution agreement."),
        ("2018 Actelion, $360M:", "patient co-payments paid through a charity; no admission of wrongdoing."),
        ("2019 Xarelto, $775M:", "settlement over bleeding-risk warnings; a joint amount with Bayer."),
        ("Medical devices:", "DePuy hip implants and Ethicon pelvic mesh: early implant failure, tissue damage, inadequate risk warnings.")],
 'de': [("Bestechung 2011:", "Das Unternehmen übernahm in einer Vereinbarung über einen Strafaufschub die Verantwortung."),
        ("2018 Actelion, 360 Mio. $:", "Zuzahlungen von Patienten über eine Stiftung beglichen; kein Schuldeingeständnis."),
        ("2019 Xarelto, 775 Mio. $:", "Vergleich wegen der Warnhinweise zum Blutungsrisiko; gemeinsamer Betrag mit Bayer."),
        ("Medizinprodukte:", "DePuy-Hüftprothesen und Ethicon-Beckenbodennetze: frühes Versagen, Gewebeschäden, unzureichende Warnhinweise.")],
 'es': [("Sobornos de 2011:", "la empresa asumió su responsabilidad en un acuerdo de enjuiciamiento diferido."),
        ("2018 Actelion, 360 M$:", "copagos de pacientes pagados a través de una fundación; sin reconocimiento de culpa."),
        ("2019 Xarelto, 775 M$:", "acuerdo por las advertencias sobre el riesgo de hemorragia; importe conjunto con Bayer."),
        ("Dispositivos médicos:", "prótesis de cadera DePuy y mallas pélvicas Ethicon: fallo precoz, daño tisular, advertencias insuficientes.")],
 'ru': [("Взятки 2011 года:", "компания признала ответственность в соглашении об отсрочке уголовного преследования."),
        ("2018, Actelion, 360 млн $:", "доплаты пациентов оплачивались через благотворительный фонд; вина не признана."),
        ("2019, Xarelto, 775 млн $:", "соглашение по предупреждениям о риске кровотечений; общая сумма с Bayer."),
        ("Медицинские изделия:", "тазобедренные протезы DePuy и тазовые сетки Ethicon: ранний отказ, повреждение тканей, недостаточные предупреждения.")],
 'zh': [("2011年贿赂案：", "公司在暂缓起诉协议中承担了责任。"),
        ("2018年Actelion，3.6亿美元：", "通过慈善基金会代付患者自付费用；未承认过错。"),
        ("2019年Xarelto，7.75亿美元：", "就出血风险警示达成和解；与拜耳的共同金额。"),
        ("医疗器械：", "DePuy髋关节假体与Ethicon盆底网片：假体早期失效、组织损伤、风险警示不足。")],
 'hi': [("2011 रिश्वत मामला:", "कंपनी ने अभियोजन स्थगन समझौते में ज़िम्मेदारी स्वीकार की।"),
        ("2018 Actelion, 36 करोड़ $:", "एक धर्मार्थ संस्था के ज़रिए मरीज़ों का सह-भुगतान; ग़लती स्वीकार नहीं।"),
        ("2019 Xarelto, 77.5 करोड़ $:", "रक्तस्राव जोखिम की चेतावनियों पर समझौता; Bayer के साथ संयुक्त राशि।"),
        ("चिकित्सा उपकरण:", "DePuy कूल्हा प्रत्यारोपण और Ethicon पेल्विक मेश: जल्दी विफलता, ऊतक क्षति, अपर्याप्त चेतावनी।")],
 'ja': [("2011年の贈賄事件：", "会社は起訴猶予合意で責任を認めた。"),
        ("2018年 Actelion、3億6000万ドル：", "慈善財団を通じて患者の自己負担を肩代わり。過失は認めず。"),
        ("2019年 Xarelto、7億7500万ドル：", "出血リスクの警告をめぐる和解。バイエルとの共同額。"),
        ("医療機器：", "DePuyの人工股関節とEthiconの骨盤メッシュ：早期の不具合、組織損傷、不十分なリスク警告。")],
}
M = {
 'en': "Fine ≠ compensation ≠ settlement: these amounts cannot be added up into a single 'total of fines'.",
 'de': "Strafe ≠ Schadensersatz ≠ Vergleich: Diese Beträge lassen sich nicht zu einer einzigen „Strafsumme“ addieren.",
 'es': "Multa ≠ indemnización ≠ acuerdo: estas cifras no pueden sumarse como un único «total de multas».",
 'ru': "Штраф ≠ компенсация ≠ мировое соглашение: эти суммы нельзя сложить в один «итог штрафов».",
 'zh': "罚款 ≠ 赔偿 ≠ 和解：这些金额不能简单相加为一个“罚款总额”。",
 'hi': "जुर्माना ≠ मुआवज़ा ≠ समझौता: इन राशियों को जोड़कर एक 'कुल जुर्माना' नहीं बनाया जा सकता।",
 'ja': "罰金 ≠ 賠償 ≠ 和解：これらの金額を足し合わせて一つの「罰金総額」にすることはできない。",
}
SRC = {
 'en': "Sources: US Department of Justice, SEC, J&J filings, National Opioid Settlement",
 'de': "Quellen: US-Justizministerium, SEC, Mitteilungen von J&J, National Opioid Settlement",
 'es': "Fuentes: Departamento de Justicia de EE. UU., SEC, comunicaciones de J&J, National Opioid Settlement",
 'ru': "Источники: Министерство юстиции США, SEC, отчётность J&J, National Opioid Settlement",
 'zh': "来源：美国司法部、美国证券交易委员会（SEC）、强生公司披露文件、National Opioid Settlement",
 'hi': "स्रोत: अमेरिकी न्याय विभाग, SEC, J&J की रिपोर्टें, National Opioid Settlement",
 'ja': "出典：米国司法省、米国証券取引委員会（SEC）、J&Jの開示資料、National Opioid Settlement",
}
CARDS['b25_jj_info'] = ('burg', {l: D(T[l][0], T[l][1], T[l][2], S[l], None, P[l], M[l], SRC[l]) for l in T})
