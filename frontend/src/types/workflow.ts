export type WorkflowStatus = "active" | "inactive" | "archived";

export interface Workflow {
  id: string;
  project_id: string;
  name: string;
  slug: string;
  description: string | null;
  status: WorkflowStatus;
  created_by_user_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateWorkflowInput {
  project_id: string;
  name: string;
  slug: string;
  description?: string;
}

export interface WorkflowConfiguration {
  id: string;
  workflow_id: string;
  name: string;
  version_label: string;
  description: string | null;
  strategy_name: string | null;
  config_json: Record<string, unknown> | null;
  is_active: boolean;
  created_by_user_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateWorkflowConfigurationInput {
  name: string;
  version_label: string;
  description?: string;
  strategy_name?: string;
  config_json?: Record<string, unknown>;
}
