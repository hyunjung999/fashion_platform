export default function LoadingState({ label = "데이터를 불러오는 중입니다" }) {
  return (
    <div className="state-panel">
      <div className="spinner" />
      <span>{label}</span>
    </div>
  );
}
