<template>
  <button class="auth-submit-button" type="submit">
    <slot />
  </button>
</template>

<style scoped>
.auth-submit-button {
  width: 100%;
  height: 44px;
  border: 0;
  border-radius: 6px;
  background: var(--color-primary);
  color: #fff;
  cursor: pointer;
  font-size: 13px;
  font-weight: 650;
  transition: background 150ms ease;
}

.auth-submit-button:hover {
  background: var(--color-primary-dark);
}

.auth-submit-button:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}
</style>
