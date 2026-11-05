<template>
  <div class="admin-shell">
    <aside class="sidebar" aria-label="Admin navigation">
      <RouterLink class="brand" to="/admin" aria-label="mk.dev admin home">
        <span class="brand-mark" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </span>
        <span>mk.dev <span class="brand-suffix">admin</span></span>
      </RouterLink>

      <div class="sidebar-section-label">WORKSPACE</div>
      <nav class="navigation">
        <RouterLink class="nav-link" to="/admin" aria-current="page">
          <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
            <rect x="3" y="3" width="5" height="5" rx="1" />
            <rect x="12" y="3" width="5" height="5" rx="1" />
            <rect x="3" y="12" width="5" height="5" rx="1" />
            <rect x="12" y="12" width="5" height="5" rx="1" />
          </svg>
          <span>Overview</span>
        </RouterLink>
      </nav>

      <div class="sidebar-bottom">
        <div class="admin-profile">
          <span class="avatar" aria-hidden="true">A</span>
          <span class="profile-copy">
            <span class="profile-name">Administrator</span>
            <span class="profile-role">Admin account</span>
          </span>
        </div>
        <RouterLink class="sign-out" to="/admin/login">
          <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
            <path d="M8 4H4v12h4M11 6l4 4-4 4m4-4H7" />
          </svg>
          <span>Sign out</span>
        </RouterLink>
      </div>
    </aside>

    <main class="workspace">
      <header class="workspace-header">
        <div>
          <p class="breadcrumb">Workspace <span>/</span> Overview</p>
          <h1>Overview</h1>
        </div>
      </header>
      <section class="workspace-content" aria-label="Workspace content"></section>
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
  margin: 1px 0 42px 8px;
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

.navigation {
  display: grid;
  gap: 4px;
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
  gap: 9px;
  margin-top: auto;
}

.admin-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 8px;
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
  min-height: 120px;
  padding: 28px 36px 22px;
  border-bottom: 1px solid #e9ebf2;
  background: #fff;
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
    position: static;
    width: 100%;
    min-height: auto;
    padding: 15px 16px 12px;
    border-right: 0;
    border-bottom: 1px solid #e9ebf2;
  }

  .brand {
    margin: 0 0 18px 2px;
  }

  .sidebar-section-label {
    display: none;
  }

  .navigation {
    display: flex;
  }

  .nav-link {
    min-height: 38px;
  }

  .sidebar-bottom {
    position: absolute;
    top: 15px;
    right: 16px;
    display: flex;
    margin: 0;
  }

  .admin-profile {
    padding: 0;
    border: 0;
  }

  .profile-copy {
    display: none;
  }

  .sign-out {
    width: 38px;
    justify-content: center;
    padding: 0;
    font-size: 0;
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
</style>
