import json
import os.path
import typing
from time import strftime, gmtime
import pandas as pd
import streamlit as st
import plotly.express as px
from tqdm import tqdm
from src import config
from src.services import dataset, ai
from src.services.ai import ConversationResult


class ResponseData(typing.TypedDict):
    data: list[ConversationResult]
    commons: dict[str, dict[str, int]]


@st.cache_data
def analyze_data() -> ResponseData:
    """
    Load dataset and process with conversation service
    """
    data = []
    service = ai.ConversationService()

    def get_iterator():
        return tqdm(dataset.load_dataset(config.DATA_FILE))

    # Analyze conversations and extract common data
    common_topics: dict[str, int] = service.extract_common_topics(get_iterator())
    common_themes: dict[str, int] = service.extract_common_themes(get_iterator())

    # Measure conversations metrics
    for conv in get_iterator():
        # Extract basic conversation metrics
        # Analyze conversation content
        data += [service.label(conv, topics=list(common_topics.keys()), themes=list(common_themes.keys()))]

    # Save result into json file

    response_data = dict(
        data=data,
        commons=dict(
            topics=common_topics,
            themes=common_themes,
        )
    )

    with open(os.path.join(config.OUT_DIR, 'result-{}.json'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())).replace(' ', '-')), 'w', encoding='utf-8') as f:
        f.write(json.dumps(response_data, ensure_ascii=False, indent=4))

    return response_data


def main():
    st.set_page_config(page_title="Conversation Analytics", layout="wide")
    st.title("Leadership Conversation Analysis Dashboard")

    if filename := config.ANALYTICS_FILENAME:
        st.info(f"Loading data from file: {filename}")
        with open(filename, encoding='utf-8') as f:
            response_data = json.load(f)
    else:
        st.info("Analyzing data from scratch...")
        response_data = analyze_data()

    df, commons = pd.DataFrame(response_data['data']), response_data['commons']

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Feedback Score", f"{df['feedback_score'].mean():.2f}/1.0")
    with col2:
        st.metric("Success Rate", f"{df['success_score'].mean() * 100:.1f}%")
    with col3:
        st.metric("Avg Conversation Length", f"{df['length'].mean():.1f} turns")

    # Main Visualizations
    st.header("Conversation Analysis")

    # First row of charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Feedback Distribution")
        fig = px.histogram(
            df,
            x='feedback_score',
            nbins=10,
            labels={'feedback_score': 'User Feedback Score'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Success vs Conversation Length")
        fig = px.scatter(
            df,
            x='length',
            y='success_score',
            color='feedback_score',
            trendline='lowess'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Second row of charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Topic Distribution")
        topic_counts = df['topic'].value_counts().reset_index()
        fig = px.bar(
            topic_counts,
            x='count',
            y='topic',
            orientation='h'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Common Themes")
        themes = df.explode('themes')
        theme_counts = themes['themes'].value_counts().reset_index()
        fig = px.pie(
            theme_counts,
            values='count',
            names='themes'
        )
        st.plotly_chart(fig, use_container_width=True)
