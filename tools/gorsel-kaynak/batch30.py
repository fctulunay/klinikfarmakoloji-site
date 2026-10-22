from batch1 import D
CARDS = {}

# Weight-loss injections: Nefes news on Canan Karatay's claims vs SELECT / FLOW / ESSENCE (author's infographic)
T = {
 'en': ("SCIENTIFIC CRITIQUE OF THE NEFES NEWS STORY", "DO CANAN KARATAY'S CLAIMS MATCH THE EVIDENCE?", "Weight-loss injections: organ damage claims and clinical facts"),
 'de': ("WISSENSCHAFTLICHE KRITIK AM NEFES-BERICHT", "STIMMEN CANAN KARATAYS BEHAUPTUNGEN MIT DER EVIDENZ ÜBEREIN?", "Abnehmspritzen: Behauptungen über Organschäden und klinische Fakten"),
 'es': ("CRÍTICA CIENTÍFICA DE LA NOTICIA DE NEFES", "¿COINCIDEN LAS AFIRMACIONES DE CANAN KARATAY CON LA EVIDENCIA?", "Inyecciones para adelgazar: afirmaciones de daño orgánico y hechos clínicos"),
 'ru': ("НАУЧНАЯ КРИТИКА ПУБЛИКАЦИИ NEFES", "СООТВЕТСТВУЮТ ЛИ УТВЕРЖДЕНИЯ КАНАН КАРАТАЙ ДОКАЗАТЕЛЬСТВАМ?", "Уколы для похудения: утверждения о вреде органам и клинические факты"),
 'zh': ("对NEFES报道的科学评析", "CANAN KARATAY的说法与证据相符吗？", "减肥针：器官损害说法与临床事实"),
 'hi': ("NEFES की खबर की वैज्ञानिक समीक्षा", "क्या कनान करताय के दावे साक्ष्य से मेल खाते हैं?", "वज़न घटाने के इंजेक्शन: अंग क्षति के दावे और नैदानिक तथ्य"),
 'ja': ("NEFES紙の記事への科学的批評", "カナン・カラタイ氏の主張は根拠と一致するか？", "痩せる注射：臓器障害の主張と臨床的事実"),
}
S = {
 'en': [("−20%", "HEART · SELECT: relative risk of CV death, heart attack or stroke (semaglutide 6.5% vs placebo 8.0%)"), ("−24%", "KIDNEY · FLOW: serious kidney outcomes and kidney/CV death, in type 2 diabetes with chronic kidney disease"), ("62.9% vs 34.3%", "LIVER · ESSENCE: steatohepatitis resolved without worsening fibrosis (MASH, F2-F3)")],
 'de': [("−20 %", "HERZ · SELECT: relatives Risiko für CV-Tod, Herzinfarkt oder Schlaganfall (Semaglutid 6,5 % vs. Placebo 8,0 %)"), ("−24 %", "NIERE · FLOW: schwere Nierenereignisse und renaler/CV-Tod bei Typ-2-Diabetes mit chronischer Nierenerkrankung"), ("62,9 % vs. 34,3 %", "LEBER · ESSENCE: Rückbildung der Steatohepatitis ohne Verschlechterung der Fibrose (MASH, F2-F3)")],
 'es': [("−20 %", "CORAZÓN · SELECT: riesgo relativo de muerte CV, infarto o ictus (semaglutida 6,5 % vs placebo 8,0 %)"), ("−24 %", "RIÑÓN · FLOW: eventos renales graves y muerte renal/CV, en diabetes tipo 2 con enfermedad renal crónica"), ("62,9 % vs 34,3 %", "HÍGADO · ESSENCE: resolución de la esteatohepatitis sin empeorar la fibrosis (MASH, F2-F3)")],
 'ru': [("−20%", "СЕРДЦЕ · SELECT: относительный риск СС-смерти, инфаркта или инсульта (семаглутид 6,5% vs плацебо 8,0%)"), ("−24%", "ПОЧКИ · FLOW: тяжёлые почечные исходы и почечная/СС-смерть при диабете 2 типа с ХБП"), ("62,9% vs 34,3%", "ПЕЧЕНЬ · ESSENCE: разрешение стеатогепатита без ухудшения фиброза (MASH, F2-F3)")],
 'zh': [("−20%", "心脏 · SELECT：心血管死亡、心梗或卒中的相对风险（司美格鲁肽6.5% 对 安慰剂8.0%）"), ("−24%", "肾脏 · FLOW：2型糖尿病合并慢性肾病患者的严重肾脏结局及肾脏/心血管死亡"), ("62.9% 对 34.3%", "肝脏 · ESSENCE：脂肪性肝炎消退且纤维化未加重（MASH，F2-F3）")],
 'hi': [("−20%", "हृदय · SELECT: हृदय-संवहनी मृत्यु, दिल का दौरा या स्ट्रोक का सापेक्ष जोखिम (सेमाग्लूटाइड 6.5% बनाम प्लेसीबो 8.0%)"), ("−24%", "गुर्दा · FLOW: टाइप 2 मधुमेह व दीर्घकालिक गुर्दा रोग में गंभीर गुर्दा परिणाम और गुर्दा/हृदय मृत्यु"), ("62.9% बनाम 34.3%", "यकृत · ESSENCE: फाइब्रोसिस बिगड़े बिना स्टीटोहेपेटाइटिस का ठीक होना (MASH, F2-F3)")],
 'ja': [("−20%", "心臓 · SELECT：心血管死・心筋梗塞・脳卒中の相対リスク（セマグルチド6.5% 対 プラセボ8.0%）"), ("−24%", "腎臓 · FLOW：2型糖尿病と慢性腎臓病における重篤な腎イベントと腎・心血管死"), ("62.9% 対 34.3%", "肝臓 · ESSENCE：線維化の悪化なく脂肪肝炎が消失（MASH、F2-F3）")],
}
P = {
 'en': [("Real risks exist:", "acute kidney injury from vomiting and fluid loss, gallbladder disease, pancreatitis, hypoglycaemia with insulin."), ("Scope:", "the data are for semaglutide and the patient groups studied; they cannot be generalised to all drugs.")],
 'de': [("Echte Risiken gibt es:", "akute Nierenschädigung durch Erbrechen und Flüssigkeitsverlust, Gallenblasenerkrankungen, Pankreatitis, Unterzuckerung mit Insulin."), ("Geltungsbereich:", "Die Daten gelten für Semaglutid und die untersuchten Patientengruppen; sie lassen sich nicht auf alle Mittel übertragen.")],
 'es': [("Hay riesgos reales:", "lesión renal aguda por vómitos y pérdida de líquidos, enfermedad de la vesícula, pancreatitis, hipoglucemia con insulina."), ("Alcance:", "los datos son de semaglutida y de los grupos estudiados; no se pueden generalizar a todos los fármacos.")],
 'ru': [("Реальные риски есть:", "острое повреждение почек из-за рвоты и потери жидкости, болезни желчного пузыря, панкреатит, гипогликемия с инсулином."), ("Границы:", "данные относятся к семаглутиду и изученным группам; их нельзя переносить на все препараты.")],
 'zh': [("确有真实风险：", "呕吐和失水导致的急性肾损伤、胆囊疾病、胰腺炎、与胰岛素合用时低血糖。"), ("适用范围：", "数据来自司美格鲁肽及所研究的患者群体，不能推广到所有药物。")],
 'hi': [("वास्तविक जोखिम हैं:", "उल्टी और द्रव हानि से तीव्र गुर्दा क्षति, पित्ताशय रोग, अग्नाशयशोथ, इंसुलिन के साथ हाइपोग्लाइसीमिया।"), ("दायरा:", "आँकड़े सेमाग्लूटाइड और अध्ययन किए गए रोगी समूहों के हैं; इन्हें सभी दवाओं पर लागू नहीं किया जा सकता।")],
 'ja': [("現実のリスクはある：", "嘔吐・脱水による急性腎障害、胆嚢疾患、膵炎、インスリン併用時の低血糖。"), ("範囲：", "データはセマグルチドと試験対象の患者群のもので、すべての薬に一般化はできない。")],
}
M = {
 'en': "Benefit and risk must be explained together.",
 'de': "Nutzen und Risiko müssen gemeinsam dargestellt werden.",
 'es': "El beneficio y el riesgo deben explicarse juntos.",
 'ru': "О пользе и риске нужно рассказывать вместе.",
 'zh': "获益与风险必须一并说明。",
 'hi': "लाभ और जोखिम को साथ-साथ बताया जाना चाहिए।",
 'ja': "利益とリスクは一緒に説明されなければならない。",
}
SRC = {l: "SELECT, NEJM 2023 · FLOW, NEJM 2024 · ESSENCE, NEJM 2025 · Product information" for l in T}
CARDS['b30_zayiflama_info'] = ('navy', {l: D(T[l][0], T[l][1], T[l][2], S[l], None, P[l], M[l], SRC[l]) for l in T})
