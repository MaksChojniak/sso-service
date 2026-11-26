<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest } from '@/shared/api/client'

const router = useRouter()
const mobileNavigationOpen = ref(false)

interface Stats {
  total_clients: number
  active_clients: number
  total_users: number
  active_tokens: number
}

interface ClientApp {
  client_id: string
  name: string
  service_url: string
  redirect_uris: string[]
  is_active: boolean
  has_signing_key: boolean
  created_at: string
}

interface DatabaseModelSummary {
  key: string
  label: string
  count: number
}

interface DatabaseColumn {
  key: string
  label: string
}

const activeSection = ref<'overview' | 'database'>('overview')

const stats = ref<Stats>({
  total_clients: 0,
  active_clients: 0,
  total_users: 0,
  active_tokens: 0,
})

const clients = ref<ClientApp[]>([])
const isLoading = ref(true)
const newClientModalOpen = ref(false)
const newClientName = ref('')
const newClientServiceUrl = ref('')
const newClientRedirectUri = ref('')
const createError = ref('')
const generatedSecret = ref('')

const databaseModels = ref<DatabaseModelSummary[]>([])
const selectedModelKey = ref('')
const selectedModelLabel = ref('')
const tableColumns = ref<DatabaseColumn[]>([])
const tableRows = ref<Record<string, unknown>[]>([])
const tableTotalCount = ref(0)
const isTableLoading = ref(false)
const tableError = ref('')
const tableSearch = ref('')

const filteredRows = computed(() => {
  const query = tableSearch.value.trim().toLowerCase()
  if (!query) return tableRows.value
  return tableRows.value.filter((row) =>
    Object.values(row).some((val) => String(val ?? '').toLowerCase().includes(query)),
  )
})

function handleAuthFailure(status: number) {
  if (status === 401 || status === 403) {
    void router.replace('/not-allowed')
    return true
  }
  return false
}

async function fetchDashboard() {
  isLoading.value = true
  const { data, status } = await apiRequest('/api/v1/admin/clients/stats/overview')
  if (handleAuthFailure(status)) return
  if (data?.stats) {
    stats.value = data.stats
    clients.value = data.recent_clients || []
  }
  isLoading.value = false
}

async function fetchDatabaseModels() {
  const { data, status } = await apiRequest('/api/v1/admin/database/models')
  if (handleAuthFailure(status)) return
  if (Array.isArray(data?.models)) {
    databaseModels.value = data.models
  }
}

async function fetchDatabaseTable(modelKey: string) {
  isTableLoading.value = true
  tableError.value = ''
  const { data, error, status } = await apiRequest(`/api/v1/admin/database/models/${encodeURIComponent(modelKey)}`)
  if (handleAuthFailure(status)) return
  if (error) {
    tableError.value = error
    tableColumns.value = []
    tableRows.value = []
    tableTotalCount.value = 0
  } else if (data) {
    selectedModelLabel.value = data.model?.label || modelKey
    tableColumns.value = data.columns || []
    tableRows.value = data.rows || []
    tableTotalCount.value = data.total_count ?? 0
  }
  isTableLoading.value = false
}

function selectOverview() {
  activeSection.value = 'overview'
  mobileNavigationOpen.value = false
}

function selectDatabaseModel(modelKey: string) {
  activeSection.value = 'database'
  selectedModelKey.value = modelKey
  tableSearch.value = ''
  mobileNavigationOpen.value = false
  void fetchDatabaseTable(modelKey)
}

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined || value === '') return '—'
  if (typeof value === 'boolean') return value ? 'Yes' : 'No'
  return String(value)
}

async function handleCreateClient() {
  createError.value = ''
  generatedSecret.value = ''

  const redirectUris = newClientRedirectUri.value
    .split('\n')
    .map(u => u.trim())
    .filter(Boolean)

  const { data, error, status } = await apiRequest('/api/v1/admin/clients/', {
    method: 'POST',
    body: JSON.stringify({
      name: newClientName.value,
      service_url: newClientServiceUrl.value,
      redirect_uris: redirectUris,
    }),
  })
  if (handleAuthFailure(status)) return

  if (error) {
    createError.value = error
    return
  }

  if (data?.client) {
    generatedSecret.value = data.client.client_secret || ''
    newClientName.value = ''
    newClientServiceUrl.value = ''
    newClientRedirectUri.value = ''
    void fetchDashboard()
    void fetchDatabaseModels()
  }
}

async function handleSignOut() {
  await apiRequest('/api/v1/auth/logout', { method: 'POST' })
  void router.push('/admin/login')
}

onMounted(() => {
  void fetchDashboard()
  void fetchDatabaseModels()
})
</script>

<template>
  <div class="admin-shell">
    <aside class="sidebar" aria-label="Admin navigation">
      <RouterLink class="brand" to="/admin" aria-label="mk.dev admin home">
        <span class="brand-mark" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </span>
        <span>mk.dev <span class="brand-suffix">admin</span></span>
      </RouterLink>

      <button
        class="mobile-nav-toggle"
        type="button"
        aria-controls="admin-navigation"
        :aria-expanded="mobileNavigationOpen"
        :aria-label="mobileNavigationOpen ? 'Close navigation' : 'Open navigation'"
        @click="mobileNavigationOpen = !mobileNavigationOpen"
      >
        <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="M3 5h14M3 10h14M3 15h14" />
        </svg>
      </button>

      <div
        id="admin-navigation"
        class="sidebar-content"
        :class="{ 'is-open': mobileNavigationOpen }"
        @keydown.esc="mobileNavigationOpen = false"
      >
        <div class="mobile-navigation-header">
          <span>Navigation</span>
          <button
            class="mobile-nav-close"
            type="button"
            aria-label="Close navigation"
            @click="mobileNavigationOpen = false"
          >
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <path d="m5 5 10 10M15 5 5 15" />
            </svg>
          </button>
        </div>

        <div class="admin-profile">
          <span class="avatar" aria-hidden="true">A</span>
          <span class="profile-copy">
            <span class="profile-name">Administrator</span>
            <span class="profile-role">Admin account</span>
          </span>
        </div>

        <div class="sidebar-section-label">WORKSPACE</div>
        <nav class="navigation" aria-label="Workspace navigation">
          <button
            class="nav-link nav-btn"
            type="button"
            :aria-current="activeSection === 'overview' ? 'page' : undefined"
            @click="selectOverview"
          >
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <rect x="3" y="3" width="5" height="5" rx="1" />
              <rect x="12" y="3" width="5" height="5" rx="1" />
              <rect x="3" y="12" width="5" height="5" rx="1" />
              <rect x="12" y="12" width="5" height="5" rx="1" />
            </svg>
            <span>Overview</span>
          </button>
        </nav>

        <div class="sidebar-section-label sidebar-section-label--spaced">DATABASE</div>
        <nav class="navigation" aria-label="Database tables navigation">
          <button
            v-for="model in databaseModels"
            :key="model.key"
            class="nav-link nav-btn"
            type="button"
            :aria-current="activeSection === 'database' && selectedModelKey === model.key ? 'page' : undefined"
            @click="selectDatabaseModel(model.key)"
          >
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <ellipse cx="10" cy="5" rx="6" ry="2.2" />
              <path d="M4 5v5c0 1.2 2.7 2.2 6 2.2s6-1 6-2.2V5" />
              <path d="M4 10v5c0 1.2 2.7 2.2 6 2.2s6-1 6-2.2v-5" />
            </svg>
            <span class="nav-label">{{ model.label }}</span>
            <span class="nav-count">{{ model.count }}</span>
          </button>
        </nav>

        <div class="sidebar-bottom">
          <button class="sign-out" type="button" @click="handleSignOut">
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <path d="M8 4H4v12h4M11 6l4 4-4 4m4-4H7" />
            </svg>
            <span>Sign out</span>
          </button>
        </div>
      </div>
    </aside>

    <main class="workspace">
      <header class="workspace-header">
        <div class="header-titles">
          <p v-if="activeSection === 'overview'" class="breadcrumb">Workspace <span>/</span> Overview</p>
          <p v-else class="breadcrumb">Database <span>/</span> {{ selectedModelLabel || selectedModelKey }}</p>
          <h1>{{ activeSection === 'overview' ? 'Overview' : (selectedModelLabel || selectedModelKey) }}</h1>
        </div>
        <button
          v-if="activeSection === 'overview'"
          class="primary-btn"
          type="button"
          @click="newClientModalOpen = true"
        >
          + Add Client Application
        </button>
        <button
          v-else
          class="secondary-btn"
          type="button"
          @click="fetchDatabaseTable(selectedModelKey); fetchDatabaseModels()"
        >
          Refresh Table
        </button>
      </header>

      <section v-if="activeSection === 'overview'" class="workspace-content" aria-label="Workspace content">
        <!-- Stats cards -->
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-label">Active Clients</span>
            <span class="stat-value">{{ stats.active_clients }} / {{ stats.total_clients }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Registered Users</span>
            <span class="stat-value">{{ stats.total_users }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Active Tokens</span>
            <span class="stat-value">{{ stats.active_tokens }}</span>
          </div>
        </div>

        <!-- Clients table -->
        <div class="content-card">
          <div class="card-header">
            <h2>Registered Client Applications</h2>
            <button class="refresh-btn" type="button" @click="fetchDashboard">Refresh</button>
          </div>

          <div v-if="isLoading" class="state-msg">Loading applications...</div>
          <div v-else-if="clients.length === 0" class="state-msg">
            No client applications registered yet. Click "+ Add Client Application" to register one.
          </div>
          <table v-else class="clients-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Client ID</th>
                <th>Service URL</th>
                <th>Keys</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in clients" :key="c.client_id">
                <td class="font-bold">{{ c.name }}</td>
                <td><code class="client-id-code">{{ c.client_id }}</code></td>
                <td><a :href="c.service_url" target="_blank" rel="noreferrer" class="link">{{ c.service_url }}</a></td>
                <td>
                  <span v-if="c.has_signing_key" class="badge badge-success">RSA 2048</span>
                  <span v-else class="badge badge-warning">No Key</span>
                </td>
                <td>
                  <span v-if="c.is_active" class="status-dot dot-active">Active</span>
                  <span v-else class="status-dot dot-inactive">Inactive</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Add Client Modal -->
        <div v-if="newClientModalOpen" class="modal-backdrop">
          <div class="modal-card">
            <div class="modal-header">
              <h3>Register New Client Application</h3>
              <button class="close-btn" type="button" @click="newClientModalOpen = false; generatedSecret = ''">✕</button>
            </div>

            <div v-if="generatedSecret" class="secret-alert">
              <p class="font-bold">⚠️ Copy this Client Secret immediately:</p>
              <code class="secret-box">{{ generatedSecret }}</code>
              <p class="secret-hint">It will NEVER be shown again!</p>
              <button class="primary-btn mt-4" type="button" @click="newClientModalOpen = false; generatedSecret = ''">Done</button>
            </div>

            <form v-else class="modal-form" @submit.prevent="handleCreateClient">
              <div v-if="createError" class="error-banner">{{ createError }}</div>

              <label class="modal-field">
                <span>Application Name</span>
                <input v-model="newClientName" placeholder="e.g. My Dashboard" required />
              </label>

              <label class="modal-field">
                <span>Service URL</span>
                <input v-model="newClientServiceUrl" type="url" placeholder="https://app.example.com" required />
              </label>

              <label class="modal-field">
                <span>Redirect URIs (one per line)</span>
                <textarea v-model="newClientRedirectUri" rows="3" placeholder="https://app.example.com/oidc/callback" required></textarea>
              </label>

              <div class="modal-actions">
                <button class="secondary-btn" type="button" @click="newClientModalOpen = false">Cancel</button>
                <button class="primary-btn" type="submit">Create & Generate Keys</button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <section v-else class="workspace-content" aria-label="Database table preview">
        <div class="content-card">
          <div class="card-header card-header--wrap">
            <div class="table-title-group">
              <h2>{{ selectedModelLabel || selectedModelKey }}</h2>
              <span class="row-count-pill">{{ tableTotalCount }} rows</span>
            </div>
            <div class="table-toolbar">
              <input
                v-model="tableSearch"
                class="table-search-input"
                type="search"
                placeholder="Filter loaded rows..."
                aria-label="Filter table rows"
              />
            </div>
          </div>

          <div v-if="isTableLoading" class="state-msg">Loading table data...</div>
          <div v-else-if="tableError" class="state-msg error-text">{{ tableError }}</div>
          <div v-else-if="filteredRows.length === 0" class="state-msg">
            No records found in {{ selectedModelLabel || selectedModelKey }}.
          </div>
          <div v-else class="table-scroll">
            <table class="clients-table">
              <thead>
                <tr>
                  <th v-for="col in tableColumns" :key="col.key">{{ col.label }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, rowIdx) in filteredRows" :key="String(row.id ?? rowIdx)">
                  <td v-for="col in tableColumns" :key="col.key">
                    <span
                      v-if="typeof row[col.key] === 'boolean'"
                      class="badge"
                      :class="row[col.key] ? 'badge-success' : 'badge-warning'"
                    >
                      {{ row[col.key] ? 'True' : 'False' }}
                    </span>
                    <code v-else-if="col.key === 'id' || col.key === 'client_id' || col.key === 'code' || col.key === 'token'" class="client-id-code">
                      {{ formatCellValue(row[col.key]) }}
                    </code>
                    <span v-else class="cell-value">{{ formatCellValue(row[col.key]) }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.admin-shell {
  display: flex;
  min-height: 100vh;
  background: #f7f8fb;
  color: var(--color-ink);
}

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 1;
  display: flex;
  width: 248px;
  flex-direction: column;
  padding: 24px 16px 16px;
  border-right: 1px solid #e9ebf2;
  background: #fff;
}

.brand {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  gap: 10px;
  margin: 1px 0 22px 8px;
  color: var(--color-ink);
  font-size: 18px;
  font-weight: 750;
  letter-spacing: -0.5px;
  text-decoration: none;
}

.brand-mark {
  display: grid;
  width: 20px;
  height: 20px;
  grid-template-columns: repeat(2, 1fr);
  gap: 2px;
}

.brand-mark span {
  background: var(--color-primary);
}

.brand-mark span:nth-child(2),
.brand-mark span:nth-child(3) {
  opacity: 0.68;
}

.brand-suffix {
  color: var(--color-muted);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0;
}

.sidebar-section-label {
  margin: 0 10px 10px;
  color: #9aa3b4;
  font-size: 9px;
  font-weight: 750;
  letter-spacing: 1.15px;
}

.sidebar-section-label--spaced {
  margin-top: 22px;
}

.navigation {
  display: grid;
  gap: 4px;
}

.nav-btn {
  width: 100%;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.nav-label {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.nav-count {
  padding: 2px 7px;
  border-radius: 10px;
  background: #f0f2f7;
  color: #6b768c;
  font-size: 10px;
  font-weight: 650;
}

.nav-link[aria-current='page'] .nav-count {
  background: #e0e3ff;
  color: var(--color-primary-dark);
}

.sidebar-content {
  display: contents;
}

.mobile-nav-toggle,
.mobile-navigation-header {
  display: none;
}

.nav-link,
.sign-out {
  display: flex;
  min-height: 42px;
  align-items: center;
  gap: 12px;
  padding: 0 11px;
  border-radius: 6px;
  color: #59657b;
  font-size: 12px;
  font-weight: 550;
  text-decoration: none;
  transition:
    background 150ms ease,
    color 150ms ease;
}

.nav-link[aria-current='page'] {
  background: #f0f1ff;
  color: var(--color-primary-dark);
  font-weight: 650;
}

.nav-link svg,
.sign-out svg {
  width: 17px;
  height: 17px;
  flex: 0 0 auto;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.5;
}

.sidebar-bottom {
  display: grid;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #eceef4;
}

.admin-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 28px;
  padding: 14px 8px;
  border-top: 1px solid #eceef4;
}

.avatar {
  display: grid;
  width: 34px;
  height: 34px;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 50%;
  background: #eeefff;
  color: var(--color-primary-dark);
  font-size: 12px;
  font-weight: 700;
}

.profile-copy {
  display: grid;
  gap: 3px;
}

.profile-name {
  color: #303b50;
  font-size: 11px;
  font-weight: 650;
}

.profile-role {
  color: #8993a5;
  font-size: 10px;
}

.sign-out {
  min-height: 38px;
}

.nav-link:hover,
.sign-out:hover {
  background: #f5f6fa;
  color: var(--color-ink);
}

.workspace {
  display: flex;
  min-width: 0;
  min-height: 100vh;
  flex: 1;
  flex-direction: column;
  margin-left: 248px;
}

.workspace-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 120px;
  padding: 28px 36px 22px;
  border-bottom: 1px solid #e9ebf2;
  background: #fff;
}

.primary-btn {
  padding: 10px 18px;
  border: 0;
  border-radius: 6px;
  background: var(--color-primary);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 150ms ease;
}

.primary-btn:hover {
  opacity: 0.9;
}

.secondary-btn {
  padding: 10px 18px;
  border: 1px solid #dfe3ed;
  border-radius: 6px;
  background: #fff;
  color: #59657b;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  padding: 20px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #e9ebf2;
  display: grid;
  gap: 6px;
}

.stat-label {
  color: #8993a5;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.stat-value {
  color: var(--color-ink);
  font-size: 24px;
  font-weight: 700;
}

.content-card {
  border-radius: 8px;
  background: #fff;
  border: 1px solid #e9ebf2;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e9ebf2;
}

.card-header--wrap {
  flex-wrap: wrap;
  gap: 12px;
}

.table-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.row-count-pill {
  padding: 3px 9px;
  border-radius: 12px;
  background: #f0f1ff;
  color: var(--color-primary-dark);
  font-size: 11px;
  font-weight: 650;
}

.table-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.table-search-input {
  width: 220px;
  max-width: 100%;
  padding: 7px 11px;
  border: 1px solid #dfe3ed;
  border-radius: 6px;
  font-size: 12px;
  color: var(--color-ink);
  outline: none;
}

.table-search-input:focus {
  border-color: var(--color-primary);
}

.table-scroll {
  width: 100%;
  overflow-x: auto;
}

.cell-value {
  display: inline-block;
  max-width: 260px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: bottom;
}

.error-text {
  color: #b91c1c;
}

.card-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 650;
}

.refresh-btn {
  background: transparent;
  border: 1px solid #dfe3ed;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 12px;
  color: #59657b;
  cursor: pointer;
}

.state-msg {
  padding: 32px;
  text-align: center;
  color: #8993a5;
  font-size: 13px;
}

.clients-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}

.clients-table th {
  padding: 12px 24px;
  background: #fafbfe;
  color: #8993a5;
  font-weight: 650;
  font-size: 11px;
  text-transform: uppercase;
  border-bottom: 1px solid #e9ebf2;
}

.clients-table td {
  padding: 14px 24px;
  border-bottom: 1px solid #f0f2f7;
  color: #303b50;
}

.client-id-code {
  font-family: monospace;
  background: #f4f5f9;
  padding: 3px 6px;
  border-radius: 4px;
  font-size: 11px;
}

.link {
  color: var(--color-primary);
  text-decoration: none;
}

.badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

.badge-success {
  background: #ecfdf5;
  color: #059669;
}

.badge-warning {
  background: #fffbeb;
  color: #d97706;
}

.status-dot {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}

.dot-active::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
}

.dot-inactive::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #9ca3af;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.modal-card {
  width: 100%;
  max-width: 480px;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  font-size: 17px;
}

.close-btn {
  background: none;
  border: 0;
  font-size: 16px;
  cursor: pointer;
  color: #8993a5;
}

.modal-form {
  display: grid;
  gap: 16px;
}

.modal-field {
  display: grid;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #36425a;
}

.modal-field input,
.modal-field textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dfe3ed;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
}

.modal-field textarea {
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.secret-alert {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 6px;
  padding: 16px;
  display: grid;
  gap: 8px;
}

.secret-box {
  background: #fff;
  padding: 8px 12px;
  border: 1px solid #fcd34d;
  border-radius: 4px;
  word-break: break-all;
  font-size: 12px;
  color: #b45309;
}

.secret-hint {
  font-size: 11px;
  color: #92400e;
  margin: 0;
}

.mt-4 {
  margin-top: 12px;
}

.error-banner {
  padding: 8px 12px;
  background: #fef2f2;
  border: 1px solid #fee2e2;
  color: #b91c1c;
  font-size: 12px;
  border-radius: 4px;
}

.breadcrumb {
  margin: 0 0 12px;
  color: #8993a5;
  font-size: 11px;
}

.breadcrumb span {
  padding: 0 6px;
  color: #c1c6d1;
}

h1 {
  margin: 0;
  color: var(--color-ink);
  font-size: 23px;
  font-weight: 650;
  letter-spacing: -0.5px;
}

.workspace-content {
  flex: 1;
  padding: 32px 36px;
}

@media (max-width: 700px) {
  .admin-shell {
    flex-direction: column;
  }

  .sidebar {
    position: relative;
    z-index: 1;
    display: flex;
    width: 100%;
    min-height: auto;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 15px 16px;
    border-right: 0;
    border-bottom: 1px solid #e9ebf2;
  }

  .brand {
    min-height: 38px;
    margin: 0 0 0 2px;
  }

  .mobile-nav-toggle {
    display: flex;
    width: 38px;
    height: 38px;
    align-items: center;
    justify-content: center;
    margin-left: auto;
    padding: 0;
    border: 1px solid #e9ebf2;
    border-radius: 6px;
    background: #fff;
    color: #59657b;
    cursor: pointer;
  }

  .mobile-nav-toggle svg {
    width: 17px;
    height: 17px;
    stroke: currentColor;
    stroke-linecap: round;
    stroke-width: 1.5;
  }

  .sidebar-content {
    position: fixed;
    inset: 0;
    z-index: 3;
    display: flex;
    flex-direction: column;
    padding: 20px 20px 16px;
    background: #fff;
    visibility: hidden;
    transform: translateX(100%);
    transition:
      transform 220ms ease,
      visibility 0s linear 220ms;
  }

  .sidebar-content.is-open {
    visibility: visible;
    transform: translateX(0);
    transition: transform 220ms ease;
  }

  .mobile-navigation-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 18px;
    border-bottom: 1px solid #e9ebf2;
    color: var(--color-ink);
    font-size: 16px;
    font-weight: 650;
  }

  .mobile-nav-close {
    display: grid;
    width: 38px;
    height: 38px;
    place-items: center;
    border: 1px solid #e9ebf2;
    border-radius: 6px;
    background: #fff;
    color: #59657b;
    cursor: pointer;
  }

  .mobile-nav-close svg {
    width: 18px;
    height: 18px;
    stroke: currentColor;
    stroke-linecap: round;
    stroke-width: 1.5;
  }

  .admin-profile {
    margin: 0 0 28px;
    padding: 14px 8px;
  }

  .sidebar-section-label {
    display: block;
  }

  .navigation {
    display: grid;
    gap: 4px;
  }

  .nav-link {
    min-height: 38px;
  }

  .sidebar-bottom {
    margin-top: auto;
  }

  .workspace {
    min-height: auto;
    margin-left: 0;
  }

  .workspace-header {
    min-height: 104px;
    padding: 22px 20px;
  }

  .workspace-content {
    min-height: 50vh;
    padding: 20px;
  }
}

@media (max-width: 700px) and (prefers-reduced-motion: reduce) {
  .sidebar-content,
  .sidebar-content.is-open {
    transition: none;
  }
}
</style>
