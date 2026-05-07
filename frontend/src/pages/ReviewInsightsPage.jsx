import { useEffect, useState } from "react";
import { api } from "../api.js";
import ErrorState from "../components/ErrorState.jsx";
import LoadingState from "../components/LoadingState.jsx";

export default function ReviewInsightsPage() {
  const [state, setState] = useState({ loading: true, data: null, error: null });

  useEffect(() => {
    api.getReviewAnalysis()
      .then((data) => setState({ loading: false, data, error: null }))
      .catch((error) => setState({ loading: false, data: null, error }));
  }, []);

  if (state.loading) return <LoadingState />;
  if (state.error) return <ErrorState message={state.error.message} />;

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Review Insights</p>
          <h1>카테고리별 리뷰 긍부정 분석</h1>
        </div>
        <div className="target-badge">{state.data.target.label} vs 경쟁 상품</div>
      </header>

      <section className="review-comparison">
        <ReviewGroup group={state.data.target} />
        <ReviewGroup group={state.data.competitors} />
      </section>
    </div>
  );
}

function ReviewGroup({ group }) {
  return (
    <section className="content-band review-panel">
      <div className="section-heading">
        <div>
          <h2>{group.label}</h2>
          <p>{group.total_reviews}개 리뷰 · {group.product_ids.length}개 상품 기준</p>
        </div>
      </div>

      <div className="insight-list">
        {group.categories.map((insight) => (
          <article key={insight.category} className="insight-row">
            <div className="insight-title">
              <strong>{insight.category}</strong>
              <span>긍정 {insight.positive_count} · 부정 {insight.negative_count} · 중립 {insight.neutral_count}</span>
            </div>
            <div className="summary-grid">
              <div>
                <span className="summary-label positive">긍정 요약</span>
                <p>{insight.positive_summary}</p>
              </div>
              <div>
                <span className="summary-label negative">부정 요약</span>
                <p>{insight.negative_summary}</p>
              </div>
            </div>
            <div className="keyword-list">
              {insight.keywords.map((keyword) => (
                <span key={keyword}>{keyword}</span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
