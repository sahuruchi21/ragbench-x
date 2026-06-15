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