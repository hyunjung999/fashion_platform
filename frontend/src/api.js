const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function fetchJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`API 요청 실패: ${response.status}`);
  }
  return response.json();
}

export const api = {
  getMockData: () => fetchJson("/mock-data"),
  getPositioning: (productId = "A") => fetchJson(`/positioning?product_id=${productId}`),
  getSimilarProducts: (productId = "A") => fetchJson(`/similar-products?product_id=${productId}&limit=40`),
  getReviewAnalysis: (productId = "A") => fetchJson(`/review-analysis?product_id=${productId}`),
  getLengthAnalysis: () => fetchJson("/length-analysis"),
  getFitAnalysis: () => fetchJson("/fit-analysis"),
  getColorAnalysis: () => fetchJson("/color-analysis"),
  getMaterialAnalysis: () => fetchJson("/material-analysis"),
};
