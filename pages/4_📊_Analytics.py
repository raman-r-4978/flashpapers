"""Analytics and statistics dashboard."""

import streamlit as st

from flashpapers.utils import AnalyticsUtils

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Analytics Dashboard")

# Get instances from session state
storage = st.session_state.storage
analytics = AnalyticsUtils(storage)

# Get analytics data
stats = analytics.get_analytics()
performance = analytics.get_performance_metrics()

# Overview metrics
st.header("📈 Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Papers", stats["total_papers"])

with col2:
    st.metric("Reviewed Papers", stats["reviewed_papers"])
    if stats["total_papers"] > 0:
        percentage = (stats["reviewed_papers"] / stats["total_papers"]) * 100
        st.caption(f"{percentage:.1f}% of collection")

with col3:
    st.metric("Due Today", stats["papers_due_today"])

with col4:
    st.metric("Total Reviews", stats["total_reviews"])

st.markdown("---")

# Performance metrics
st.header("🎯 Performance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Reviews/Paper", performance["average_reviews_per_paper"])

with col2:
    st.metric("Retention Rate", f"{performance['retention_rate']}%")

with col3:
    st.metric("Review Streak", f"{performance['review_streak']} days")

with col4:
    st.metric("Avg Ease Factor", stats["average_ease_factor"])

st.markdown("---")

# Category distribution
if stats["categories_distribution"]:
    st.header("📚 Category Distribution")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Create bar chart data
        import pandas as pd

        cat_df = pd.DataFrame(
            list(stats["categories_distribution"].items()), columns=["Category", "Count"]
        )
        cat_df = cat_df.sort_values("Count", ascending=False)

        st.bar_chart(cat_df.set_index("Category"))

    with col2:
        st.subheader("Details")
        for cat, count in sorted(
            stats["categories_distribution"].items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / stats["total_papers"]) * 100 if stats["total_papers"] > 0 else 0
            st.text(f"{cat}: {count} ({percentage:.1f}%)")

    st.markdown("---")

# Most reviewed paper
if performance["most_reviewed_paper"]:
    st.header("🏆 Most Reviewed Paper")
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"**{performance['most_reviewed_paper']['title']}**")

    with col2:
        st.metric("Reviews", performance["most_reviewed_paper"]["review_count"])

    st.markdown("---")

# Upcoming reviews
st.header("📅 Upcoming Reviews")

upcoming = analytics.get_upcoming_reviews(days=14)

if upcoming:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Next 14 Days")
        for item in upcoming[:10]:
            st.text(f"• {item['paper_title']}")
            st.caption(f"  Due in {item['days_until']} day(s)")

    with col2:
        # Summary by day
        from collections import Counter

        days_count = Counter(item["days_until"] for item in upcoming)
        st.subheader("By Day")
        for day in sorted(days_count.keys())[:7]:
            st.text(f"Day {day}: {days_count[day]} paper(s)")
else:
    st.info("No reviews scheduled in the next 14 days")

st.markdown("---")

# Recent review history
if stats["review_history"]:
    st.header("📜 Recent Review History (Last 30 Days)")

    for review in stats["review_history"][:10]:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.text(f"• {review['paper_title']}")

        with col2:
            st.caption(f"{review['days_ago']} days ago")

st.markdown("---")

# Collection insights
st.header("💡 Insights")

insights = []

# Retention insight
retention = performance["retention_rate"]
if retention < 50:
    insights.append("⚠️ Low retention rate. Consider reviewing more papers regularly.")
elif retention > 80:
    insights.append("🎉 Excellent retention rate! Keep up the good work!")

# Due papers insight
if stats["papers_due_today"] > 10:
    insights.append(f"📚 You have {stats['papers_due_today']} papers due today. Time to review!")
elif stats["papers_due_today"] == 0:
    insights.append("✅ All caught up on reviews!")

# Streak insight
if performance["review_streak"] >= 7:
    insights.append(f"🔥 Great streak! {performance['review_streak']} days in a row!")
elif performance["review_streak"] == 0:
    insights.append("💪 Start a review streak today!")

# Ease factor insight
if stats["average_ease_factor"] < 2.0:
    insights.append("📉 Average ease factor is low. Papers might be too difficult.")
elif stats["average_ease_factor"] > 2.7:
    insights.append("📈 High ease factor! You're mastering your papers!")

if insights:
    for insight in insights:
        st.info(insight)
else:
    st.info("Add more papers and reviews to see personalized insights!")

# Export/Backup section
st.markdown("---")
st.header("💾 Data Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("📦 Create Backup", use_container_width=True):
        backup_path = storage.create_backup()
        st.success(f"✅ Backup created: {backup_path.name}")

with col2:
    # Export to CSV would go here
    st.button("📄 Export to CSV (Coming Soon)", use_container_width=True, disabled=True)
