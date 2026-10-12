# Profile

Everything the scout knows about me. It retrieves from this file to judge fit
and to ground the notes it drafts, so two rules:

1. **Only true things.** If it isn't here, the scout shouldn't claim it. A
   drafted note that invents experience is worse than no note.
2. **Specific beats impressive.** "Built a retrieval agent and measured its
   failure rate" is more useful to a matcher than "strong AI skills."

Write it once, honestly, in half an hour. Update it as the term goes on.

---

## Looking for

Summer 2027 internship, SWE/AI/ML engineering. US. Open to relocating.
     Interested in: evaluation, agent systems, applied ML.
     Not interested in: pure research roles requiring a PhD.

## Timing

Available June-September 2027. Graduating June 2028.

## Languages and tools

     Python      - fluent, primary language, 3 years
     Java        - coursework only
     numpy/pandas- comfortable
     R           - fluent, projects
     PyTorch     - coursework
     SQL         - basic
     Git         - daily

## Coursework that's actually relevant

<!-- Course name, what it covered, what I built in it. Skip the course code -
     nobody outside the school knows what COSC 74 is.

     Machine Learning and Statistical Data Analysis - regression through neural
       networks; built a three-tier text classifier comparing TF-IDF, embeddings
       and an LLM on cost, calibration and subgroup performance.

     Topics in Adversarial Machine Learning - seminar on attacks and defences;
       presented on LLM jailbreaks; group project reproducing <x>.
-->

## Projects

FitStake                                                              Jan 2026 - Present
Founder & Lead Engineer
● Built a blockchain-based fitness accountability app for friends & family: users stake real money on workout challenges, submit and verify proof via Fitbit/Strava or photo/video; winners split the losers’ pot, and if everyone fails, funds are donated to charity.
● Designed the UX to hide blockchain complexity: users sign up with email & Privy automatically creates a wallet, USDC stablecoin is purchased directly with a credit card, and workout proof is stored permanently on-chain.
● Deployed a smart contract written in Solidity on Base (Ethereum L2) handling escrow & reward distribution; implemented a React Progressive Web App (installable on iOS/Android) & Express.js backend.

Moen Lab, Geisel School of Medicine at Dartmouth - Hanover, NH        June 2025 - Present
Student Research Assistant (Upcoming First Author Paper)
Project 1: Decision support software to match patients to healthcare providers across a network of clinics
● Improved the matching engine to pair patients with subspecialty providers by cancer type, replacing random assignment; tested it via 100+ simulation batches automated with Bash on a remote Linux server; application being deployed as a SaaS for hospitals.
● Implemented R scripts to organize large, anonymized hospital records by clinic, cancer type, and treatment type.
Project 2: Analyzing Provider Networks to Improve Patient Access to an Effective but Underutilized Cancer Treatment (MDT)
● Processed ~800,000 Medicare records in R, applying graph theory methods (undirected network construction, bipartite projection) to map physician connections, then used statistical modeling (logistic & Poisson regression) to test whether MDT (Metastasis Directed Therapy) specialist ties predicted treatment receipt.
● Found that patients were significantly more likely to receive MDT when their physician had a direct specialist connection.

Retrieval-Augmented Generation (RAG) Document Q&A Agent          December 2025 - Present
● Implemented RAG pipeline in Python to ingest text files, chunk it into 100-word overlapping segments, convert chunks into embeddings using all-MiniLM-L6-v2, store the embeddings in FAISS for similarity search against incoming queries.
● At query time, the program retrieves the five most relevant passages from the document & instructs the language model to generate a response solely from the extracted passages, returning “I don't know” for any out-of-scope questions.

AI Tool to Detect & Rewrite Gender-Biased Job Postings           May 2026 - Present
● Trained an AI model (93% accuracy) to flag masculine-coded language, which discourages women from applying; found that 72% of postings in male-dominated fields contained such language, vs. 60% in female-dominated ones, across 10K job postings.
● Used LLMs to rewrite flagged sentences as gender-neutral; then evaluated their performance using my model & a human survey.

VideoGate Technologies - Hyderabad, India                        July 2025 - September 2025
Software Engineering Intern - Video streaming startup for low-bandwidth environments;
● Designed a hyperlocal ad insertion feature with Angular front-end & MySQL database.
● Defined product specifications; wrote targeted prompts to guide AI-assisted code generation, then implemented, tested, and debugged a working prototype: Advertisers specify budget & geo-radius (lat/long); viewers receive up to 3 ad slots per video.
● Implemented geospatial targeting with RedisGeo/Spring Boot to fetch ads within a defined radius & insert during playback.


## Things I have not done

 Genuinely useful, and the section people skip. The scout uses this to name
     gaps honestly instead of glossing over them - which is the whole point of
     the "gap" line in its output.

     - No production deployment experience
     - No TypeScript or frontend work
     - No distributed training
     - No internship yet

## Constraints

 Nothing that I can think of - I'm a US citizen so NO visa constraints.
