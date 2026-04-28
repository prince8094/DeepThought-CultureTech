# Methodology & Proposal: 1000 ICP-Qualified Companies in One Month  
## DeepThought Business Analytics Internship Submission  

---

## Part 1: Advanced Sourcing Methods (Beyond Google)

Finding true Federer profiles requires querying structured databases that naturally filter for differentiation (C3) and growth (C6).

---

### 1. DSIR (Department of Scientific & Industrial Research) R&D Directory

**Why it works:**  
DSIR certification requires a company to prove they have a dedicated, functioning R&D lab. This is an immediate, high-fidelity signal for C3 (Differentiated) and C4 (Technical DM).

**Limitations:**  
Misses newer bootstrapped startups; PDF-heavy formatting requires parsing.

---

### 2. Chemexcil & Pharmexcil Export Registries

**Why it works:**  
Companies exporting specialty chemicals or complex APIs to regulated markets (US/EU) must meet stringent quality standards. Presence here strongly correlates with C5 (Tailwinds) and C1 (In-house Manufacturing).

**Limitations:**  
Mixes actual manufacturers with pure merchant traders. Requires cross-referencing NIC codes.

---

### 3. Unsupervised ML on MCA/ZaubaCorp Data (Custom Approach)

**Why it works:**  
Leveraging Python and scikit-learn, bulk NIC code data (e.g., Code 20119 - Manufacturing of other basic chemicals) can be analyzed using K-Means clustering on company product descriptions. This enables scalable identification of “specialty/custom” vs “bulk/commodity” businesses.

**Limitations:**  
Requires clean text data, which MCA filings often lack. Must be enriched with scraped website data.
