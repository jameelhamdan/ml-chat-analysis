### LLM based conversation analysis

#### **Approach**
- Analyzed a dataset of leadership conversations to extract insights on topics, themes, and metrics (e.g., feedback score, success score, conversation length).
- Used predefined prompts and OpenAI's language model to identify recurring patterns and label conversations using chainlang library.
- Visualized findings using interactive charts (e.g., histograms, scatter plots, bar charts, pie charts) in a Streamlit dashboard.

#### **Key Decisions**
- **Analysis**
  - Due to the low volume of conversations and their relative low complexity, A simple direct approach of using a single prompt to fetch all metrics for an individual conversation has been used.
- **Data Processing**:
  - Extracted common topics (e.g., "difficult conversations," "team dynamics") and themes (e.g., "communication strategies," "empathy and support") using OpenAI.
  - Computed metrics like feedback score, success score, and conversation length for each conversation.
- **Visualization**:
  - Chose visualizations to highlight key patterns:
    - Histogram for feedback distribution.
    - Scatter plot for success vs. conversation length.
    - Bar chart for topic frequency.
    - Pie chart for theme distribution.

#### **Findings**
1. **Topics**:
   - "Difficult conversations" was the most frequent topic (15 occurrences), followed by "team dynamics" (14 occurrences).
2. **Themes**:
   - Common themes included "communication strategies" (8 occurrences), "empathy and support" (5 occurrences), and "recognition and appreciation" (7 occurrences).
3. **Metrics**:
   (Calculated based on average of several runs of the script)
   - Average feedback score: **0.85/1.0**.
   - Average success rate: **77.1%**.
   - Average conversation length: **97.8 turns**.
4. **Patterns**:
   - Longer conversations tended to have higher success rates.
   - Feedback scores were generally high, with most scores clustered around 0.8–1.0.

#### **Future Improvements**
- Add filters for dynamic exploration (e.g., by topic, theme, or date range).
- Incorporate sentiment analysis for deeper insights.
- Optimize for larger datasets and real-time updates.

This approach provides actionable insights into leadership conversations, helping identify strengths and areas for improvement.

### How to run

1. Install python 3.11
2. Install packages `$ pip install -r requirements`
3. Set environment variable `$ set OPENAI_API_KEY=...` or add a `.env` file with environment variable
4. Run command `streamlit run main.py`

---

[CHALLENGE.md](./CHALLENGE.md)
