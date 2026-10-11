<script setup lang="ts">
import { computed, ref } from 'vue'

const step = ref(1)
const email = ref('')
const verificationCode = ref('')
const password = ref('')
const confirmPassword = ref('')
const formError = ref('')
const codeInputFocused = ref(false)
const codeDigits = computed(() => Array.from(verificationCode.value.padEnd(8, ' ')))

const stepTitle = computed(() => {
  if (step.value === 1) return 'Enter your email'
  if (step.value === 2) return 'Verify your email'
  return 'Create a new password'
})

function handleSubmit() {
  formError.value = ''

  if (step.value === 1) {
    step.value = 2
    return
  }

  if (step.value === 2) {
    if (!/^[0-9]{8}$/.test(verificationCode.value)) {
      formError.value = 'Enter the 8-digit code from your email.'
      return
    }

    step.value = 3
    return
  }

  if (password.value !== confirmPassword.value) {
    formError.value = 'Your passwords do not match.'
  }
}

function editEmail() {
  step.value = 1
  verificationCode.value = ''
  formError.value = ''
}

function sanitizeVerificationCode(event: Event) {
  const input = event.target

  if (!(input instanceof HTMLInputElement)) return

  verificationCode.value = input.value.replace(/\D/g, '').slice(0, 8)
  input.value = verificationCode.value
}
</script>

<template>
  <form class="auth-form" @submit.prevent="handleSubmit">
    <p class="step-label">STEP {{ step }} OF 3 <span aria-hidden="true">·</span> {{ stepTitle }}</p>

    <template v-if="step === 1">
      <label class="field">
        <span>Email address</span>
        <input
          v-model="email"
          type="email"
          name="email"
          placeholder="you@example.com"
          autocomplete="email"
          required
        />
      </label>
      <button class="primary-button" type="submit">Continue</button>
    </template>

    <template v-else-if="step === 2">
      <p class="step-description">
        Enter the 8-digit verification code sent to <strong>{{ email }}</strong>.
      </p>
      <label class="field">
        <span>Verification code</span>
        <span class="code-input" :class="{ 'is-focused': codeInputFocused }">
          <span
            v-for="(digit, index) in codeDigits"
            :key="index"
            class="code-cell"
            :class="{
              'is-filled': digit !== ' ',
              'is-active': codeInputFocused && index === Math.min(verificationCode.length, 7),
            }"
            aria-hidden="true"
          >{{ digit === ' ' ? '' : digit }}</span>
          <input
            v-model="verificationCode"
            class="code-native-input"
            type="text"
            name="verificationCode"
            inputmode="numeric"
            autocomplete="one-time-code"
            pattern="[0-9]{8}"
            maxlength="8"
            minlength="8"
            aria-label="8-digit verification code"
            aria-describedby="code-hint"
            required
            @input="sanitizeVerificationCode"
            @focus="codeInputFocused = true"
            @blur="codeInputFocused = false"
          />
        </span>
        <span id="code-hint" class="field-hint">The code must contain 8 digits.</span>
      </label>
      <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>
      <div class="actions">
        <button class="secondary-button" type="button" @click="editEmail">Back</button>
        <button class="primary-button" type="submit">Verify code</button>
      </div>
    </template>

    <template v-else>
      <p class="step-description">Choose a new password for your account.</p>
      <label class="field">
        <span>New password</span>
        <input
          v-model="password"
          type="password"
          name="password"
          placeholder="At least 8 characters"
          autocomplete="new-password"
          minlength="8"
          required
        />
      </label>
      <label class="field">
        <span>Confirm new password</span>
        <input
          v-model="confirmPassword"
          type="password"
          name="confirmPassword"
          placeholder="Enter your password again"
          autocomplete="new-password"
          minlength="8"
          required
        />
      </label>
      <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>
      <div class="actions">
        <button class="secondary-button" type="button" @click="step = 2">Back</button>
        <button class="primary-button" type="submit">Reset password</button>
      </div>
    </template>
  </form>
</template>

<style scoped>
.auth-form {
  display: grid;
  gap: 13px;
}

.step-label {
  margin: 0 0 3px;
  color: #687386;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.7px;
  text-transform: uppercase;
}

.step-label span {
  padding: 0 3px;
}

.step-description {
  margin: 0;
  color: var(--color-muted);
  font-size: 12px;
  line-height: 1.6;
}

.step-description strong {
  color: var(--color-ink);
  font-weight: 600;
  overflow-wrap: anywhere;
}

.field {
  display: grid;
  gap: 7px;
  color: #36425a;
  font-size: 12px;
  font-weight: 600;
}

.field input {
  width: 100%;
  height: 38px;
  padding: 0 10px;
  border: 0;
  border-bottom: 1px solid #8a94a6;
  border-radius: 0;
  outline: none;
  background: #fff;
  color: var(--color-ink);
  font-size: 12px;
  font-weight: 400;
}

.field input::placeholder {
  color: #a6adbb;
}

.field input:focus {
  border-color: #8188f1;
  box-shadow: 0 1px 0 var(--color-primary);
}

.code-input {
  position: relative;
  display: grid;
  grid-template-columns: repeat(8, minmax(0, 1fr));
  gap: 7px;
}

.code-cell {
  display: grid;
  height: 46px;
  place-items: center;
  border: 1px solid #d8dce5;
  border-radius: 7px;
  background: #fff;
  color: var(--color-ink);
  font-size: 18px;
  font-weight: 600;
  transition:
    border-color 150ms ease,
    box-shadow 150ms ease;
}

.code-input.is-focused .code-cell.is-active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgb(90 98 232 / 14%);
}

.code-cell.is-filled {
  border-color: #aeb5c3;
}

.code-native-input {
  position: absolute;
  z-index: 1;
  inset: 0;
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  opacity: 0;
  cursor: text;
}

.code-native-input:focus {
  outline: none;
}

.field-hint {
  color: var(--color-muted);
  font-size: 10px;
  font-weight: 400;
}

.form-error {
  margin: -4px 0 0;
  color: #bc3546;
  font-size: 11px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 2px;
}

.primary-button,
.secondary-button {
  min-width: 112px;
  height: 40px;
  padding: 0 18px;
  border: 0;
  border-radius: 0;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}

.primary-button {
  background: var(--color-primary);
  color: #fff;
  transition: background 150ms ease;
}

.primary-button:hover {
  background: var(--color-primary-dark);
}

.secondary-button {
  background: transparent;
  color: var(--color-ink);
}

.secondary-button:hover {
  background: #f3f3f3;
}

.primary-button:focus-visible,
.secondary-button:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}

@media (max-width: 380px) {
  .code-input {
    gap: 4px;
  }

  .code-cell {
    height: 42px;
  }
}
</style>
