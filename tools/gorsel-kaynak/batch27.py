from batch1 import D
CARDS = {}

# FDA advisory committee patient/consumer reps tied to pharma-funded groups (cover + infographic card)
K = {
 'tr': ("HABER", "FDA'IN BAZI DANIŞMA KURULU ÜYELERİ ŞAİBELİ!", "Hasta ve tüketici temsilcilerinin endüstri bağlantıları"),
 'en': ("NEWS", "SOME FDA ADVISORY COMMITTEE MEMBERS UNDER A CLOUD", "Industry ties of patient and consumer representatives"),
 'de': ("NACHRICHTEN", "ZWEIFEL AN EINIGEN MITGLIEDERN DER FDA-BERATUNGSAUSSCHÜSSE", "Industrieverbindungen von Patienten- und Verbrauchervertretern"),
 'es': ("NOTICIAS", "SOMBRAS SOBRE ALGUNOS MIEMBROS DE LOS COMITÉS ASESORES DE LA FDA", "Vínculos con la industria de los representantes de pacientes y consumidores"),
 'ru': ("НОВОСТИ", "ПОД ПОДОЗРЕНИЕМ: ЧЛЕНЫ КОНСУЛЬТАТИВНЫХ КОМИТЕТОВ FDA", "Связи представителей пациентов и потребителей с индустрией"),
 'zh': ("新闻", "FDA部分顾问委员会成员受到质疑", "患者和消费者代表与制药业的关联"),
 'hi': ("समाचार", "FDA सलाहकार समितियों के कुछ सदस्य संदेह के घेरे में", "मरीज़ और उपभोक्ता प्रतिनिधियों के उद्योग से संबंध"),
 'ja': ("ニュース", "疑惑の目を向けられるFDA諮問委員会の一部委員", "患者・消費者代表と製薬業界とのつながり"),
}

T = {
 'en': ("NEWS", "ARE PATIENT GROUPS AT THE SERVICE OF DRUG COMPANIES?", "Industry ties of patient and consumer representatives · FDA advisory committee meetings, 2013–2022"),
 'de': ("NACHRICHTEN", "STEHEN PATIENTENVERBÄNDE IM DIENST DER PHARMAFIRMEN?", "Industrieverbindungen von Patienten- und Verbrauchervertretern · Sitzungen der FDA-Beratungsausschüsse, 2013–2022"),
 'es': ("NOTICIAS", "¿ESTÁN LAS ASOCIACIONES DE PACIENTES AL SERVICIO DE LAS FARMACÉUTICAS?", "Vínculos con la industria de los representantes de pacientes y consumidores · Reuniones de comités asesores de la FDA, 2013–2022"),
 'ru': ("НОВОСТИ", "ПАЦИЕНТСКИЕ ОРГАНИЗАЦИИ НА СЛУЖБЕ У ФАРМКОМПАНИЙ?", "Связи представителей пациентов и потребителей с индустрией · Заседания консультативных комитетов FDA, 2013–2022"),
 'zh': ("新闻", "患者组织在为制药公司服务吗？", "患者和消费者代表与制药业的关联 · FDA顾问委员会会议，2013–2022年"),
 'hi': ("समाचार", "क्या मरीज़ संगठन दवा कंपनियों के इशारे पर हैं?", "मरीज़ और उपभोक्ता प्रतिनिधियों के उद्योग से संबंध · FDA सलाहकार समिति बैठकें, 2013–2022"),
 'ja': ("ニュース", "患者団体は製薬会社の言いなりか？", "患者・消費者代表と製薬業界とのつながり · FDA諮問委員会の会議、2013–2022年"),
}
S = {
 'en': [("38%", "of meetings had at least one rep tied to an industry-funded organization"), ("11%", "of meetings: the rep's organization was funded by the maker of the drug under review"), ("90%+", "of groups consulted in user-fee (PDUFA) talks were industry-funded (POGO)")],
 'de': [("38 %", "der Sitzungen hatten mindestens einen Vertreter mit Bindung an eine industriefinanzierte Organisation"), ("11 %", "der Sitzungen: Die Organisation des Vertreters wurde vom Hersteller des geprüften Medikaments finanziert"), ("über 90 %", "der in den Nutzergebühr-Verhandlungen (PDUFA) befragten Gruppen waren industriefinanziert (POGO)")],
 'es': [("38 %", "de las reuniones tuvo al menos un representante vinculado a una organización financiada por la industria"), ("11 %", "de las reuniones: la organización del representante recibía fondos del fabricante del fármaco evaluado"), ("más del 90 %", "de los grupos consultados en las negociaciones de tasas (PDUFA) recibía fondos de la industria (POGO)")],
 'ru': [("38%", "заседаний: хотя бы один представитель связан с организацией, финансируемой индустрией"), ("11%", "заседаний: организацию представителя финансировал производитель рассматриваемого препарата"), ("более 90%", "групп, участвовавших в переговорах о сборах (PDUFA), финансировались индустрией (POGO)")],
 'zh': [("38%", "的会议中至少有一名代表与接受业界资助的组织有关联"), ("11%", "的会议中，代表所属组织接受了受审药物生产商的资助"), ("90%以上", "参与用户付费（PDUFA）磋商的团体接受业界资助（POGO）")],
 'hi': [("38%", "बैठकों में कम से कम एक प्रतिनिधि उद्योग से वित्तपोषित संगठन से जुड़ा था"), ("11%", "बैठकों में प्रतिनिधि के संगठन को समीक्षाधीन दवा की निर्माता कंपनी से धन मिला"), ("90% से अधिक", "उपयोगकर्ता शुल्क (PDUFA) वार्ता में शामिल समूह उद्योग से वित्तपोषित थे (POGO)")],
 'ja': [("38%", "の会議に、業界資金を受ける団体と関係する代表が少なくとも1人いた"), ("11%", "の会議で、代表の所属団体が審査対象薬の製造企業から資金を受けていた"), ("90%以上", "ユーザーフィー（PDUFA）交渉で意見を求められた団体が業界資金を受けていた（POGO）")],
}
P = {
 'en': [("Note:", "these figures are shares of meetings, not of people."), ("Problem:", "the financial ties of organizations are not visible enough."), ("Risk:", "the independence of views presented on behalf of patients is in question."), ("Solution:", "open disclosure of funding, a public record, no vote when there is a conflict."), ("A question for Turkey:", "are company support to patient associations and conflict-of-interest declarations in TİTCK and SGK processes made public?")],
 'de': [("Hinweis:", "Die Zahlen sind Anteile der Sitzungen, nicht der Personen."), ("Problem:", "Die finanziellen Verbindungen der Organisationen sind nicht ausreichend sichtbar."), ("Risiko:", "Die Unabhängigkeit der im Namen der Patienten vorgetragenen Ansichten steht in Frage."), ("Lösung:", "offene Offenlegung der Finanzierung, öffentliches Register, keine Stimme bei Interessenkonflikt."), ("Eine Frage an die Türkei:", "Werden Firmenzuwendungen an Patientenverbände und Interessenerklärungen in den Verfahren von TİTCK und SGK veröffentlicht?")],
 'es': [("Nota:", "estas cifras son proporciones de reuniones, no de personas."), ("Problema:", "los vínculos financieros de las organizaciones no son lo bastante visibles."), ("Riesgo:", "se cuestiona la independencia de las opiniones presentadas en nombre de los pacientes."), ("Solución:", "declaración abierta de la financiación, registro público y no votar si hay conflicto."), ("Una pregunta para Turquía:", "¿son públicos los apoyos de empresas a asociaciones de pacientes y las declaraciones de conflicto de intereses en los procesos de TİTCK y SGK?")],
 'ru': [("Примечание:", "это доли заседаний, а не людей."), ("Проблема:", "финансовые связи организаций недостаточно видны."), ("Риск:", "под вопросом независимость мнений, высказываемых от имени пациентов."), ("Решение:", "открытое раскрытие финансирования, публичный реестр, отказ от голосования при конфликте интересов."), ("Вопрос для Турции:", "публикуются ли поддержка компаниями пациентских ассоциаций и декларации о конфликте интересов в процедурах TİTCK и SGK?")],
 'zh': [("说明：", "这些数字是会议所占比例，而非人数比例。"), ("问题：", "组织的财务关联不够透明。"), ("风险：", "代表患者提出的意见是否独立受到质疑。"), ("对策：", "公开披露资金来源、建立公开记录、存在利益冲突时不参与投票。"), ("对土耳其的提问：", "企业对患者协会的资助以及TİTCK和SGK程序中的利益冲突声明是否公开？")],
 'hi': [("ध्यान दें:", "ये आँकड़े बैठकों का अनुपात हैं, व्यक्तियों का नहीं।"), ("समस्या:", "संगठनों के वित्तीय संबंध पर्याप्त रूप से दिखाई नहीं देते।"), ("जोखिम:", "मरीज़ों की ओर से रखी गई राय की स्वतंत्रता पर सवाल है।"), ("समाधान:", "वित्तपोषण का खुला खुलासा, सार्वजनिक रिकॉर्ड, हितों के टकराव में मतदान नहीं।"), ("तुर्की के लिए प्रश्न:", "क्या कंपनियों से मरीज़ संघों को मिली सहायता और TİTCK व SGK प्रक्रियाओं में हितों के टकराव की घोषणाएँ सार्वजनिक हैं?")],
 'ja': [("注：", "これらは会議の割合であり、人数の割合ではない。"), ("問題：", "団体の金銭的なつながりが十分に見えない。"), ("リスク：", "患者を代表して述べられる意見の独立性が問われている。"), ("解決策：", "資金の公開、公的な記録、利益相反がある場合は投票しない。"), ("トルコへの問い：", "企業による患者団体への支援と、TİTCK・SGKの手続きにおける利益相反の申告は公開されているか？")],
}
M = {
 'en': "The patient's voice matters; so does knowing who pays for it.",
 'de': "Die Stimme der Patienten zählt; ebenso wichtig ist, wer sie bezahlt.",
 'es': "La voz del paciente importa; también saber quién la financia.",
 'ru': "Голос пациента важен, как и то, кто его оплачивает.",
 'zh': "患者的声音很重要；谁在为它买单同样重要。",
 'hi': "मरीज़ की आवाज़ मायने रखती है; यह भी कि उसका ख़र्च कौन उठाता है।",
 'ja': "患者の声は大切だ。誰がその費用を出しているかを知ることも同じく大切だ。",
}
SRC = {l: "Health Affairs Scholar, 7.10.2026 · STAT, 13.10.2026 · POGO · NCHR 2024" for l in T}
CARDS['b27_fda_info'] = ('burg', {l: D(T[l][0], T[l][1], T[l][2], S[l], None, P[l], M[l], SRC[l]) for l in T})
