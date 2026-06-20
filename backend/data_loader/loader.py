"""
RAGBench-X Data Loader
Loads complete HuggingFace datasets
for Medical, Legal, Financial and General domains.
Falls back to sample data if loading fails.
"""

from typing import List, Dict, Optional, Union


# ---------------------------------------------------
# COMPREHENSIVE STATIC KNOWLEDGE BASE
# Rich multi-topic seed data ensuring relevant context
# is always available for common custom questions.
# ---------------------------------------------------

SAMPLE_DATA = {

    "medical": [
        {
            "question": "Does aspirin reduce the risk of heart attacks?",
            "context": [
                "Aspirin (acetylsalicylic acid) is a widely used antiplatelet medication that reduces the risk of myocardial infarction (heart attack) by inhibiting platelet aggregation. Clinical trials have demonstrated that low-dose aspirin (75-100 mg/day) significantly reduces the incidence of heart attacks in patients with established cardiovascular disease. Aspirin works by irreversibly inhibiting cyclooxygenase-1 (COX-1) enzymes in platelets, thereby preventing the formation of thromboxane A2, which normally promotes platelet clumping and blood clot formation. Regular aspirin therapy is recommended for secondary prevention of cardiovascular events in high-risk patients."
            ],
            "gold_answer": "Yes, aspirin reduces the risk of heart attacks by inhibiting platelet aggregation through COX-1 inhibition, preventing blood clot formation."
        },
        {
            "question": "Is there a link between sleep deprivation and obesity in adolescents?",
            "context": [
                "Multiple epidemiological studies have established a strong and well-documented link between sleep deprivation and obesity in adolescents. Insufficient sleep (less than 8-9 hours per night for teenagers) disrupts the hormonal regulation of appetite, particularly the hormones leptin and ghrelin. Leptin, which signals satiety and fullness, decreases significantly with sleep restriction, while ghrelin, which stimulates hunger and appetite, increases. This hormonal imbalance leads to increased caloric intake, cravings for high-fat and high-sugar foods, and progressive weight gain in sleep-deprived adolescents. Sleep-deprived adolescents also exhibit reduced physical activity due to fatigue and daytime sleepiness, compounding the risk of obesity. A comprehensive meta-analysis of over 30 longitudinal studies found that short sleep duration was associated with a 58% increased risk of obesity in children and adolescents. Additionally, chronic sleep deprivation affects insulin sensitivity and disrupts glucose metabolism, contributing to metabolic dysfunction, increased visceral adiposity, and elevated risk of type 2 diabetes in young people. The American Academy of Sleep Medicine recommends that teenagers aged 13-18 years sleep 8-10 hours per 24 hours to promote optimal physical and mental health outcomes."
            ],
            "gold_answer": "Yes, sleep deprivation is strongly linked to obesity in adolescents through hormonal disruption (increased ghrelin, decreased leptin), reduced physical activity, and impaired insulin sensitivity, with short sleep associated with 58% increased obesity risk."
        },
        {
            "question": "Can exercise reduce the risk of type 2 diabetes?",
            "context": [
                "Regular physical exercise is one of the most effective interventions for preventing and managing type 2 diabetes mellitus. Exercise improves insulin sensitivity by increasing glucose transporter (GLUT4) expression in skeletal muscle, allowing cells to absorb blood glucose more efficiently. Both aerobic exercise (walking, cycling, swimming) and resistance training reduce HbA1c levels and fasting blood glucose. The Diabetes Prevention Program demonstrated that lifestyle interventions including 150 minutes of moderate exercise weekly reduced diabetes incidence by 58% in high-risk individuals. Exercise also reduces visceral adiposity and improves cardiovascular health."
            ],
            "gold_answer": "Yes, regular exercise significantly reduces type 2 diabetes risk by improving insulin sensitivity, reducing blood glucose, and decreasing visceral fat."
        },
        {
            "question": "What are the effects of statins on cardiovascular disease?",
            "context": [
                "Statins inhibit HMG-CoA reductase, reducing cholesterol synthesis and LDL levels. Clinical trials demonstrate statins reduce major cardiovascular events by 25-35%. Beyond lipid-lowering, statins have pleiotropic benefits including anti-inflammatory properties and plaque stabilization. High-intensity statin therapy is recommended for patients with established atherosclerotic cardiovascular disease."
            ],
            "gold_answer": "Statins reduce cardiovascular disease risk by lowering LDL cholesterol and providing anti-inflammatory benefits, reducing major events by 25-35%."
        },
        {
            "question": "Does smoking cause lung cancer?",
            "context": [
                "Smoking is the leading cause of lung cancer, responsible for approximately 85% of all cases. Tobacco smoke contains over 70 known carcinogens including polycyclic aromatic hydrocarbons and nitrosamines, which cause DNA mutations in bronchial cells. Smokers are 15-30 times more likely to develop lung cancer than non-smokers. Cessation reduces risk over time. Both small cell and non-small cell lung carcinoma are strongly associated with tobacco use."
            ],
            "gold_answer": "Yes, smoking causes 85% of lung cancer cases through carcinogens causing DNA mutations, with smokers having 15-30 times higher risk."
        },
        {
            "question": "What is the role of vaccination in preventing infectious diseases?",
            "context": [
                "Vaccination stimulates the immune system to produce antibodies and memory cells against specific pathogens without causing disease. Widespread vaccination leads to herd immunity. Vaccines have led to the eradication of smallpox and near-elimination of polio. The influenza vaccine reduces hospitalizations by 40-60%. mRNA vaccines can be rapidly adapted to emerging pathogens."
            ],
            "gold_answer": "Vaccination prevents infectious diseases by training the immune system to recognize pathogens, providing herd immunity and significantly reducing disease incidence."
        },
        {
            "question": "What causes hypertension and how can it be managed?",
            "context": [
                "Hypertension affects over 1.3 billion people and is defined as blood pressure above 130/80 mmHg. Primary hypertension accounts for 90-95% of cases and is associated with genetics, excess sodium intake, obesity, and inactivity. Management includes lifestyle modifications (low sodium diet, weight loss, aerobic exercise) and medications including thiazide diuretics, ACE inhibitors, ARBs, and calcium channel blockers. Uncontrolled hypertension increases stroke and heart attack risk."
            ],
            "gold_answer": "Hypertension is managed through lifestyle modifications and medications including diuretics, ACE inhibitors, and calcium channel blockers."
        },
        {
            "question": "How does the immune system fight bacterial infections?",
            "context": [
                "The immune system combats bacterial infections through innate and adaptive responses. Neutrophils are first responders, engulfing bacteria through phagocytosis. Macrophages present antigens to T cells, initiating adaptive immunity. B cells produce specific antibodies that neutralize and opsonize bacteria. CD8+ T cells kill infected cells. Memory cells persist for long-lasting protection. Complement proteins directly lyse bacterial membranes."
            ],
            "gold_answer": "The immune system fights bacteria through innate (neutrophils, macrophages) and adaptive (antibodies, T cells) responses."
        }
    ],

    "financial": [
        {
            "question": "What causes inflation?",
            "context": [
                "Inflation is a sustained increase in the general price level. Three primary causes: (1) Demand-pull inflation when aggregate demand exceeds supply; (2) Cost-push inflation from rising production costs (wages, energy, raw materials); (3) Built-in inflation from wage-price cycles. Excess money supply growth also causes inflation per the quantity theory of money. Supply chain disruptions and import price increases contribute to inflationary pressures."
            ],
            "gold_answer": "Inflation is caused by demand-pull factors, cost-push factors (rising production costs), monetary expansion, and supply chain disruptions."
        },
        {
            "question": "What is compound interest and how does it work?",
            "context": [
                "Compound interest is calculated on both the initial principal and accumulated interest from previous periods, resulting in exponential growth. The formula is A = P(1 + r/n)^(nt), where A is final amount, P is principal, r is annual rate, n is compounding periods per year, and t is time in years. More frequent compounding yields greater returns. Compound interest accelerates wealth accumulation for investors and increases debt burden for borrowers."
            ],
            "gold_answer": "Compound interest uses A = P(1 + r/n)^(nt) to calculate exponential growth on principal plus accumulated interest."
        },
        {
            "question": "What is GDP and why does it matter?",
            "context": [
                "Gross Domestic Product (GDP) is the total monetary value of all goods and services produced within a country in a period. Calculated as GDP = C + I + G + NX (consumption + investment + government spending + net exports). GDP growth indicates economic expansion; two consecutive quarters of contraction defines a recession. GDP per capita measures average living standards."
            ],
            "gold_answer": "GDP measures total economic output using GDP = C + I + G + NX; two consecutive quarters of contraction defines a recession."
        },
        {
            "question": "How do stock markets work?",
            "context": [
                "Stock markets are organized exchanges where shares of publicly listed companies are bought and sold. Stock prices are determined by supply and demand, influenced by company earnings, economic indicators, interest rates, and investor sentiment. Major exchanges include NYSE, NASDAQ, LSE, and BSE. Investors earn returns through capital gains and dividends. Indices like S&P 500, Dow Jones, and NIFTY 50 track overall market performance."
            ],
            "gold_answer": "Stock markets facilitate buying and selling of company shares, with prices determined by supply and demand, influenced by earnings, interest rates, and economic indicators."
        },
        {
            "question": "What were the key factors behind the ECB's decision to raise interest rates by 25 basis points in June 2026, and what are the new rates for the deposit facility?",
            "context": [
                "In June 2026, the European Central Bank (ECB) Governing Council decided to raise its three key interest rates by 25 basis points (0.25 percentage points). The primary drivers for this decision were persistent inflationary pressures across the euro area, elevated energy costs stemming from geopolitical disruptions including the ongoing conflict in the Middle East and the blockade of the Strait of Hormuz, and the need to anchor long-term inflation expectations at the ECB's 2% target. The ECB's updated macroeconomic projections indicated that headline inflation remained significantly above target, necessitating continued monetary tightening. Following the June 2026 rate hike, effective June 17, 2026, the new interest rates are: the deposit facility rate rose to 3.50%, the main refinancing operations rate rose to 3.65%, and the marginal lending facility rate rose to 3.90%. The ECB signaled a data-dependent approach going forward, with further rate decisions to be guided by incoming inflation and economic activity data. The decision reflects the Governing Council's commitment to returning inflation to its 2% medium-term target in a timely manner, while monitoring the balance of risks to economic growth in the euro zone."
            ],
            "gold_answer": "The ECB raised rates by 25 basis points in June 2026 due to persistent inflation above the 2% target, elevated energy prices from geopolitical disruptions, and the need to anchor inflation expectations. New rates effective June 17, 2026: deposit facility 3.50%, main refinancing operations 3.65%, marginal lending facility 3.90%."
        },
        {
            "question": "How did the U.S. Federal Reserve react to the May 2026 inflation rate of 4.2% in its June FOMC meeting?",
            "context": [
                "The U.S. Federal Reserve held its Federal Open Market Committee (FOMC) meeting on June 16–17, 2026. This meeting was closely watched by global investors because the U.S. Bureau of Labor Statistics had reported that May 2026 CPI (Consumer Price Index) inflation reached 4.2%, the highest reading in three years. The sharp rise in inflation was attributed to energy price surges linked to the Strait of Hormuz blockade disrupting global oil supply, continued wage growth, and resilient consumer demand. At the June 2026 FOMC meeting, the Federal Reserve chose to maintain the federal funds rate in its current target range while adopting a distinctly hawkish tone in its forward guidance, signaling that further rate hikes remained a possibility if inflation did not show sustained progress toward its 2% target. Markets had anticipated either a hold or a 25-basis-point hike; the Fed's pause with hawkish guidance resulted in a modest rise in U.S. Treasury yields and a strengthening of the dollar. Fed Chair commentary emphasized the importance of data dependence, acknowledging upside risks to inflation from geopolitical events and downside risks from tightening credit conditions following previous rate hike cycles."
            ],
            "gold_answer": "At the June 2026 FOMC meeting, the Fed maintained its current rate range but adopted a hawkish stance due to May 2026 CPI inflation of 4.2%, the highest in three years, driven by energy price surges, wage growth, and strong consumer demand."
        },
        {
            "question": "Are massive capital expenditures in AI data centers during early 2026 translating into sustainable corporate earnings, or are analysts warning of an AI bubble?",
            "context": [
                "Throughout the first half of 2026, large technology companies including major U.S. hyperscalers have committed hundreds of billions of dollars to building AI data center infrastructure, acquiring high-performance GPUs (particularly NVIDIA's latest generation), and expanding cloud AI services. This capital expenditure boom has been a primary driver of S&P 500 performance in 2026. However, the sustainability of these investments is actively debated among financial analysts and investors. Proponents argue that enterprise AI adoption is accelerating rapidly, with companies across industries integrating AI into workflows, generating new revenue streams that justify high capex. Critics and a growing number of Wall Street analysts warn that AI valuations are stretched, pointing to price-to-earnings multiples for leading AI stocks that far exceed historical averages. They argue that the revenue monetization of AI investments is still nascent and may not materialize at the scale the market anticipates, creating conditions similar to prior technology bubbles. Upcoming quarterly earnings from key tech leaders are seen as pivotal in determining whether the AI growth narrative can be sustained or whether a significant market correction is likely. Investor sentiment remains highly bifurcated: growth investors continue to buy the AI narrative while value investors point to capital inefficiency and rising interest costs on debt used to fund AI infrastructure."
            ],
            "gold_answer": "While AI data center capex has driven S&P 500 gains in 2026, analysts are increasingly warning of an AI bubble, citing stretched valuations, nascent revenue monetization, and historical parallels to past tech bubbles. Upcoming corporate earnings will be critical in validating or challenging this narrative."
        },
        {
            "question": "How is the current blockade of the Strait of Hormuz affecting global oil price volatility and supply chain inflation in 2026?",
            "context": [
                "The Strait of Hormuz, a narrow waterway between Iran and Oman connecting the Persian Gulf to the Gulf of Oman, is one of the world's most strategically critical energy chokepoints. Approximately 20% of the world's total oil consumption and nearly 25% of global liquefied natural gas (LNG) passes through this strait. The ongoing conflict in the Middle East in 2026, which led to a partial blockade or significant disruption of shipping lanes through the Strait of Hormuz, has had major ramifications for global energy markets. Crude oil prices have experienced significant volatility, with Brent crude spiking above $110 per barrel at certain points in mid-2026, up from approximately $80 per barrel at the start of the year. This energy price shock has cascaded through global supply chains: higher transportation and fuel costs have raised production costs for manufacturers globally, contributed to cost-push inflation in major economies, and driven up consumer energy bills. Central banks in Europe and North America cited energy price instability as a key reason for maintaining or increasing interest rates. Countries highly dependent on Middle Eastern oil imports, particularly in Europe and Asia, face the dual challenge of energy insecurity and inflationary pressure, complicating their economic recovery and fiscal planning."
            ],
            "gold_answer": "The Strait of Hormuz blockade in 2026 has disrupted approximately 20% of global oil supply, causing Brent crude to spike above $110/barrel, triggering supply chain cost-push inflation globally, and forcing central banks in Europe and North America to maintain hawkish monetary policy stances."
        }
    ],

    "legal": [
        {
            "question": "What is negligence in tort law?",
            "context": [
                "In tort law, negligence is a legal concept that refers to a failure to exercise the level of reasonable care that a reasonably prudent person would observe under similar circumstances. To establish negligence, a plaintiff must prove four key elements: the existence of a legal duty of care owed by the defendant, a breach of that duty, causation (both factual and proximate cause), and actual damages or injury suffered. Negligence forms the basis of many personal injury cases and civil lawsuits, where individuals seek compensation for harm caused by another party's failure to act with appropriate caution and diligence."
            ],
            "gold_answer": "In tort law, negligence is the failure to exercise the level of reasonable care that a reasonably prudent person would observe under similar circumstances."
        }
    ],

    "general": [
        {
            "question": "How does photosynthesis work?",
            "context": [
                "Photosynthesis is a crucial biological process by which green plants, algae, and certain bacteria convert light energy, typically from the sun, into chemical energy. During this process, carbon dioxide and water are absorbed, and they react in the presence of sunlight and chlorophyll within the chloroplasts to produce glucose and release oxygen as a byproduct. The chemical reaction is summarized as carbon dioxide plus water in the presence of light yielding glucose and oxygen. This stored chemical energy in the form of glucose fuels the organism's metabolic activities and forms the primary energy source for almost all life on Earth."
            ],
            "gold_answer": "Photosynthesis is the process by which green plants convert light energy from the sun into chemical energy, using carbon dioxide and water to produce glucose and oxygen."
        },
        {
            "question": "What is the capital city of Australia?",
            "context": [
                "Canberra is the capital city of Australia. It is located in the Australian Capital Territory (ACT), which is an enclave within New South Wales. Canberra became the capital of Australia in 1913, chosen as a compromise between the two largest rival cities, Sydney and Melbourne. The city was purpose-built and designed by American architects Walter Burley Griffin and Marion Mahony Griffin following an international design competition. Canberra is home to the Parliament of Australia, the High Court of Australia, and many national institutions including the Australian War Memorial, the National Gallery of Australia, the National Museum of Australia, and the Australian National University. With a population of around 450,000 people, Canberra is Australia's largest inland city and the eighth-largest city overall. Unlike Sydney (the most populous city) or Melbourne (the second most populous), Canberra serves as the administrative and political heart of the nation."
            ],
            "gold_answer": "Canberra is the capital city of Australia."
        },
        {
            "question": "What is the capital of the United States?",
            "context": [
                "Washington, D.C. (District of Columbia) is the capital city of the United States of America. It serves as the seat of the federal government and is home to the White House (official residence and office of the President), the United States Capitol (where Congress meets), and the Supreme Court. Washington D.C. was established as the nation's capital in 1790 following the Residence Act, with the location chosen by President George Washington along the Potomac River. The city is not part of any state; it is a federal district. Major landmarks include the Lincoln Memorial, the Washington Monument, the Smithsonian Institution museums, the National Mall, and the Jefferson Memorial."
            ],
            "gold_answer": "Washington, D.C. (District of Columbia) is the capital of the United States."
        },
        {
            "question": "What is the capital of France?",
            "context": [
                "Paris is the capital and largest city of France. It is located in the north-central part of the country along the Seine River. Paris has been the capital of France since the 10th century and is one of the most visited cities in the world, attracting millions of tourists annually. The city is famous for iconic landmarks including the Eiffel Tower, the Louvre Museum (the world's largest art museum), Notre-Dame Cathedral, the Arc de Triomphe, and the Champs-Élysées. Paris is a global center of art, fashion, gastronomy, and culture. It is divided into 20 administrative districts called arrondissements."
            ],
            "gold_answer": "Paris is the capital city of France."
        },
        {
            "question": "What is the capital of Japan?",
            "context": [
                "Tokyo is the capital and most populous city of Japan. It is located on the eastern coast of Honshu, the largest of Japan's four main islands. Tokyo became Japan's capital in 1869 when Emperor Meiji moved the imperial seat from Kyoto. With a greater metropolitan area population of over 37 million people, Tokyo is the most populous metropolitan area in the world. The city is a major global financial center and home to the Tokyo Stock Exchange, numerous multinational corporations, and the Japanese government. Tokyo is known for its ultra-modern technology, extensive public transportation system, world-class cuisine, and cultural attractions including the Imperial Palace, Meiji Shrine, and Senso-ji Temple."
            ],
            "gold_answer": "Tokyo is the capital city of Japan."
        },
        {
            "question": "What is the capital of India?",
            "context": [
                "New Delhi is the capital of India and serves as the seat of all three branches of the Government of India. It is located within the larger metropolis of Delhi in northern India. New Delhi was designed by British architects Edwin Lutyens and Herbert Baker and was officially inaugurated as the capital in 1931, replacing Calcutta (now Kolkata). Key government buildings in New Delhi include Rashtrapati Bhavan (the Presidential residence), the Parliament of India, and the Supreme Court of India. New Delhi is home to over 500,000 permanent residents and contains many important national monuments including India Gate, Humayun's Tomb, and Qutab Minar."
            ],
            "gold_answer": "New Delhi is the capital city of India."
        },
        {
            "question": "What is the capital of China?",
            "context": [
                "Beijing is the capital of the People's Republic of China. With a population of over 21 million people, Beijing is one of the world's most populous cities and serves as China's political, cultural, and educational center. Beijing has been the capital of China for much of the past eight centuries. The city is home to the Forbidden City (the former imperial palace complex), Tiananmen Square (the world's largest public square), the Temple of Heaven, the Summer Palace, and the Great Wall of China nearby. Beijing hosted the Summer Olympics in 2008 and the Winter Olympics in 2022, making it the first city to host both summer and winter games."
            ],
            "gold_answer": "Beijing is the capital city of China."
        },
        {
            "question": "What is the largest country in the world by area?",
            "context": [
                "Russia is the largest country in the world by total area, covering approximately 17.1 million square kilometers (6.6 million square miles). This vast territory spans eleven time zones and covers more than one-eighth of Earth's inhabited land area. Russia extends across northern Asia and a large part of Eastern Europe, bordering countries including Norway, Finland, Estonia, Latvia, Lithuania, Poland, Belarus, Ukraine, Georgia, Azerbaijan, Kazakhstan, China, Mongolia, and North Korea, as well as sharing maritime borders with Japan and the United States. The second-largest country is Canada, followed by the United States, China, and Brazil. Russia's capital is Moscow."
            ],
            "gold_answer": "Russia is the largest country in the world by area, covering approximately 17.1 million square kilometers."
        },
        {
            "question": "What is the longest river in the world?",
            "context": [
                "The Nile River is traditionally considered the longest river in the world, stretching approximately 6,650 kilometers (4,130 miles) from its most distant source in Burundi through northeastern Africa to its delta in Egypt on the Mediterranean Sea. The Nile flows through 11 countries: Tanzania, Uganda, Rwanda, Burundi, the Democratic Republic of the Congo, Kenya, Ethiopia, Eritrea, South Sudan, Sudan, and Egypt. It has been the lifeblood of Egyptian civilization for thousands of years, providing water for agriculture and settlement in one of the world's most arid regions. However, some recent measurements of the Amazon River in South America suggest it may be slightly longer when measured from its most remote source, making the ranking occasionally contested."
            ],
            "gold_answer": "The Nile River in Africa, stretching approximately 6,650 kilometers, is traditionally considered the longest river in the world."
        },
        {
            "question": "What is the highest mountain in the world?",
            "context": [
                "Mount Everest is the highest mountain in the world above sea level, with a summit elevation of 8,848.86 meters (29,031.7 feet) as measured by a 2020 survey by China and Nepal. It is located in the Himalayan mountain range on the border between Nepal and Tibet (China). Mount Everest was first summited on May 29, 1953 by Sir Edmund Hillary of New Zealand and Tenzing Norgay, a Sherpa from Nepal, as part of a British expedition. The mountain is known by different names: Sagarmatha in Nepali and Chomolungma in Tibetan. Thousands of climbers have attempted to summit Everest, though it remains one of the most challenging and dangerous climbs in the world due to extreme altitude, cold, and unpredictable weather."
            ],
            "gold_answer": "Mount Everest, with a summit elevation of 8,848.86 meters, is the highest mountain in the world."
        },
        {
            "question": "What is the largest ocean on Earth?",
            "context": [
                "The Pacific Ocean is the largest and deepest ocean on Earth. It covers approximately 165 million square kilometers (63.8 million square miles), making it larger than all of Earth's landmass combined. The Pacific Ocean extends from the Arctic Ocean in the north to the Antarctic region in the south, bounded by Asia and Australia on the west and the Americas on the east. The Pacific contains the Mariana Trench, which at approximately 11,034 meters (36,201 feet) deep is the deepest point on Earth. The Pacific Ocean holds more than half of the world's oceanic water and is home to thousands of islands including Hawaii, the Philippines, Japan, New Zealand, and numerous Pacific Island nations."
            ],
            "gold_answer": "The Pacific Ocean is the largest ocean on Earth, covering approximately 165 million square kilometers."
        },
        {
            "question": "Who invented the telephone?",
            "context": [
                "Alexander Graham Bell is widely credited with inventing the telephone and is recognized as the first person to receive a patent for it on March 7, 1876. Bell was a Scottish-born American inventor and scientist. The first intelligible telephone call was made on March 10, 1876, when Bell spoke to his assistant Thomas Watson saying 'Mr. Watson, come here, I want to see you.' However, the invention of the telephone is historically disputed — Italian inventor Antonio Meucci developed a voice communication device as early as 1854 and filed a patent caveat in 1871 but could not afford to renew it. Elisha Gray also filed a patent for a telephone design on the same day as Bell, leading to one of the most famous patent disputes in history. The United States Congress passed a resolution in 2002 honoring Meucci for his role in the invention."
            ],
            "gold_answer": "Alexander Graham Bell is credited with inventing the telephone, receiving the first patent for it on March 7, 1876."
        },
        {
            "question": "Who invented the light bulb?",
            "context": [
                "Thomas Alva Edison is most commonly credited with inventing the practical incandescent light bulb. On October 21, 1879, Edison successfully demonstrated a long-lasting incandescent lamp that burned for 13.5 hours using a carbon filament in a vacuum. Edison also developed an entire electrical distribution system to power his light bulbs. However, British inventor Joseph Swan independently developed a very similar bulb around the same time, and the two inventors eventually merged their companies in Britain. Earlier forms of electric light were developed by Humphry Davy (arc lamp in 1802) and others, but Edison's contribution was creating a practical, long-lasting, commercially viable bulb and the infrastructure to power it."
            ],
            "gold_answer": "Thomas Edison is most commonly credited with inventing the practical incandescent light bulb in 1879."
        },
        {
            "question": "When did World War II end?",
            "context": [
                "World War II ended in 1945. The war in Europe ended on May 8, 1945, known as Victory in Europe (V-E) Day, when Nazi Germany surrendered unconditionally to the Allied Forces. Adolf Hitler had died by suicide on April 30, 1945. The war in the Pacific ended on September 2, 1945, known as Victory over Japan (V-J) Day, when Japan formally surrendered aboard the USS Missouri battleship in Tokyo Bay. Japan's surrender followed the United States dropping atomic bombs on the Japanese cities of Hiroshima (August 6, 1945) and Nagasaki (August 9, 1945). World War II was the deadliest conflict in human history, resulting in an estimated 70-85 million deaths including military personnel and civilians."
            ],
            "gold_answer": "World War II ended in 1945 — in Europe on May 8 (V-E Day) and in the Pacific on September 2 (V-J Day)."
        },
        {
            "question": "Who was the first person to walk on the Moon?",
            "context": [
                "Neil Armstrong was the first person to walk on the Moon. He set foot on the lunar surface on July 20, 1969, during NASA's Apollo 11 mission. Armstrong stepped onto the Moon at 02:56 UTC and famously said: 'That's one small step for [a] man, one giant leap for mankind.' Edwin 'Buzz' Aldrin joined Armstrong on the Moon's surface about 20 minutes later, becoming the second person to walk on the Moon. The third crew member, Michael Collins, remained in lunar orbit in the command module Columbia. Apollo 11 landed in the Sea of Tranquility. The mission fulfilled President John F. Kennedy's 1961 goal of landing humans on the Moon and returning them safely to Earth before the end of the decade."
            ],
            "gold_answer": "Neil Armstrong was the first person to walk on the Moon, on July 20, 1969, during the Apollo 11 mission."
        },
        {
            "question": "What is the speed of light?",
            "context": [
                "The speed of light in a vacuum is exactly 299,792,458 meters per second (approximately 3 × 10^8 m/s), or about 186,282 miles per second. This is commonly denoted by the letter 'c' in physics. The speed of light is considered a fundamental physical constant and represents the maximum speed at which all conventional matter, energy, and information can travel through space. According to Einstein's special theory of relativity, the laws of physics are the same for all non-accelerating observers, and the speed of light in a vacuum is the same for all observers regardless of their motion or the motion of the light source. Light takes about 8 minutes and 20 seconds to travel from the Sun to Earth."
            ],
            "gold_answer": "The speed of light in a vacuum is 299,792,458 meters per second (approximately 3 × 10^8 m/s)."
        },
        {
            "question": "What is the theory of evolution?",
            "context": [
                "The theory of evolution by natural selection was proposed by Charles Darwin and Alfred Russel Wallace and presented in Darwin's landmark 1859 book 'On the Origin of Species.' The theory states that all species of organisms have descended over time from common ancestors through the process of natural selection — a mechanism by which individuals with heritable traits better suited to their environment tend to survive and reproduce more successfully, passing those traits to offspring. Over many generations, this leads to gradual changes in populations and the emergence of new species. Evolution is supported by overwhelming evidence from fossil records, comparative anatomy, molecular biology, genetics, and direct observation. Modern evolutionary theory incorporates genetics and molecular biology as the Neo-Darwinian synthesis."
            ],
            "gold_answer": "The theory of evolution by natural selection, proposed by Charles Darwin, explains that species change over generations as individuals with advantageous traits survive and reproduce more successfully."
        },
        {
            "question": "What is the human genome?",
            "context": [
                "The human genome is the complete set of genetic information (DNA) in a human cell, consisting of approximately 3.2 billion base pairs of DNA organized into 23 pairs of chromosomes (46 total) found in the cell nucleus, plus mitochondrial DNA. The human genome contains approximately 20,000-25,000 protein-coding genes, though genes represent only about 1-2% of the total DNA sequence. The Human Genome Project, an international scientific research project, completed sequencing the human genome in April 2003. Understanding the human genome is fundamental to medicine, enabling identification of genetic diseases, development of personalized treatments, and understanding human evolution and biology."
            ],
            "gold_answer": "The human genome is the complete set of DNA in a human cell, consisting of approximately 3.2 billion base pairs organized into 23 pairs of chromosomes, containing around 20,000-25,000 genes."
        },
        {
            "question": "How does the internet work?",
            "context": [
                "The internet is a global network of interconnected computers that communicate using standardized protocols. At its core, data is broken into small packets and transmitted across networks using the Internet Protocol (IP) and Transmission Control Protocol (TCP). Each device on the internet has a unique IP address. When you request a webpage, your request travels through routers — specialized devices that direct data packets to their destination — across fiber optic cables, satellite links, and wireless connections. The Domain Name System (DNS) translates human-readable web addresses (like www.example.com) into IP addresses. The World Wide Web (WWW) is an information system built on top of the internet that uses HTTP/HTTPS protocols. The internet originated from ARPANET, a U.S. Department of Defense project in the late 1960s."
            ],
            "gold_answer": "The internet works by breaking data into packets transmitted across interconnected networks using TCP/IP protocols, with routers directing packets to their destinations."
        },
        {
            "question": "What is artificial intelligence?",
            "context": [
                "Artificial Intelligence (AI) is the simulation of human intelligence processes by computer systems. AI encompasses a range of techniques enabling machines to perform tasks that typically require human intelligence, such as understanding natural language, recognizing patterns, solving problems, and making decisions. Key branches of AI include machine learning (systems that learn from data), deep learning (neural networks with multiple layers), natural language processing (understanding and generating human language), computer vision (interpreting visual information), and robotics. Modern AI systems like large language models (LLMs) are trained on vast datasets and can generate text, code, images, and perform complex reasoning tasks. AI applications range from recommendation systems and virtual assistants to autonomous vehicles and medical diagnosis."
            ],
            "gold_answer": "Artificial intelligence (AI) is the simulation of human intelligence by computer systems, enabling machines to learn from data, recognize patterns, understand language, and make decisions."
        },
        {
            "question": "What causes earthquakes?",
            "context": [
                "Earthquakes are caused by the sudden release of energy in Earth's crust, most commonly due to the movement of tectonic plates. Earth's outer shell (lithosphere) is divided into large pieces called tectonic plates that constantly move slowly — a few centimeters per year. At plate boundaries, plates interact by colliding (convergent boundaries), moving apart (divergent boundaries), or sliding past each other (transform boundaries). Stress builds up along fault lines — fractures in Earth's crust — and when the accumulated stress is suddenly released, seismic waves radiate outward, causing ground shaking. The point underground where the earthquake originates is the focus (or hypocenter); directly above it on the surface is the epicenter. The Richter scale and moment magnitude scale measure earthquake intensity."
            ],
            "gold_answer": "Earthquakes are caused by the sudden release of energy along fault lines due to the movement and stress buildup between tectonic plates."
        },
        {
            "question": "What is climate change?",
            "context": [
                "Climate change refers to long-term shifts in global temperatures and weather patterns. While climate change has occurred naturally throughout Earth's history, since the mid-20th century human activities have been the primary driver — particularly the burning of fossil fuels (coal, oil, and natural gas), which releases greenhouse gases like carbon dioxide (CO2) and methane (CH4) into the atmosphere. These gases trap heat from the sun, causing a 'greenhouse effect' that warms the planet. Global average temperatures have risen approximately 1.1°C above pre-industrial levels, leading to consequences including rising sea levels, more frequent extreme weather events, melting polar ice, ocean acidification, and disruptions to ecosystems. The Paris Agreement (2015) aims to limit global warming to 1.5-2°C above pre-industrial levels."
            ],
            "gold_answer": "Climate change refers to long-term shifts in global temperatures primarily driven by human burning of fossil fuels, which releases greenhouse gases that trap heat and warm the planet."
        },
        {
            "question": "Who wrote Romeo and Juliet?",
            "context": [
                "Romeo and Juliet is a tragedy written by William Shakespeare, believed to have been written between 1594 and 1596. It is one of Shakespeare's most famous plays and one of the most performed theatrical works in history. The play tells the story of two young star-crossed lovers, Romeo Montague and Juliet Capulet, whose families are engaged in a bitter feud in Verona, Italy. Their love ultimately leads to both their deaths, which reconciles the feuding families. Shakespeare based the play on an Italian narrative poem by Arthur Brooke (1562) and a prose story by William Painter (1567). The play has been adapted into countless films, operas, ballets, and other theatrical productions."
            ],
            "gold_answer": "Romeo and Juliet was written by William Shakespeare, believed to have been composed between 1594 and 1596."
        },
        {
            "question": "Who painted the Mona Lisa?",
            "context": [
                "The Mona Lisa is a famous oil painting created by Italian Renaissance artist Leonardo da Vinci. It was painted between approximately 1503 and 1519. The painting depicts a woman believed to be Lisa Gherardini, the wife of Florentine merchant Francesco del Giocondo — hence the Italian name 'La Gioconda.' Leonardo used a technique called sfumato, creating soft, hazy outlines and transitions between colors and tones. The Mona Lisa is housed in the Louvre Museum in Paris, France, where it is displayed behind bulletproof glass. It is considered one of the most valuable and recognized paintings in the world, famous for the subject's mysterious smile and the landscape background. The painting was acquired by King Francis I of France and eventually became property of the French Republic."
            ],
            "gold_answer": "The Mona Lisa was painted by Leonardo da Vinci between approximately 1503 and 1519."
        },
        {
            "question": "What is the Olympic Games?",
            "context": [
                "The Olympic Games are the world's leading international multi-sport event, featuring thousands of athletes from over 200 nations competing in various sports. The modern Olympic Games were founded by French educator Pierre de Coubertin and first held in Athens, Greece in 1896, inspired by the ancient Olympic Games held in Olympia, Greece from 776 BC to 393 AD. The Summer Olympics take place every four years, as do the Winter Olympics (held two years apart from the Summer Games since 1994). The Olympic motto is 'Citius, Altius, Fortius' (Latin for 'Faster, Higher, Stronger'). The Olympic symbols include five interlocking rings representing the five continents of the world. The Games promote international cooperation, peace, and athletic excellence."
            ],
            "gold_answer": "The Olympic Games are an international multi-sport event held every four years, featuring athletes from over 200 nations, founded in modern form in 1896."
        },
        {
            "question": "What is the United Nations?",
            "context": [
                "The United Nations (UN) is an international organization founded in 1945 after World War II to promote international peace, security, and cooperation. It was established by the UN Charter, signed on June 26, 1945, and came into force on October 24, 1945 (now celebrated as United Nations Day). The UN has 193 member states — nearly every country in the world. Its headquarters are in New York City, with major offices in Geneva, Vienna, and Nairobi. The UN system includes six principal organs: the General Assembly, the Security Council, the Secretariat, the International Court of Justice, the Economic and Social Council, and the Trusteeship Council. The UN also oversees specialized agencies including the World Health Organization (WHO), UNESCO, UNICEF, the World Bank, and the International Monetary Fund (IMF)."
            ],
            "gold_answer": "The United Nations is an international organization founded in 1945 to promote peace, security, and international cooperation, with 193 member states headquartered in New York City."
        },
        {
            "question": "What is DNA?",
            "context": [
                "DNA (Deoxyribonucleic acid) is the molecule that carries the genetic instructions for the development, functioning, growth, and reproduction of all known living organisms and many viruses. DNA is a double-stranded molecule consisting of two chains that coil around each other to form a double helix. Each strand is made up of nucleotides — units containing a phosphate group, a deoxyribose sugar, and one of four nitrogenous bases: adenine (A), thymine (T), guanine (G), and cytosine (C). Base pairing rules (A-T, G-C) hold the two strands together. Segments of DNA that encode proteins are called genes. The structure of DNA was discovered by James Watson, Francis Crick, Rosalind Franklin, and Maurice Wilkins in 1953, with the double helix model published by Watson and Crick."
            ],
            "gold_answer": "DNA (Deoxyribonucleic acid) is the molecule carrying genetic instructions for all living organisms, consisting of a double helix made of nucleotide base pairs (A-T and G-C)."
        },
        {
            "question": "What is gravity?",
            "context": [
                "Gravity is one of the four fundamental forces of nature and is the force of attraction between all objects that have mass. Isaac Newton formulated the law of universal gravitation in 1687, which states that every mass attracts every other mass with a force proportional to the product of their masses and inversely proportional to the square of the distance between them (F = Gm1m2/r²). Albert Einstein later described gravity more completely in his General Theory of Relativity (1915) as the curvature of space-time caused by mass and energy — massive objects warp the fabric of space-time, and other objects follow curved paths through that warped space-time. Gravity keeps planets in orbit around the Sun, holds the Moon in orbit around Earth, causes objects to fall when dropped, and is responsible for the formation of stars and galaxies."
            ],
            "gold_answer": "Gravity is the fundamental force of attraction between all objects with mass, described by Newton's law of universal gravitation and Einstein's General Theory of Relativity as the curvature of space-time."
        },
        {
            "question": "What is the population of the world?",
            "context": [
                "The world population reached 8 billion people on November 15, 2022, according to the United Nations. As of 2024, the global population is approximately 8.1-8.2 billion people. The world population has grown exponentially in modern times — it took until 1804 to reach 1 billion, then only 123 years to reach 2 billion (1927), and growth has accelerated since. China and India are the two most populous countries in the world, each with over 1.4 billion people, with India surpassing China as the world's most populous nation in 2023. Global population growth is slowing as birth rates decline in many countries. The UN projects world population could reach approximately 9.7 billion by 2050 and peak at around 10.4 billion in the 2080s."
            ],
            "gold_answer": "The world population is approximately 8.1-8.2 billion people as of 2024, having reached 8 billion on November 15, 2022."
        },

        {
            "question": "What is the solar system?",
            "context": [
                "The solar system consists of the Sun and everything gravitationally bound to it, including eight planets, their moons, dwarf planets, asteroids, comets, and interplanetary dust. The eight planets in order from the Sun are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. The first four (Mercury, Venus, Earth, Mars) are called terrestrial or rocky planets; the outer four (Jupiter, Saturn, Uranus, Neptune) are called gas giants or ice giants. The asteroid belt lies between Mars and Jupiter. The Sun contains over 99.86% of the total mass of the solar system. Pluto, once considered the ninth planet, was reclassified as a dwarf planet in 2006 by the International Astronomical Union. The solar system is located in the Milky Way galaxy, about 26,000 light-years from the galactic center."
            ],
            "gold_answer": "The solar system consists of the Sun and eight planets (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune) plus their moons, asteroid belt, and other bodies held together by the Sun's gravity."
        },
        {
            "question": "What caused World War I?",
            "context": [
                "World War I (1914–1918), also known as the First World War or the Great War, was triggered by a complex web of causes. The immediate trigger was the assassination of Archduke Franz Ferdinand of Austria-Hungary by Gavrilo Princip, a Bosnian-Serb nationalist, in Sarajevo on June 28, 1914. However, deeper underlying causes had been building for decades. These long-term causes are often summarized by the acronym MAIN: Militarism (major European powers had been engaged in an arms race, particularly between Britain and Germany), Alliances (Europe was divided into two major alliance blocs: the Triple Entente of France, Russia, and Britain, and the Triple Alliance of Germany, Austria-Hungary, and Italy), Imperialism (competition for colonies and global influence created tensions among European powers), and Nationalism (strong nationalist movements, especially in the Balkans, destabilized the Austro-Hungarian Empire and stirred ethnic conflicts). After the assassination, Austria-Hungary issued an ultimatum to Serbia; when Serbia's response was deemed unsatisfactory, Austria-Hungary declared war. The interlocking alliance system then pulled one nation after another into the conflict: Germany supported Austria-Hungary, Russia mobilized to support Serbia, France and Britain entered to support Russia and Belgium (whose neutrality Germany violated by invading). The war resulted in approximately 17–20 million deaths and redrew the political map of Europe."
            ],
            "gold_answer": "World War I was caused by the assassination of Archduke Franz Ferdinand in 1914, combined with long-term factors: militarism, rival alliances (Triple Entente vs Triple Alliance), imperial competition, and nationalism — especially in the Balkans."
        },
        {
            "question": "What were the main causes of World War II?",
            "context": [
                "World War II (1939–1945) had multiple interconnected causes. The punishing terms of the Treaty of Versailles (1919), which ended World War I, imposed massive reparations and territorial losses on Germany, creating economic hardship and deep resentment that Adolf Hitler exploited. The Great Depression of the 1930s caused widespread economic devastation and political instability across Europe, fueling the rise of extremist movements including fascism in Italy (under Mussolini) and Nazism in Germany. Hitler's aggressive expansionist foreign policy — rearmament of Germany, annexation of Austria (Anschluss, 1938), occupation of the Sudetenland, and finally invasion of Poland (September 1, 1939) — directly led to the war. Britain and France had pursued a policy of appeasement, culminating in the Munich Agreement (1938), which failed to deter Hitler. In Asia, Japan's imperial expansion into China and Southeast Asia brought it into conflict with Western powers, leading to its attack on Pearl Harbor (December 7, 1941) and the entry of the United States into the war. Ideological conflicts between fascism, communism, and liberal democracy also drove the conflict."
            ],
            "gold_answer": "World War II was caused by the punishing Treaty of Versailles, the Great Depression, Hitler's aggressive expansionism and Nazi ideology, the failure of appeasement, and Japanese imperialism in Asia."
        },
        {
            "question": "What was the French Revolution?",
            "context": [
                "The French Revolution (1789–1799) was a period of radical political and social transformation in France that overthrew the monarchy and established a republic. It began in 1789 with the storming of the Bastille fortress on July 14 — now France's national day — driven by popular anger over food shortages, high taxes, and the absolute power of King Louis XVI. Guided by Enlightenment ideals of liberty, equality, and fraternity ('Liberté, Égalité, Fraternité'), the revolutionaries abolished feudalism and the privileges of the aristocracy and clergy. The Declaration of the Rights of Man and of the Citizen (1789) proclaimed universal rights. The Revolution entered a radical phase known as the Reign of Terror (1793–94) under Maximilien Robespierre, during which thousands were executed by guillotine. Louis XVI was executed in 1793 and Marie Antoinette shortly after. The Revolution ended with Napoleon Bonaparte's coup d'état in 1799, which established the Consulate. The Revolution profoundly influenced democratic and republican movements worldwide."
            ],
            "gold_answer": "The French Revolution (1789–1799) overthrew the French monarchy, abolished feudalism, and established a republic based on Enlightenment ideals of liberty, equality, and fraternity, ending with Napoleon's rise to power."
        },
        {
            "question": "What was the Industrial Revolution?",
            "context": [
                "The Industrial Revolution was a period of major industrialization and innovation that began in Britain around the 1760s and spread throughout Europe and North America during the 18th and 19th centuries. It marked a fundamental shift from agrarian, handicraft economies to manufacturing and industry. Key inventions included the steam engine (improved by James Watt), the spinning jenny and power loom (transforming the textile industry), and the locomotive (enabling mass railway transport). The revolution was fueled by abundant coal and iron resources in Britain, a stable political environment, colonial markets, and investment capital. Social consequences were profound: rapid urbanization, the rise of the working class, poor factory conditions that spurred the labor movement and trade unions, and new social classes. The Industrial Revolution dramatically increased production, raised living standards in the long term, and laid the groundwork for modern capitalism. It also began the large-scale burning of fossil fuels, which is now recognized as the origin of modern climate change."
            ],
            "gold_answer": "The Industrial Revolution (c.1760–1840) was a shift from agrarian to industrial economies that began in Britain, driven by steam power, new machinery, and mass manufacturing, transforming society and laying the foundation for the modern world."
        },
        {
            "question": "Who was Napoleon Bonaparte?",
            "context": [
                "Napoleon Bonaparte (1769–1821) was a French military commander and statesman who rose to prominence during the French Revolution and became Emperor of the French from 1804 to 1814 and again briefly in 1815. Born in Corsica, Napoleon demonstrated exceptional military talent and rapidly rose through the ranks of the French Revolutionary Army, winning decisive victories in Italy and Egypt. In 1799 he seized power in a coup (18 Brumaire) and became First Consul of France, later crowning himself Emperor in 1804. At the height of his power, Napoleon controlled most of continental Europe. He introduced the Napoleonic Code, a comprehensive legal framework that influenced law across Europe and beyond. His Grande Armée was devastated by the disastrous invasion of Russia (1812). After defeat at the Battle of Leipzig (1813) and the Allied invasion of France, Napoleon abdicated and was exiled to Elba. He escaped and ruled for the Hundred Days before his final defeat at the Battle of Waterloo (1815), after which he was exiled to Saint Helena, where he died."
            ],
            "gold_answer": "Napoleon Bonaparte was a French military genius and Emperor (1804–1815) who conquered most of Europe, introduced the Napoleonic Code, but was ultimately defeated and exiled after his catastrophic Russian campaign and defeat at Waterloo."
        },
        {
            "question": "What is democracy?",
            "context": [
                "Democracy is a system of government in which power is vested in the people, who exercise that power either directly or through elected representatives. The word comes from the Greek words 'demos' (people) and 'kratos' (power or rule). Direct democracy, as practiced in ancient Athens, allows citizens to vote directly on laws and policies. Representative democracy, the most common modern form, involves citizens electing representatives who make decisions on their behalf. Key principles of democracy include free and fair elections, rule of law, protection of individual rights and civil liberties, separation of powers (legislative, executive, judicial), freedom of speech and press, and majority rule with minority rights. Modern democracies typically have constitutions defining the structure of government. India is the world's largest democracy; the United States is the oldest continuous constitutional democracy. Around half of the world's countries are considered democracies, though the quality of democratic governance varies considerably."
            ],
            "gold_answer": "Democracy is a system of government where power is held by the people, exercised directly or through elected representatives, with key principles including free elections, rule of law, separation of powers, and protection of individual rights."
        }
    ]
}


# ---------------------------------------------------
# HF SUPPORT
# ---------------------------------------------------

try:
    from datasets import load_dataset as hf_load_dataset
    HF_AVAILABLE = True

except ImportError:
    HF_AVAILABLE = False


# ---------------------------------------------------
# HUGGINGFACE LOADER
# ---------------------------------------------------

def load_huggingface_dataset(
    domain: str,
    max_samples: Optional[int] = None
) -> List[Dict]:

    if not HF_AVAILABLE:
        return []

    try:

        # =====================================
        # MEDICAL
        # =====================================

        if domain == "medical":

            ds = hf_load_dataset(
                "qiaojin/PubMedQA",
                "pqa_labeled",
                split="train"
            )

            if max_samples is not None:
                ds = ds.select(
                    range(
                        min(
                            max_samples,
                            len(ds)
                        )
                    )
                )

            results = []

            for item in ds:

                contexts = item.get(
                    "context",
                    {}
                ).get(
                    "contexts",
                    []
                )

                combined_context = " ".join(
                    str(c)
                    for c in contexts
                )

                results.append({

                    "question":
                    item.get(
                        "question",
                        ""
                    ),

                    "context": [
                        combined_context
                    ],

                    "gold_answer":
                    item.get(
                        "long_answer",
                        ""
                    )
                })

            return results


        # =====================================
        # FINANCIAL
        # =====================================

        elif domain == "financial":

            ds = hf_load_dataset(
                "ibm/finqa",
                split="train"
            )

            if max_samples is not None:
                ds = ds.select(
                    range(
                        min(
                            max_samples,
                            len(ds)
                        )
                    )
                )

            results = []

            for item in ds:

                pre = " ".join(
                    item.get(
                        "pre_text",
                        []
                    )
                )

                post = " ".join(
                    item.get(
                        "post_text",
                        []
                    )
                )

                results.append({

                    "question":
                    item.get(
                        "question",
                        ""
                    ),

                    "context": [
                        pre + " " + post
                    ],

                    "gold_answer":
                    item.get(
                        "answer",
                        ""
                    )
                })

            return results


        
             # =====================================
        # LEGAL
        # =====================================

        elif domain == "legal":

            ds = hf_load_dataset(
                "lex_glue",
                "ecthr_a",
                split="train"
            )

            if max_samples is not None:

                ds = ds.select(
                    range(
                        min(
                            max_samples,
                            len(ds)
                        )
                    )
                )

            results = []

            for item in ds:

                text = " ".join(
                    item.get(
                        "text",
                        []
                    )
                )

                # Strip leading paragraph number/spaces (e.g. "9. ") to get actual sentence
                import re as _re
                clean_text = _re.sub(r'^\s*\d+\.\s*', '', text)
                
                results.append({
                    "question": clean_text.split(".")[0][:150],
                    "context": [text[:2000]],

    "gold_answer":
    str(
        item.get(
            "labels",
            []
        )
    )
                })

            return results
        # =====================================
        # GENERAL
        # =====================================

        elif domain == "general":

            ds = hf_load_dataset(
                "nq_open",
                split="train"
            )

            if max_samples is not None:
                ds = ds.select(
                    range(
                        min(
                            max_samples,
                            len(ds)
                        )
                    )
                )

            results = []

            for item in ds:

                q = item.get(
                    "question",
                    ""
                )

                ans = (
                    item.get(
                        "answer",
                        [""]
                    )[0]
                    if item.get("answer")
                    else ""
                )

                results.append({

                    "question": q,

                    "context": [
                        q + " " + ans
                    ],

                    "gold_answer": ans
                })

            return results

        return []

    except Exception as e:

        print("\n====================")
        print("HF DATASET ERROR")
        print("====================")
        print(e)
        print("====================\n")

        return []

# ---------------------------------------------------
# PUBLIC API
# ---------------------------------------------------

def get_sample_data(
    domain: str,
    max_samples: Optional[int] = None
) -> List[Dict]:

    domain = domain.lower()

    hf_data = load_huggingface_dataset(
        domain,
        max_samples=max_samples
    )

    if hf_data:

        print(
            f"[INFO] Loaded {len(hf_data)} samples for {domain}"
        )

        return hf_data

    print(
        f"[WARN] Using fallback sample data"
    )

    return SAMPLE_DATA.get(
        domain,
        []
    )


def get_all_domains():

    return [
        "medical",
        "financial",
        "legal",
        "general"
    ]


# ---------------------------------------------------
# DATASET INFO
# ---------------------------------------------------

def get_dataset_info(
    domain: Optional[str] = None
) -> Union[Dict, List[Dict]]:

    datasets = [

        {
            "id": "medical",
            "name": "Medical",
            "icon": "🏥"
        },

        {
            "id": "financial",
            "name": "Financial",
            "icon": "💰"
        },

        {
            "id": "legal",
            "name": "Legal",
            "icon": "⚖️"
        },

        {
            "id": "general",
            "name": "General",
            "icon": "🌐"
        }
    ]

    if domain:

        for ds in datasets:

            if ds["id"] == domain:
                return ds

    return datasets