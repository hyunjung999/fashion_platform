import { BarChart3, MessageSquareText, Table2, TrendingUp } from "lucide-react";
import { useState } from "react";
import DashboardPage from "./pages/DashboardPage.jsx";
import ComparisonPage from "./pages/ComparisonPage.jsx";
import ReviewInsightsPage from "./pages/ReviewInsightsPage.jsx";
import AnalysisPage from "./pages/AnalysisPage.jsx";

const PAGES = [
  { id: "dashboard", label: "메인 대시보드", icon: BarChart3, component: DashboardPage },
  { id: "comparison", label: "상품 비교", icon: Table2, component: ComparisonPage },
  { id: "reviews", label: "리뷰 인사이트", icon: MessageSquareText, component: ReviewInsightsPage },
  { id: "analysis", label: "심층 분석", icon: TrendingUp, component: AnalysisPage },
];

export default function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const CurrentPage = PAGES.find((page) => page.id === activePage).component;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <span className="brand-mark">A</span>
          <div>
            <strong>Training Pants Lab</strong>
            <p>여성 트레이닝 팬츠 시장 분석</p>
          </div>
        </div>

        <nav className="nav-list" aria-label="대시보드 메뉴">
          {PAGES.map((page) => {
            const Icon = page.icon;
            return (
              <button
                key={page.id}
                className={activePage === page.id ? "nav-button active" : "nav-button"}
                onClick={() => setActivePage(page.id)}
                type="button"
              >
                <Icon size={18} />
                <span>{page.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <main className="main-area">
        <CurrentPage />
      </main>
    </div>
  );
}
