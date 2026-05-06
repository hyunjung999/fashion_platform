import { useEffect, useState } from "react";
import { api } from "../api.js";
import ErrorState from "../components/ErrorState.jsx";
import LoadingState from "../components/LoadingState.jsx";
import MetricCard from "../components/MetricCard.jsx";
import PositioningChart from "../components/PositioningChart.jsx";

export default function DashboardPage() {
  const [state, setState] = useState({ loading: true, data: null, mock: null, error: null });

  useEffect(() => {
    Promise.all([api.getPositioning(), api.getMockData()])
      .then(([data, mock]) => setState({ loading: false, data, mock, error: null }))
      .catch((error) => setState({ loading: false, data: null, mock: null, error }));
  }, []);

  if (state.loading) return <LoadingState />;
  if (state.error) return <ErrorState message={state.error.message} />;

  const target = state.data.products.find((product) => product.product_id === "A");

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Positioning Analysis</p>
          <h1>자사 상품 시장 포지셔닝</h1>
        </div>
        <div className="target-badge">Product A 강조 표시</div>
      </header>

      <div className="metric-grid">
        <MetricCard label="상품 수" value={`${state.mock.product_count}개`} subtext="Product A 포함 Mock 데이터" />
        <MetricCard label="리뷰 수" value={`${state.mock.review_count}개`} subtext="상품당 5~20개 생성" />
        <MetricCard label="Product A 평점" value={target.rating.toFixed(1)} subtext={`${target.price.toLocaleString()}원`} />
        <MetricCard label="Product A 사분면" value={target.quadrant} subtext={`총장 ${target.length}cm / 통 ${target.width}cm`} />
      </div>

      <section className="content-band">
        <div className="section-heading">
          <div>
            <h2>4사분면 포지셔닝 맵</h2>
            <p>중앙 분할선은 전체 상품의 총장과 통 중앙값 기준입니다.</p>
          </div>
          <span>Length split {state.data.length_split}cm · Width split {state.data.width_split}cm</span>
        </div>
        <PositioningChart data={state.data} />
      </section>

      <section className="two-column">
        <div className="content-band compact">
          <h2>사분면별 상품 수</h2>
          <div className="count-list">
            {Object.entries(state.data.quadrant_counts).map(([label, count]) => (
              <div key={label}>
                <span>{label}</span>
                <strong>{count}개</strong>
              </div>
            ))}
          </div>
        </div>
        <div className="content-band compact">
          <h2>K-means 클러스터</h2>
          <div className="cluster-grid">
            {state.data.cluster_centers.map((cluster) => (
              <div key={cluster.cluster_id} className="cluster-pill">
                <strong>C{cluster.cluster_id}</strong>
                <span>{cluster.count}개</span>
                <small>{cluster.length}cm / {cluster.width}cm</small>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
