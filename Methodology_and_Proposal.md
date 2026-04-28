# DeepThought: 1000-Company Scale-Up Methodology & QA Architecture

## 1. Top-of-Funnel Sourcing Architecture
To achieve a final yield of 1,000 qualified Federer companies, we must source an initial universe of ~4,000 MSMEs. 
* **Primary Structured Sources:** DSIR R&D Directory (strongest C3/C4 signal), Chemexcil Export Data, PLI Scheme Beneficiary lists.
* **Secondary Unstructured Sources:** ZaubaCorp / MCA Data (filtered by target NIC codes like 20119 for specialty chemicals, and paid-up capital limits to exclude >500Cr entities).
* **Target:** 4,000 domains deduplicated via fuzzy matching.

## 2. Scraper & Processing Architecture
* **Tools:** Python, `Playwright` (for JavaScript-heavy sites), `BeautifulSoup`, and `Scikit-learn`.
* **Process:** The scraper navigates to the Homepage, About Us, and Products pages, concatenating the text up to an 8k token limit. 
* **Pre-Filtering (ML):** We apply a K-Means clustering algorithm on the scraped "Products" text using TF-IDF vectorization. This mathematically isolates specialty manufacturers (e.g., "recombinant", "oligonucleotide", "cryogenic") from commodity traders, stripping out ~40% of the noise before LLM scoring.

## 3. AI Scoring Prompt & Pipeline
* **LLM Integration:** Claude 3.5 Sonnet API via JSON-mode.
* **Prompt Logic:** The LLM is strictly instructed *not* to infer. If a capability is not explicitly written in the scraped text, it scores a 0.
* **Exclusion Logic:** Immediate auto-fail if the text contains: "distributor", "authorized dealer", "subsidiary of", "wholly owned by", or "group company".

## 4. Quality Assurance (QA) Process
* **Programmatic QA:** Any company scoring a perfect "Strong" on C3 (Differentiation) but showing zero C6 (Growth) signals is automatically flagged for manual review, as this often indicates a stale/dormant patent holder rather than an active Federer.
* **Human-in-the-Loop:** 100% of "Borderline" scores (40-59 range) undergo manual website verification. 20% of "Strong Pass" scores are spot-checked to ensure the LLM did not hallucinate manufacturing capabilities for a CRO/testing lab.
