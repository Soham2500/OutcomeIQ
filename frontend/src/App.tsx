import { Navigate, Route, Routes } from "react-router-dom";
import { TOKEN_KEY } from "./api/client";
import { Layout } from "./components/Layout";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { BillingPage } from "./pages/BillingPage";
import { DashboardPage } from "./pages/DashboardPage";
import { DemoGuidePage } from "./pages/DemoGuidePage";
import { LoginPage } from "./pages/LoginPage";
import { PricingPage } from "./pages/PricingPage";
import { ProjectsPage } from "./pages/ProjectsPage";
import { RecommendationsPage } from "./pages/RecommendationsPage";
import { RegisterPage } from "./pages/RegisterPage";
import { WorkflowsPage } from "./pages/WorkflowsPage";
import { ProtectedRoute } from "./routes/ProtectedRoute";

function HomeRedirect() {
  return (
    <Navigate
      replace
      to={localStorage.getItem(TOKEN_KEY) ? "/dashboard" : "/login"}
    />
  );
}

export default function App() {
  return (
    <Routes>
      <Route element={<HomeRedirect />} path="/" />
      <Route element={<LoginPage />} path="/login" />
      <Route element={<RegisterPage />} path="/register" />
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route element={<DashboardPage />} path="/dashboard" />
        <Route element={<ProjectsPage />} path="/projects" />
        <Route element={<WorkflowsPage />} path="/workflows" />
        <Route element={<AnalyticsPage />} path="/analytics" />
        <Route element={<RecommendationsPage />} path="/recommendations" />
        <Route element={<PricingPage />} path="/pricing" />
        <Route element={<BillingPage />} path="/billing" />
        <Route element={<DemoGuidePage />} path="/demo-guide" />
      </Route>
      <Route element={<HomeRedirect />} path="*" />
    </Routes>
  );
}
