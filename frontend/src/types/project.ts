export interface Project {
  id: string;
  organization_id: string;
  name: string;
  slug: string;
  description: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectInput {
  organization_id: string;
  name: string;
  slug: string;
  description?: string;
}

export interface CreateOrganizationInput {
  name: string;
  slug: string;
}
