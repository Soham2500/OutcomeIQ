import { Navigate, Route, Routes } from "react-router-dom";
import { TOKEN_KEY } from "./api/client";
import { Layout } from "./components/Layout";
import { AdminBillingPage } from "./pages/AdminBillingPage";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { BillingPage } from "./pages/BillingPage";
import { ContactPage } from "./pages/ContactPage";
import { DashboardPage } from "./pages/DashboardPage";
import { DemoGuidePage } from "./pages/DemoGuidePage";
import { LaunchReadinessPage } from "./pages/LaunchReadinessPage";
import { LoginPage } from "./pages/LoginPage";
import { PricingPage } from "./pages/PricingPage";
import { PrivacyPolicyPage } from "./pages/PrivacyPolicyPage";
import { ProjectsPage } from "./pages/ProjectsPage";
import { RecommendationsPage } from "./pages/RecommendationsPage";
import { RegisterPage } from "./pages/RegisterPage";
import { RefundPolicyPage } from "./pages/RefundPolicyPage";
import { TermsPage } from "./pages/TermsPage";
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
      <Route element={<PrivacyPolicyPage />} path="/privacy" />
      <Route element={<TermsPage />} path="/terms" />
      <Route element={<RefundPolicyPage />} path="/refund-policy" />
      <Route element={<ContactPage />} path="/contact" />
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
        <Route element={<LaunchReadinessPage />} path="/launch-readiness" />
        <Route element={<AdminBillingPage />} path="/admin/billing" />
      </Route>
      <Route element={<HomeRedirect />} path="*" />
    </Routes>
  );
}
