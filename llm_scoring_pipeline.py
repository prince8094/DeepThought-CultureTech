import json
import os
import requests
import pandas as pd

# LLM API configuration (can be Claude, Gemini, etc.)
API_URL = "https://api.llm-provider.com/v1/chat/completions"
API_KEY = os.getenv("LLM_API_KEY")


def generate_federer_score(company_text):
    """
    Sends company data to an LLM and gets a structured score
    based on the DeepThought Federer Framework.
    """

    # Keeping prompt strict to avoid hallucinations
    prompt = f"""
    You are a strict B2B analyst. Evaluate the company ONLY based on given text.
    Do not assume anything.

    Criteria:
    C1: Physical manufacturer (not service/CRO/distributor)
    C2: Based in India
    C3: Differentiated product (IP, niche, patents)
    C4: Technical decision maker (PhD, engineer, etc.)
    C5: Industry tailwinds
    C6: Growth signals (hiring, expansion, news)

    Output strictly in JSON:
    {{
        "C1_Score": "Strong|Moderate|Weak|Fail",
        "C3_Score": "Strong|Moderate|Weak",
        "Total_Score": <int>,
        "Verdict": "Pass|Borderline|Fail"
    }}

    Company Text:
    {company_text[:8000]}
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-5-sonnet",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        # Actual API call (kept commented for now)
        # response = requests.post(API_URL, json=payload, headers=headers)
        # return response.json()['choices'][0]['message']['content']

        # Mock response (used for testing pipeline)
        return json.dumps({
            "Verdict": "Pass",
            "Total_Score": 85,
            "C1_Score": "Strong"
        })

    except Exception as e:
        print(f"Error while scoring: {e}")
        return None


def process_batch(input_csv):
    """
    Processes a batch of companies and assigns LLM-based scores.
    """

    df = pd.read_csv(input_csv)
    results = []

    for _, row in df.iterrows():
        # Combine all useful text fields
        combined_text = (
            str(row.get('about_us_scraped', '')) + " " +
            str(row.get('product_description_scraped', ''))
        )

        score_json = generate_federer_score(combined_text)

        if score_json:
            try:
                parsed = json.loads(score_json)

                row['Verdict'] = parsed.get('Verdict')
                row['Total_Score'] = parsed.get('Total_Score')

                results.append(row)

            except json.JSONDecodeError:
                print("Skipping row due to invalid JSON response")

    # Save final output
    output_df = pd.DataFrame(results)
    output_df.to_csv('llm_scored_output.csv', index=False)

    print(f"Done: {len(output_df)} companies scored and saved.")


# Example run
if __name__ == "__main__":
    # process_batch('cleaned_specialty_candidates.csv')
    pass
