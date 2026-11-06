<script setup lang="ts">
import { ref } from 'vue'

withDefaults(
  defineProps<{
    id: string
    label: string
    name: string
    placeholder: string
    autocomplete: string
    type?: 'email' | 'password'
  }>(),
  {
    type: 'email',
  },
)

const passwordVisible = ref(false)
</script>

<template>
  <label class="auth-field" :for="id">
    <span>{{ label }}</span>
    <span v-if="type === 'password'" class="password-input">
      <input
        :id="id"
        :type="passwordVisible ? 'text' : 'password'"
        :name="name"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        required
      />
      <button
        class="visibility-toggle"
        type="button"
        :aria-label="passwordVisible ? 'Hide password' : 'Show password'"
        @click="passwordVisible = !passwordVisible"
      >
        {{ passwordVisible ? 'Hide' : 'Show' }}
      </button>
    </span>
    <input
      v-else
      :id="id"
      :type="type"
      :name="name"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
      required
    />
  </label>
</template>

<style scoped>
.auth-field {
  display: grid;
  gap: 8px;
  color: #36425a;
  font-size: 12px;
  font-weight: 650;
}

.auth-field input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  border: 1px solid #dfe3ed;
  border-radius: 6px;
  outline: none;
  background: #fff;
  color: var(--color-ink);
  font-size: 13px;
  font-weight: 400;
  transition:
    border-color 150ms ease,
    box-shadow 150ms ease;
}

.auth-field input::placeholder {
  color: #a6adbb;
}

.auth-field input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgb(90 98 232 / 12%);
}

.password-input {
  position: relative;
}

.password-input input {
  padding-right: 60px;
}

.visibility-toggle {
  position: absolute;
  top: 50%;
  right: 12px;
  padding: 4px 0;
  transform: translateY(-50%);
  border: 0;
  background: transparent;
  color: #77839a;
  cursor: pointer;
  font-size: 11px;
  font-weight: 650;
}

.visibility-toggle:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}
</style>
