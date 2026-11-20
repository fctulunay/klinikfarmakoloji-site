from batch1 import D
CARDS = {}
# "Yeni antibiyotikler ve özellikleri" (Bilimsel Yazılar, 2026-11-20): cover collage + 13 mechanism diagrams.
# Condensed cards: drug, class, mechanism, licence status. Only what the pictures and the article say.
L = ('en', 'de', 'es', 'ru', 'zh', 'hi', 'ja')
K = dict(zip(L, ("NEW ANTIBIOTICS", "NEUE ANTIBIOTIKA", "NUEVOS ANTIBIÓTICOS", "НОВЫЕ АНТИБИОТИКИ", "新型抗生素", "नए एंटीबायोटिक", "新しい抗菌薬")))
MECH = dict(zip(L, ("Mechanism:", "Wirkmechanismus:", "Mecanismo:", "Механизм:", "作用机制：", "क्रियाविधि:", "作用機序：")))
STAT = dict(zip(L, ("Status:", "Status:", "Situación:", "Статус:", "现状：", "स्थिति:", "現状：")))
NOTE = dict(zip(L, ("Conceptual illustration of the mechanism, not a drawing of the molecule.",
                    "Konzeptionelle Darstellung des Mechanismus, keine Abbildung des Moleküls.",
                    "Ilustración conceptual del mecanismo, no un dibujo de la molécula.",
                    "Схематическое изображение механизма, а не структуры молекулы.",
                    "作用机制示意图，并非分子结构图。",
                    "क्रियाविधि का अवधारणात्मक चित्र, अणु की वास्तविक संरचना नहीं।",
                    "作用機序の概念図であり、分子構造の図ではありません。")))

# id: (title, subtitle, mechanism, status) per language
DRUGS = {
 'image1': {
  'en': ("Tebipenem pivoxil (Utebzi)", "Oral carbapenem (prodrug)", "Binds PBPs and blocks peptidoglycan cross-linking; the cell wall weakens.", "FDA 2026: complicated urinary tract infection when oral options are limited."),
  'de': ("Tebipenem-Pivoxil (Utebzi)", "Orales Carbapenem (Prodrug)", "Bindet an PBP und hemmt die Quervernetzung des Peptidoglykans; die Zellwand wird geschwächt.", "FDA 2026: komplizierte Harnwegsinfektion, wenn orale Optionen begrenzt sind."),
  'es': ("Tebipenem pivoxilo (Utebzi)", "Carbapenémico oral (profármaco)", "Se une a las PBP y bloquea el entrecruzamiento del peptidoglucano; la pared celular se debilita.", "FDA 2026: infección urinaria complicada cuando las opciones orales son limitadas."),
  'ru': ("Тебипенем пивоксил (Utebzi)", "Пероральный карбапенем (пролекарство)", "Связывается с ПСБ и блокирует сшивку пептидогликана; клеточная стенка ослабевает.", "FDA 2026: осложнённая инфекция мочевых путей при ограниченном выборе пероральных средств."),
  'zh': ("替比培南酯（Utebzi）", "口服碳青霉烯类（前药）", "与青霉素结合蛋白（PBP）结合，阻断肽聚糖交联，削弱细胞壁。", "FDA 2026年批准：口服选择有限时的复杂性尿路感染。"),
  'hi': ("टेबिपेनेम पिवॉक्सिल (Utebzi)", "मुँह से ली जाने वाली कार्बापेनेम (प्रोड्रग)", "PBP से जुड़कर पेप्टिडोग्लाइकन की क्रॉस-लिंकिंग रोकती है; कोशिका भित्ति कमज़ोर होती है।", "FDA 2026: जटिल मूत्र मार्ग संक्रमण, जब मुँह से ली जाने वाली दवाओं के विकल्प सीमित हों।"),
  'ja': ("テビペネム ピボキシル（Utebzi）", "経口カルバペネム（プロドラッグ）", "PBPに結合してペプチドグリカンの架橋を阻害し、細胞壁を弱める。", "FDA 2026年承認：経口薬の選択肢が限られる複雑性尿路感染症。"),
 },
 'image2': {
  'en': ("Cefepime–zidebactam (Zaynich)", "Cefepime + β-lactam enhancer", "Cefepime binds PBP3; zidebactam binds PBP2 and also inhibits some β-lactamases.", "FDA 2026: complicated urinary tract infection."),
  'de': ("Cefepim–Zidebactam (Zaynich)", "Cefepim + β-Lactam-Verstärker", "Cefepim bindet an PBP3; Zidebactam bindet an PBP2 und hemmt zudem einige β-Lactamasen.", "FDA 2026: komplizierte Harnwegsinfektion."),
  'es': ("Cefepima–zidebactam (Zaynich)", "Cefepima + potenciador betalactámico", "La cefepima se une a la PBP3; el zidebactam se une a la PBP2 e inhibe además algunas betalactamasas.", "FDA 2026: infección urinaria complicada."),
  'ru': ("Цефепим–зидебактам (Zaynich)", "Цефепим + бета-лактамный усилитель", "Цефепим связывается с ПСБ3; зидебактам связывается с ПСБ2 и подавляет некоторые бета-лактамазы.", "FDA 2026: осложнённая инфекция мочевых путей."),
  'zh': ("头孢吡肟–齐德巴坦（Zaynich）", "头孢吡肟 + β-内酰胺增效剂", "头孢吡肟结合PBP3；齐德巴坦结合PBP2，并抑制部分β-内酰胺酶。", "FDA 2026年批准：复杂性尿路感染。"),
  'hi': ("सेफेपाइम–ज़िडेबैक्टम (Zaynich)", "सेफेपाइम + बीटा-लैक्टम एन्हांसर", "सेफेपाइम PBP3 से जुड़ती है; ज़िडेबैक्टम PBP2 से जुड़ती है और कुछ बीटा-लैक्टामेज़ को भी रोकती है।", "FDA 2026: जटिल मूत्र मार्ग संक्रमण।"),
  'ja': ("セフェピム–ジデバクタム（Zaynich）", "セフェピム＋βラクタム増強薬", "セフェピムはPBP3に、ジデバクタムはPBP2に結合し、一部のβラクタマーゼも阻害する。", "FDA 2026年承認：複雑性尿路感染症。"),
 },
 'image3': {
  'en': ("Gepotidacin (Blujepa)", "New class: triazaacenaphthylene", "Inhibits DNA gyrase and topoisomerase IV; bacterial DNA replication stops.", "FDA 2025: uncomplicated urinary tract infection; urogenital gonorrhoea."),
  'de': ("Gepotidacin (Blujepa)", "Neue Klasse: Triazaacenaphthylen", "Hemmt DNA-Gyrase und Topoisomerase IV; die bakterielle DNA-Replikation stoppt.", "FDA 2025: unkomplizierte Harnwegsinfektion; urogenitale Gonorrhö."),
  'es': ("Gepotidacina (Blujepa)", "Nueva clase: triazaacenaftileno", "Inhibe la ADN girasa y la topoisomerasa IV; se detiene la replicación del ADN bacteriano.", "FDA 2025: infección urinaria no complicada; gonorrea urogenital."),
  'ru': ("Гепотидацин (Blujepa)", "Новый класс: триазааценафтилены", "Подавляет ДНК-гиразу и топоизомеразу IV; репликация бактериальной ДНК останавливается.", "FDA 2025: неосложнённая инфекция мочевых путей; урогенитальная гонорея."),
  'zh': ("吉泊达星（Blujepa）", "新类别：三氮杂苊烯类", "抑制DNA旋转酶和拓扑异构酶IV，使细菌DNA复制停止。", "FDA 2025年批准：单纯性尿路感染；泌尿生殖道淋病。"),
  'hi': ("जेपोटिडासिन (Blujepa)", "नया वर्ग: ट्रायज़ाएसेनैफ्थिलीन", "DNA गाइरेज़ और टोपोआइसोमरेज़ IV को रोकती है; जीवाणु DNA की प्रतिकृति रुक जाती है।", "FDA 2025: सरल मूत्र मार्ग संक्रमण; मूत्रजननांगी गोनोरिया।"),
  'ja': ("ゲポチダシン（Blujepa）", "新しいクラス：トリアザアセナフチレン", "DNAジャイレースとトポイソメラーゼIVを阻害し、細菌のDNA複製を止める。", "FDA 2025年承認：単純性尿路感染症、泌尿生殖器淋菌感染症。"),
 },
 'image4': {
  'en': ("Zoliflodacin (Nuzolvence)", "New class: spiropyrimidinetrione", "Inhibits bacterial DNA gyrase at a site different from fluoroquinolones.", "FDA 2025: single oral dose for urogenital gonorrhoea."),
  'de': ("Zoliflodacin (Nuzolvence)", "Neue Klasse: Spiropyrimidintrion", "Hemmt die bakterielle DNA-Gyrase an einer anderen Stelle als Fluorchinolone.", "FDA 2025: orale Einmaldosis bei urogenitaler Gonorrhö."),
  'es': ("Zoliflodacina (Nuzolvence)", "Nueva clase: espiropirimidinatriona", "Inhibe la ADN girasa bacteriana en un sitio distinto al de las fluoroquinolonas.", "FDA 2025: dosis oral única para la gonorrea urogenital."),
  'ru': ("Золифлодацин (Nuzolvence)", "Новый класс: спиропиримидинтрионы", "Подавляет бактериальную ДНК-гиразу в участке, отличном от мишени фторхинолонов.", "FDA 2025: однократный приём внутрь при урогенитальной гонорее."),
  'zh': ("唑氟达星（Nuzolvence）", "新类别：螺嘧啶三酮类", "在不同于氟喹诺酮类的位点抑制细菌DNA旋转酶。", "FDA 2025年批准：单剂口服治疗泌尿生殖道淋病。"),
  'hi': ("ज़ोलिफ्लोडासिन (Nuzolvence)", "नया वर्ग: स्पाइरोपिरिमिडिनेट्रायोन", "फ्लोरोक्विनोलोन से अलग स्थान पर जीवाणु DNA गाइरेज़ को रोकती है।", "FDA 2025: मूत्रजननांगी गोनोरिया में मुँह से एक खुराक।"),
  'ja': ("ゾリフロダシン（Nuzolvence）", "新しいクラス：スピロピリミジントリオン", "フルオロキノロンとは異なる部位で細菌のDNAジャイレースを阻害する。", "FDA 2025年承認：泌尿生殖器淋菌感染症に経口単回投与。"),
 },
 'image5': {
  'en': ("Sulbactam–durlobactam (Xacduro)", "Combination aimed at Acinetobacter", "Sulbactam inhibits PBPs; durlobactam inhibits class A, C and D β-lactamases and protects sulbactam.", "FDA 2023: hospital-acquired and ventilator pneumonia caused by Acinetobacter."),
  'de': ("Sulbactam–Durlobactam (Xacduro)", "Kombination gegen Acinetobacter", "Sulbactam hemmt PBP; Durlobactam hemmt β-Lactamasen der Klassen A, C und D und schützt Sulbactam.", "FDA 2023: im Krankenhaus erworbene und beatmungsassoziierte Pneumonie durch Acinetobacter."),
  'es': ("Sulbactam–durlobactam (Xacduro)", "Combinación dirigida a Acinetobacter", "El sulbactam inhibe las PBP; el durlobactam inhibe las betalactamasas de clase A, C y D y protege al sulbactam.", "FDA 2023: neumonía hospitalaria y asociada a ventilación por Acinetobacter."),
  'ru': ("Сульбактам–дурлобактам (Xacduro)", "Комбинация против Acinetobacter", "Сульбактам подавляет ПСБ; дурлобактам подавляет бета-лактамазы классов A, C и D и защищает сульбактам.", "FDA 2023: госпитальная и вентилятор-ассоциированная пневмония, вызванная Acinetobacter."),
  'zh': ("舒巴坦–度洛巴坦（Xacduro）", "针对不动杆菌的复方", "舒巴坦抑制PBP；度洛巴坦抑制A、C、D类β-内酰胺酶，保护舒巴坦。", "FDA 2023年批准：不动杆菌引起的医院获得性及呼吸机相关性肺炎。"),
  'hi': ("सल्बैक्टम–डर्लोबैक्टम (Xacduro)", "एसिनेटोबैक्टर के लिए संयोजन", "सल्बैक्टम PBP को रोकता है; डर्लोबैक्टम A, C और D वर्ग के बीटा-लैक्टामेज़ को रोककर सल्बैक्टम की रक्षा करता है।", "FDA 2023: एसिनेटोबैक्टर से अस्पताल-जनित और वेंटिलेटर-संबंधी निमोनिया।"),
  'ja': ("スルバクタム–デュルロバクタム（Xacduro）", "アシネトバクターを標的とする配合剤", "スルバクタムはPBPを阻害し、デュルロバクタムはクラスA・C・Dのβラクタマーゼを阻害してスルバクタムを守る。", "FDA 2023年承認：アシネトバクターによる院内肺炎・人工呼吸器関連肺炎。"),
 },
 'image6': {
  'en': ("Ceftobiprole medocaril (Zevtera)", "Cephalosporin active against MRSA", "Binds several PBPs, including PBP2a, the MRSA resistance enzyme.", "FDA 2024: S. aureus bacteraemia, skin infections, community-acquired pneumonia."),
  'de': ("Ceftobiprol-Medocaril (Zevtera)", "Gegen MRSA wirksames Cephalosporin", "Bindet an mehrere PBP, darunter PBP2a, das Resistenzenzym von MRSA.", "FDA 2024: S.-aureus-Bakteriämie, Hautinfektionen, ambulant erworbene Pneumonie."),
  'es': ("Ceftobiprol medocarilo (Zevtera)", "Cefalosporina activa frente a SARM", "Se une a varias PBP, incluida la PBP2a, la enzima de resistencia del SARM.", "FDA 2024: bacteriemia por S. aureus, infecciones de piel, neumonía adquirida en la comunidad."),
  'ru': ("Цефтобипрол медокарил (Zevtera)", "Цефалоспорин, активный против MRSA", "Связывается с несколькими ПСБ, в том числе с ПСБ2a, ферментом резистентности MRSA.", "FDA 2024: бактериемия S. aureus, инфекции кожи, внебольничная пневмония."),
  'zh': ("头孢托罗酯（Zevtera）", "对MRSA有效的头孢菌素", "与多种PBP结合，包括MRSA的耐药酶PBP2a。", "FDA 2024年批准：金黄色葡萄球菌菌血症、皮肤感染、社区获得性肺炎。"),
  'hi': ("सेफ्टोबिप्रोल मेडोकेरिल (Zevtera)", "MRSA पर प्रभावी सेफलोस्पोरिन", "कई PBP से जुड़ती है, जिनमें MRSA का प्रतिरोधी एंज़ाइम PBP2a भी शामिल है।", "FDA 2024: S. aureus बैक्टीरिमिया, त्वचा संक्रमण, समुदाय-जनित निमोनिया।"),
  'ja': ("セフトビプロール メドカリル（Zevtera）", "MRSAに有効なセファロスポリン", "MRSAの耐性酵素PBP2aを含む複数のPBPに結合する。", "FDA 2024年承認：黄色ブドウ球菌菌血症、皮膚感染症、市中肺炎。"),
 },
 'image7': {
  'en': ("Cefepime–enmetazobactam (Exblifep)", "Cefepime + ESBL inhibitor", "Enmetazobactam inhibits ESBL-type β-lactamases and protects cefepime.", "FDA 2024: complicated urinary tract infection."),
  'de': ("Cefepim–Enmetazobactam (Exblifep)", "Cefepim + ESBL-Hemmer", "Enmetazobactam hemmt β-Lactamasen vom ESBL-Typ und schützt Cefepim.", "FDA 2024: komplizierte Harnwegsinfektion."),
  'es': ("Cefepima–enmetazobactam (Exblifep)", "Cefepima + inhibidor de BLEE", "El enmetazobactam inhibe las betalactamasas de tipo BLEE y protege a la cefepima.", "FDA 2024: infección urinaria complicada."),
  'ru': ("Цефепим–энметазобактам (Exblifep)", "Цефепим + ингибитор БЛРС", "Энметазобактам подавляет бета-лактамазы типа БЛРС и защищает цефепим.", "FDA 2024: осложнённая инфекция мочевых путей."),
  'zh': ("头孢吡肟–恩美他唑巴坦（Exblifep）", "头孢吡肟 + 超广谱β-内酰胺酶抑制剂", "恩美他唑巴坦抑制ESBL型β-内酰胺酶，保护头孢吡肟。", "FDA 2024年批准：复杂性尿路感染。"),
  'hi': ("सेफेपाइम–एनमेटाज़ोबैक्टम (Exblifep)", "सेफेपाइम + ESBL अवरोधक", "एनमेटाज़ोबैक्टम ESBL प्रकार के बीटा-लैक्टामेज़ को रोककर सेफेपाइम की रक्षा करता है।", "FDA 2024: जटिल मूत्र मार्ग संक्रमण।"),
  'ja': ("セフェピム–エンメタゾバクタム（Exblifep）", "セフェピム＋ESBL阻害薬", "エンメタゾバクタムがESBL型βラクタマーゼを阻害し、セフェピムを守る。", "FDA 2024年承認：複雑性尿路感染症。"),
 },
 'image8': {
  'en': ("Aztreonam–avibactam (Emblaveo)", "Monobactam + β-lactamase inhibitor", "Aztreonam binds PBP3; avibactam inhibits serine β-lactamases (ESBL, AmpC, KPC) but not metallo-β-lactamases.", "FDA 2025: complicated intra-abdominal infection, with metronidazole."),
  'de': ("Aztreonam–Avibactam (Emblaveo)", "Monobactam + β-Lactamase-Hemmer", "Aztreonam bindet an PBP3; Avibactam hemmt Serin-β-Lactamasen (ESBL, AmpC, KPC), aber keine Metallo-β-Lactamasen.", "FDA 2025: komplizierte intraabdominelle Infektion, mit Metronidazol."),
  'es': ("Aztreonam–avibactam (Emblaveo)", "Monobactámico + inhibidor de betalactamasas", "El aztreonam se une a la PBP3; el avibactam inhibe las serina-betalactamasas (BLEE, AmpC, KPC) pero no las metalobetalactamasas.", "FDA 2025: infección intraabdominal complicada, con metronidazol."),
  'ru': ("Азтреонам–авибактам (Emblaveo)", "Монобактам + ингибитор бета-лактамаз", "Азтреонам связывается с ПСБ3; авибактам подавляет сериновые бета-лактамазы (БЛРС, AmpC, KPC), но не металло-бета-лактамазы.", "FDA 2025: осложнённая интраабдоминальная инфекция, вместе с метронидазолом."),
  'zh': ("氨曲南–阿维巴坦（Emblaveo）", "单环β-内酰胺 + β-内酰胺酶抑制剂", "氨曲南结合PBP3；阿维巴坦抑制丝氨酸β-内酰胺酶（ESBL、AmpC、KPC），但不抑制金属β-内酰胺酶。", "FDA 2025年批准：复杂性腹腔内感染，与甲硝唑合用。"),
  'hi': ("एज़्ट्रियोनम–एविबैक्टम (Emblaveo)", "मोनोबैक्टम + बीटा-लैक्टामेज़ अवरोधक", "एज़्ट्रियोनम PBP3 से जुड़ता है; एविबैक्टम सेरीन बीटा-लैक्टामेज़ (ESBL, AmpC, KPC) को रोकता है, पर मेटालो-बीटा-लैक्टामेज़ को नहीं।", "FDA 2025: जटिल अंतर-उदरीय संक्रमण, मेट्रोनिडाज़ोल के साथ।"),
  'ja': ("アズトレオナム–アビバクタム（Emblaveo）", "モノバクタム＋βラクタマーゼ阻害薬", "アズトレオナムはPBP3に結合し、アビバクタムはセリン型βラクタマーゼ（ESBL、AmpC、KPC）を阻害するが、メタロβラクタマーゼは阻害しない。", "FDA 2025年承認：複雑性腹腔内感染症（メトロニダゾールと併用）。"),
 },
 'image9': {
  'en': ("Sulopenem etzadroxil–probenecid (Orlynvah)", "Oral penem + renal secretion blocker", "Sulopenem binds PBPs; probenecid reduces its renal excretion and raises its blood level.", "FDA 2024: uncomplicated urinary tract infection in women."),
  'de': ("Sulopenem-Etzadroxil–Probenecid (Orlynvah)", "Orales Penem + Hemmer der renalen Sekretion", "Sulopenem bindet an PBP; Probenecid vermindert die renale Ausscheidung und erhöht den Blutspiegel.", "FDA 2024: unkomplizierte Harnwegsinfektion bei Frauen."),
  'es': ("Sulopenem etzadroxilo–probenecid (Orlynvah)", "Penem oral + bloqueante de la secreción renal", "El sulopenem se une a las PBP; el probenecid reduce su excreción renal y eleva su nivel en sangre.", "FDA 2024: infección urinaria no complicada en mujeres."),
  'ru': ("Сулопенем этзадроксил–пробенецид (Orlynvah)", "Пероральный пенем + блокатор почечной секреции", "Сулопенем связывается с ПСБ; пробенецид уменьшает его выведение почками и повышает уровень в крови.", "FDA 2024: неосложнённая инфекция мочевых путей у женщин."),
  'zh': ("舒洛培南酯–丙磺舒（Orlynvah）", "口服青霉烯 + 肾小管分泌抑制剂", "舒洛培南结合PBP；丙磺舒减少其肾脏排泄，提高血药浓度。", "FDA 2024年批准：女性单纯性尿路感染。"),
  'hi': ("सुलोपेनेम एट्ज़ाड्रॉक्सिल–प्रोबेनेसिड (Orlynvah)", "मुँह से ली जाने वाली पेनेम + गुर्दे के स्राव का अवरोधक", "सुलोपेनेम PBP से जुड़ती है; प्रोबेनेसिड उसका गुर्दे से निकलना घटाकर रक्त स्तर बढ़ाता है।", "FDA 2024: महिलाओं में सरल मूत्र मार्ग संक्रमण।"),
  'ja': ("スロペネム エツァドロキシル–プロベネシド（Orlynvah）", "経口ペネム＋腎尿細管分泌阻害薬", "スロペネムはPBPに結合し、プロベネシドは腎排泄を抑えて血中濃度を高める。", "FDA 2024年承認：女性の単純性尿路感染症。"),
 },
 'image10': {
  'en': ("Pivmecillinam (Pivya)", "Aminopenicillin selective for PBP2", "Binds PBP2 selectively and blocks peptidoglycan synthesis.", "FDA 2024: uncomplicated urinary tract infection in women; used in Europe for over 40 years."),
  'de': ("Pivmecillinam (Pivya)", "PBP2-selektives Aminopenicillin", "Bindet selektiv an PBP2 und hemmt die Peptidoglykansynthese.", "FDA 2024: unkomplizierte Harnwegsinfektion bei Frauen; in Europa seit über 40 Jahren im Einsatz."),
  'es': ("Pivmecilinam (Pivya)", "Aminopenicilina selectiva de la PBP2", "Se une selectivamente a la PBP2 y bloquea la síntesis de peptidoglucano.", "FDA 2024: infección urinaria no complicada en mujeres; usado en Europa desde hace más de 40 años."),
  'ru': ("Пивмециллинам (Pivya)", "Аминопенициллин, селективный к ПСБ2", "Селективно связывается с ПСБ2 и блокирует синтез пептидогликана.", "FDA 2024: неосложнённая инфекция мочевых путей у женщин; в Европе применяется более 40 лет."),
  'zh': ("匹美西林（Pivya）", "选择性作用于PBP2的氨基青霉素", "选择性结合PBP2，阻断肽聚糖合成。", "FDA 2024年批准：女性单纯性尿路感染；在欧洲已使用40余年。"),
  'hi': ("पिवमेसिलिनैम (Pivya)", "PBP2 पर चयनात्मक अमीनोपेनिसिलिन", "चयनात्मक रूप से PBP2 से जुड़कर पेप्टिडोग्लाइकन संश्लेषण रोकती है।", "FDA 2024: महिलाओं में सरल मूत्र मार्ग संक्रमण; यूरोप में 40 वर्षों से अधिक समय से उपयोग में।"),
  'ja': ("ピブメシリナム（Pivya）", "PBP2選択的アミノペニシリン", "PBP2に選択的に結合し、ペプチドグリカン合成を阻害する。", "FDA 2024年承認：女性の単純性尿路感染症。欧州では40年以上使用。"),
 },
 'image11': {
  'en': ("Zosurabalpin (RG6006)", "Lipopolysaccharide (LPS) transport inhibitor", "Blocks the LptB2FGC complex, so LPS cannot reach the outer membrane; the bacterium dies.", "Phase III, not licensed. Target: carbapenem-resistant Acinetobacter baumannii."),
  'de': ("Zosurabalpin (RG6006)", "Hemmer des Lipopolysaccharid-(LPS-)Transports", "Blockiert den LptB2FGC-Komplex, sodass LPS die äußere Membran nicht erreicht; das Bakterium stirbt.", "Phase III, nicht zugelassen. Ziel: carbapenemresistenter Acinetobacter baumannii."),
  'es': ("Zosurabalpina (RG6006)", "Inhibidor del transporte de lipopolisacárido (LPS)", "Bloquea el complejo LptB2FGC; el LPS no llega a la membrana externa y la bacteria muere.", "Fase III, sin autorización. Objetivo: Acinetobacter baumannii resistente a carbapenémicos."),
  'ru': ("Зосурабалпин (RG6006)", "Ингибитор транспорта липополисахарида (ЛПС)", "Блокирует комплекс LptB2FGC, и ЛПС не достигает наружной мембраны; бактерия погибает.", "III фаза, не зарегистрирован. Мишень: карбапенем-резистентный Acinetobacter baumannii."),
  'zh': ("佐苏拉巴平（RG6006）", "脂多糖（LPS）转运抑制剂", "阻断LptB2FGC复合物，使LPS无法到达外膜，导致细菌死亡。", "III期临床，尚未获批。目标：耐碳青霉烯类鲍曼不动杆菌。"),
  'hi': ("ज़ोसुराबैल्पिन (RG6006)", "लिपोपॉलीसैकेराइड (LPS) परिवहन अवरोधक", "LptB2FGC कॉम्प्लेक्स को रोकती है, जिससे LPS बाहरी झिल्ली तक नहीं पहुँचता; जीवाणु मर जाता है।", "चरण III, अनुमोदित नहीं। लक्ष्य: कार्बापेनेम-प्रतिरोधी एसिनेटोबैक्टर बाउमानी।"),
  'ja': ("ゾスラバルピン（RG6006）", "リポ多糖（LPS）輸送阻害薬", "LptB2FGC複合体を阻害してLPSが外膜に届かなくなり、細菌が死滅する。", "第III相、未承認。標的：カルバペネム耐性アシネトバクター・バウマニ。"),
 },
 'image12': {
  'en': ("Manicomycin", "Ribosomal protein synthesis inhibitor (50S, E site)", "Binds the E site of the 50S ribosomal subunit and stops protein synthesis.", "Preclinical; no data in humans."),
  'de': ("Manikomycin", "Hemmer der ribosomalen Proteinsynthese (50S, E-Stelle)", "Bindet an die E-Stelle der 50S-Untereinheit des Ribosoms und stoppt die Proteinsynthese.", "Präklinisch; keine Daten am Menschen."),
  'es': ("Manicomicina", "Inhibidor de la síntesis proteica ribosómica (50S, sitio E)", "Se une al sitio E de la subunidad ribosómica 50S y detiene la síntesis de proteínas.", "Preclínica; sin datos en humanos."),
  'ru': ("Маникомицин", "Ингибитор синтеза белка на рибосоме (50S, E-сайт)", "Связывается с E-сайтом субъединицы 50S рибосомы и останавливает синтез белка.", "Доклиническая стадия; данных у человека нет."),
  'zh': ("马尼霉素", "核糖体蛋白合成抑制剂（50S，E位点）", "结合核糖体50S亚基的E位点，阻止蛋白质合成。", "临床前阶段；无人体数据。"),
  'hi': ("मैनिकोमाइसिन", "राइबोसोमीय प्रोटीन संश्लेषण अवरोधक (50S, E स्थल)", "राइबोसोम की 50S उप-इकाई के E स्थल से जुड़कर प्रोटीन संश्लेषण रोकती है।", "प्रीक्लिनिकल; मनुष्यों में कोई आँकड़े नहीं।"),
  'ja': ("マニコマイシン", "リボソームのタンパク質合成阻害薬（50S、E部位）", "リボソーム50SサブユニットのE部位に結合し、タンパク質合成を止める。", "前臨床段階。ヒトでのデータはない。"),
 },
 'image13': {
  'en': ("Pre-methylenomycin C lactone", "New natural-product antibacterial", "Its exact molecular target is not yet known.", "Preclinical; in the laboratory active against Gram-positive bacteria, including MRSA and VRE."),
  'de': ("Prä-Methylenomycin-C-Lacton", "Neuer antibakterieller Naturstoff", "Das genaue molekulare Ziel ist noch nicht bekannt.", "Präklinisch; im Labor wirksam gegen grampositive Bakterien, auch MRSA und VRE."),
  'es': ("Lactona de pre-metilenomicina C", "Nuevo antibacteriano de origen natural", "Su diana molecular exacta aún no se conoce.", "Preclínica; en el laboratorio activa frente a grampositivos, incluidos SARM y ERV."),
  'ru': ("Лактон пре-метиленомицина C", "Новое природное антибактериальное вещество", "Точная молекулярная мишень пока неизвестна.", "Доклиническая стадия; в лаборатории активен против грамположительных бактерий, включая MRSA и VRE."),
  'zh': ("前亚甲霉素C内酯", "新型天然产物抗菌物质", "其确切分子靶点尚不清楚。", "临床前阶段；实验室中对革兰阳性菌（包括MRSA和VRE）有活性。"),
  'hi': ("प्री-मिथाइलेनोमाइसिन C लैक्टोन", "नया प्राकृतिक जीवाणुरोधी पदार्थ", "इसका सटीक आणविक लक्ष्य अभी ज्ञात नहीं है।", "प्रीक्लिनिकल; प्रयोगशाला में MRSA और VRE सहित ग्राम-पॉज़िटिव जीवाणुओं पर सक्रिय।"),
  'ja': ("プレメチレノマイシンCラクトン", "天然物由来の新しい抗菌物質", "正確な分子標的はまだ分かっていない。", "前臨床段階。実験室ではMRSAやVREを含むグラム陽性菌に活性を示す。"),
 },
}
for k, v in DRUGS.items():
    CARDS['b33_antib_' + k] = ('navy', {l: D(K[l], v[l][0], v[l][1], None, None, [(MECH[l], v[l][2]), (STAT[l], v[l][3])], NOTE[l]) for l in L})

# Cover collage of 12 diagrams
CT = {
 'en': ("NEW ANTIBIOTICS AND THEIR FEATURES", "How the new antibacterials work",
        [("New classes:", "gepotidacin, zoliflodacin"), ("Combinations:", "sulbactam–durlobactam, aztreonam–avibactam, cefepime–enmetazobactam"),
         ("New US licences for older drugs:", "ceftobiprole, pivmecillinam"), ("Oral options:", "tebipenem pivoxil, sulopenem–probenecid"),
         ("Research stage:", "zosurabalpin, manicomycin, pre-methylenomycin C lactone")]),
 'de': ("NEUE ANTIBIOTIKA UND IHRE EIGENSCHAFTEN", "Wie die neuen antibakteriellen Wirkstoffe wirken",
        [("Neue Klassen:", "Gepotidacin, Zoliflodacin"), ("Kombinationen:", "Sulbactam–Durlobactam, Aztreonam–Avibactam, Cefepim–Enmetazobactam"),
         ("Neue US-Zulassung für ältere Wirkstoffe:", "Ceftobiprol, Pivmecillinam"), ("Orale Optionen:", "Tebipenem-Pivoxil, Sulopenem–Probenecid"),
         ("Forschungsphase:", "Zosurabalpin, Manikomycin, Prä-Methylenomycin-C-Lacton")]),
 'es': ("NUEVOS ANTIBIÓTICOS Y SUS CARACTERÍSTICAS", "Cómo actúan los nuevos antibacterianos",
        [("Nuevas clases:", "gepotidacina, zoliflodacina"), ("Combinaciones:", "sulbactam–durlobactam, aztreonam–avibactam, cefepima–enmetazobactam"),
         ("Nueva autorización en EE. UU. de fármacos antiguos:", "ceftobiprol, pivmecilinam"), ("Opciones orales:", "tebipenem pivoxilo, sulopenem–probenecid"),
         ("En investigación:", "zosurabalpina, manicomicina, lactona de pre-metilenomicina C")]),
 'ru': ("НОВЫЕ АНТИБИОТИКИ И ИХ ОСОБЕННОСТИ", "Как действуют новые антибактериальные средства",
        [("Новые классы:", "гепотидацин, золифлодацин"), ("Комбинации:", "сульбактам–дурлобактам, азтреонам–авибактам, цефепим–энметазобактам"),
         ("Новая регистрация в США для старых препаратов:", "цефтобипрол, пивмециллинам"), ("Пероральные варианты:", "тебипенем пивоксил, сулопенем–пробенецид"),
         ("На стадии исследований:", "зосурабалпин, маникомицин, лактон пре-метиленомицина C")]),
 'zh': ("新型抗生素及其特点", "新型抗菌药物如何发挥作用",
        [("新类别：", "吉泊达星、唑氟达星"), ("复方制剂：", "舒巴坦–度洛巴坦、氨曲南–阿维巴坦、头孢吡肟–恩美他唑巴坦"),
         ("老药在美国新获批：", "头孢托罗、匹美西林"), ("口服选择：", "替比培南酯、舒洛培南–丙磺舒"),
         ("研究阶段：", "佐苏拉巴平、马尼霉素、前亚甲霉素C内酯")]),
 'hi': ("नए एंटीबायोटिक और उनकी विशेषताएँ", "नई जीवाणुरोधी दवाएँ कैसे काम करती हैं",
        [("नए वर्ग:", "जेपोटिडासिन, ज़ोलिफ्लोडासिन"), ("संयोजन:", "सल्बैक्टम–डर्लोबैक्टम, एज़्ट्रियोनम–एविबैक्टम, सेफेपाइम–एनमेटाज़ोबैक्टम"),
         ("पुरानी दवाओं को अमेरिका में नई मंज़ूरी:", "सेफ्टोबिप्रोल, पिवमेसिलिनैम"), ("मुँह से लेने के विकल्प:", "टेबिपेनेम पिवॉक्सिल, सुलोपेनेम–प्रोबेनेसिड"),
         ("अनुसंधान चरण:", "ज़ोसुराबैल्पिन, मैनिकोमाइसिन, प्री-मिथाइलेनोमाइसिन C लैक्टोन")]),
 'ja': ("新しい抗菌薬とその特徴", "新しい抗菌薬はどのように作用するか",
        [("新しいクラス：", "ゲポチダシン、ゾリフロダシン"), ("配合剤：", "スルバクタム–デュルロバクタム、アズトレオナム–アビバクタム、セフェピム–エンメタゾバクタム"),
         ("既存薬の米国での新規承認：", "セフトビプロール、ピブメシリナム"), ("経口薬：", "テビペネム ピボキシル、スロペネム–プロベネシド"),
         ("研究段階：", "ゾスラバルピン、マニコマイシン、プレメチレノマイシンCラクトン")]),
}
CARDS['b33_antib_kapak'] = ('burg', {l: D(K[l], CT[l][0], CT[l][1], None, None, CT[l][2], NOTE[l]) for l in L})

# Article is published without the author's name (author's request), so the cards carry none either.
for _t, _langs in CARDS.values():
    for _d in _langs.values(): _d['noauthor'] = True
