import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { api } from "../api.js";
import ErrorState from "../components/ErrorState.jsx";
import LoadingState from "../components/LoadingState.jsx";

export default function AnalysisPage() {
  const [state, setState] = useState({
    loading: true,
    lengthData: null,
    fitData: null,
    colorData: null,
    materialData: null,
    error: null
  });

  useEffect(() => {
    Promise.all([
      api.getLengthAnalysis(),
      api.getFitAnalysis(),
      api.getColorAnalysis(),
      api.getMaterialAnalysis()
    ])
      .then(([lengthData, fitData, colorData, materialData]) =>
        setState({ loading: false, lengthData, fitData, colorData, materialData, error: null })
      )
      .catch((error) => setState({ loading: false, lengthData: null, fitData: null, colorData: null, materialData: null, error }));
  }, []);

  if (state.loading) return <LoadingState />;
  if (state.error) return <ErrorState message={state.error.message} />;

  const brandLengthData = Object.entries(state.lengthData.brand_avg_lengths).map(([brand, length]) => ({
    brand,
    length: Math.round(length * 10) / 10
  }));

  const materialData = Object.entries(state.materialData.material_ratings).map(([material, rating]) => ({
    material,
    rating: Math.round(rating * 10) / 10
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Deep Analysis</p>
          <h1>심층 시장 분석</h1>
        </div>
      </header>

      <section className="content-band">
        <h2>브랜드별 평균 기장</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={brandLengthData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="brand" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="length" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section className="content-band">
        <h2>소재별 평균 평점</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={materialData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ material, rating }) => `${material}: ${rating}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="rating"
            >
              {materialData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </section>

      <section className="content-band">
        <h2>기장 관련 키워드</h2>
        <ul>
          {Object.entries(state.lengthData.length_keywords).map(([kw, count]) => (
            <li key={kw}>{kw}: {count}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}