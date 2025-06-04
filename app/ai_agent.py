import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.models import BugReport
from app.log_analyzer import analyze_log_advanced

load_dotenv()
# Debug için API Key’in ilk 5 karakterini yazdıralım
print("🔐 API Key (ilk 5 karakter):", os.getenv("OPENAI_API_KEY")[:5])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_bug_report_from_ai(log_content: str) -> BugReport:
    rule_based_analysis = analyze_log_advanced(log_content)

    prompt = f"""You are an expert QA engineer. Analyze the following technical log and generate a bug report. Respond ONLY with valid JSON matching this format:

{{
  "title": "Short, descriptive title",
  "description": "Detailed description",
  "steps_to_reproduce": "Step-by-step instructions",
  "expected_outcome": "What should happen",
  "actual_outcome": "What actually happened",
  "priority": "Low | Medium | High | Critical",
  "error_type": "Backend | Frontend | API | Network | User Error | Database | Configuration | AI Processing Error"
}}

Context from rule-based analysis:
- Category: {rule_based_analysis.get('category')}
- Reason: {rule_based_analysis.get('reason')}
- Suggestion: {rule_based_analysis.get('suggestion')}

Log content:
```log
{log_content[:2000]}
```"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical bug report generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        print("Response of AI:", content)
        bug_data = json.loads(content)
        return BugReport(**bug_data)

    except Exception as e:
        return BugReport(
            title="AI Analysis Failed",
            description=str(e),
            steps_to_reproduce="N/A",
            expected_outcome="N/A",
            actual_outcome="N/A",
            priority="Medium",
            error_type="AI_PROCESSING_ERROR",
            analysis_method="fallback",
            confidence_score=0.2
        )

