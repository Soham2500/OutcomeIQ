import { Navigate, Route, Routes } from "react-router-dom";
import { TOKEN_KEY } from "./api/client";
import { Layout } from "./components/Layout";
import { DashboardPage } from "./pages/DashboardPage";
import { DemoGuidePage } from "./pages/DemoGuidePage";
import { LoginPage } from "./pages/LoginPage";
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
        <Route element={<RecommendationsPage />} path="/recommendations" />
        <Route element={<DemoGuidePage />} path="/demo-guide" />
      </Route>
      <Route element={<HomeRedirect />} path="*" />
    </Routes>
  );
}
