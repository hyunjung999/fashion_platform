import { useEffect, useState } from "react";
import { api } from "../api.js";
import ErrorState from "../components/ErrorState.jsx";
import LoadingState from "../components/LoadingState.jsx";

export default function ComparisonPage() {
  const [state, setState] = useState({ loading: true, products: [], error: null });

  useEffect(() => {
    api.getSimilarProducts()
      .then((products) => setState({ loading: false, products, error: null }))
      .catch((error) => setState({ loading: false, products: [], error }));
  }, []);

  if (state.loading) return <LoadingState />;
  if (state.error) return <ErrorState message={state.error.message} />;

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Similar Products</p>
          <h1>동일 포지션 상품 비교</h1>
        </div>
        <div className="target-badge">Product A와 같은 사분면</div>
      </header>

      <section className="content-band">
        <div className="section-heading">
          <div>
            <h2>경쟁 상품 테이블</h2>
            <p>Product A와 같은 사분면에 있는 상품을 거리순으로 정렬했습니다.</p>
          </div>
          <span>{state.products.length}개 표시</span>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>브랜드</th>
                <th>가격</th>
                <th>총장</th>
                <th>통</th>
                <th>소재</th>
                <th>평점</th>
                <th>거리</th>
              </tr>
            </thead>
            <tbody>
              {state.products.map((product) => (
                <tr key={product.product_id}>
                  <td>
                    <strong>{product.brand}</strong>
                    <span>{product.product_id}</span>
                  </td>
                  <td>{product.price.toLocaleString()}원</td>
                  <td>{product.length}cm</td>
                  <td>{product.width}cm</td>
                  <td>{product.material}</td>
                  <td>{product.rating.toFixed(1)}</td>
                  <td>{product.distance_from_target.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
