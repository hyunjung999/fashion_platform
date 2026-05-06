export default function MetricCard({ label, value, subtext }) {
  return (
    <section className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {subtext ? <p>{subtext}</p> : null}
    </section>
  );
}
