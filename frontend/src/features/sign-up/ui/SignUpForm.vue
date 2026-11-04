<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

import CountryPicker from './CountryPicker.vue'

const step = ref(1)
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const verificationCode = ref('')
const firstName = ref('')
const lastName = ref('')
const countryOfOrigin = ref('')
const countryCallingCountry = ref('')
const phoneNumber = ref('')
const city = ref('')
const street = ref('')
const houseNumber = ref('')
const postalCode = ref('')
const profilePicture = ref<File | null>(null)
const profilePicturePreview = ref('')
const dateOfBirth = ref('')
const formError = ref('')
const codeInputFocused = ref(false)
const codeDigits = computed(() => Array.from(verificationCode.value.padEnd(8, ' ')))
const avatarInitial = computed(() => email.value.trim().charAt(0).toUpperCase() || '?')

const stepTitle = computed(() => {
  if (step.value === 1) return 'Your account details'
  if (step.value === 2) return 'Verify your email'
  if (step.value === 3) return 'Personal information'
  return 'Address and contact'
})

function handleSubmit() {
  formError.value = ''

  if (step.value === 1) {
    if (password.value !== confirmPassword.value) {
      formError.value = 'Your passwords do not match.'
      return
    }

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

  if (step.value === 3) {
    if (!countryOfOrigin.value) {
      formError.value = 'Select your country of origin.'
      return
    }

    step.value = 4
    return
  }

  if (!countryCallingCountry.value) {
    formError.value = 'Select your country calling code.'
  }
}

function editCredentials() {
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

function handleProfilePictureChange(event: Event) {
  const input = event.target

  if (!(input instanceof HTMLInputElement)) return

  const file = input.files?.[0]
  if (!file) return

  if (profilePicturePreview.value) URL.revokeObjectURL(profilePicturePreview.value)
  profilePicture.value = file
  profilePicturePreview.value = URL.createObjectURL(file)
}

onBeforeUnmount(() => {
  if (profilePicturePreview.value) URL.revokeObjectURL(profilePicturePreview.value)
})
</script>

<template>
  <form class="auth-form" @submit.prevent="handleSubmit">
    <p class="step-label">STEP {{ step }} OF 4 <span aria-hidden="true">·</span> {{ stepTitle }}</p>

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

      <label class="field">
        <span>Password</span>
        <input
          v-model="password"
          type="password"
          name="password"
          placeholder="At least 8 characters"
          autocomplete="new-password"
          minlength="8"
          required
          @input="formError = ''"
        />
      </label>

      <label class="field">
        <span>Confirm password</span>
        <input
          v-model="confirmPassword"
          type="password"
          name="confirmPassword"
          placeholder="Enter your password again"
          autocomplete="new-password"
          minlength="8"
          required
          @input="formError = ''"
        />
      </label>
      <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>
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
        <button class="secondary-button" type="button" @click="editCredentials">Back</button>
        <button class="primary-button" type="submit">Verify email</button>
      </div>
    </template>

    <template v-else-if="step === 3">
      <p class="step-description">
        Your email is verified. Add your personal details and profile picture.
      </p>
      <section class="profile-photo-section" aria-label="Profile picture">
        <div class="avatar" role="img" aria-label="Profile picture preview">
          <img v-if="profilePicturePreview" :src="profilePicturePreview" alt="" />
          <span v-else>{{ avatarInitial }}</span>
        </div>
        <label class="photo-upload">
          <span>Choose profile picture</span>
          <input
            type="file"
            name="profilePicture"
            accept="image/*"
            aria-label="Choose a profile picture"
            @change="handleProfilePictureChange"
          />
        </label>
        <span v-if="profilePicture" class="field-hint">{{ profilePicture.name }}</span>
      </section>

      <section class="profile-section" aria-labelledby="personal-information-title">
        <h2 id="personal-information-title" class="section-title">Personal information</h2>
        <div class="field-row">
          <label class="field">
            <span>First name</span>
            <input
              v-model="firstName"
              type="text"
              name="firstName"
              autocomplete="given-name"
              required
            />
          </label>
          <label class="field">
            <span>Last name</span>
            <input
              v-model="lastName"
              type="text"
              name="lastName"
              autocomplete="family-name"
              required
            />
          </label>
        </div>

        <label class="field">
          <span>Date of birth</span>
          <input
            v-model="dateOfBirth"
            type="date"
            name="dateOfBirth"
            autocomplete="bday"
            required
          />
        </label>

        <div class="field">
          <span>Country of origin</span>
          <CountryPicker
            v-model="countryOfOrigin"
            mode="country"
            label="Country of origin"
            @update:model-value="formError = ''"
          />
        </div>
      </section>

      <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>
      <div class="actions">
        <button class="secondary-button" type="button" @click="step = 2">Back</button>
        <button class="primary-button" type="submit">Continue</button>
      </div>
    </template>

    <template v-else>
      <p class="step-description">Add your home address and contact details.</p>
      <section class="profile-section" aria-labelledby="address-title">
        <h2 id="address-title" class="section-title">Home address</h2>
        <div class="field-row">
          <label class="field">
            <span>City</span>
            <input v-model="city" type="text" name="city" autocomplete="address-level2" required />
          </label>
          <label class="field">
            <span>Postal code</span>
            <input
              v-model="postalCode"
              type="text"
              name="postalCode"
              autocomplete="postal-code"
              required
            />
          </label>
        </div>
        <div class="field-row">
          <label class="field">
            <span>Street</span>
            <input
              v-model="street"
              type="text"
              name="street"
              autocomplete="address-line1"
              required
            />
          </label>
          <label class="field">
            <span>House number</span>
            <input
              v-model="houseNumber"
              type="text"
              name="houseNumber"
              autocomplete="address-line2"
              required
            />
          </label>
        </div>
      </section>

      <section class="profile-section" aria-labelledby="contact-information-title">
        <h2 id="contact-information-title" class="section-title">Contact information</h2>
        <label class="field">
          <span>Email address</span>
          <input
            :value="email"
            type="email"
            name="profileEmail"
            autocomplete="email"
            readonly
          />
        </label>
        <div class="field-row phone-row">
          <div class="field">
            <span>Country calling code</span>
            <CountryPicker
              v-model="countryCallingCountry"
              mode="callingCode"
              label="Country calling code"
              @update:model-value="formError = ''"
            />
          </div>
          <label class="field">
            <span>Phone number</span>
            <input
              v-model="phoneNumber"
              type="tel"
              name="phoneNumber"
              autocomplete="tel-national"
              inputmode="tel"
              placeholder="123 456 789"
              required
            />
          </label>
        </div>
      </section>

      <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>
      <div class="actions">
        <button class="secondary-button" type="button" @click="step = 3">Back</button>
        <button class="primary-button" type="submit">Create account</button>
      </div>
    </template>
  </form>
</template>

<style scoped>
.auth-form {
  display: grid;
  gap: 12px;
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

.profile-photo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 4px 0 8px;
}

.avatar {
  display: grid;
  width: 96px;
  height: 96px;
  flex: 0 0 96px;
  overflow: hidden;
  place-items: center;
  border-radius: 50%;
  background: #e8e9ff;
  color: var(--color-primary);
  font-size: 25px;
  font-weight: 600;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-upload {
  position: relative;
  display: inline-flex;
  min-height: 36px;
  align-items: center;
  padding: 0 12px;
  border: 1px solid #d8dce5;
  color: var(--color-primary);
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
}

.photo-upload:hover {
  background: #f7f7ff;
}

.photo-upload input {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  clip-path: inset(50%);
}

.photo-upload:focus-within {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}

.profile-section {
  display: grid;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid #eceef2;
}

.section-title {
  margin: 0;
  color: var(--color-ink);
  font-size: 13px;
  font-weight: 600;
}

.field {
  display: grid;
  gap: 7px;
  color: #36425a;
  font-size: 12px;
  font-weight: 600;
}

.field-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.field input,
.field select {
  min-width: 0;
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

.field input:focus,
.field select:focus {
  border-color: #8188f1;
  box-shadow: 0 1px 0 var(--color-primary);
}

.field input[readonly] {
  background: #f5f6f8;
  color: var(--color-muted);
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
  .field-row {
    grid-template-columns: 1fr;
  }

  .code-input {
    gap: 4px;
  }

  .code-cell {
    height: 42px;
  }
}
</style>
