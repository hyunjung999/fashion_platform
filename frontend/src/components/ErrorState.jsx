export default function ErrorState({ message }) {
  return (
    <div className="state-panel error">
      <strong>데이터를 불러오지 못했습니다</strong>
      <span>{message}</span>
    </div>
  );
}
