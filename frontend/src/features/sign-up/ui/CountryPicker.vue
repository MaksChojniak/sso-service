<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, useId } from 'vue'

const props = defineProps<{
  modelValue: string
  mode: 'country' | 'callingCode'
  label: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const countries = [
  { code: 'AR', name: 'Argentina', callingCode: '+54' },
  { code: 'AU', name: 'Australia', callingCode: '+61' },
  { code: 'AT', name: 'Austria', callingCode: '+43' },
  { code: 'BE', name: 'Belgium', callingCode: '+32' },
  { code: 'BR', name: 'Brazil', callingCode: '+55' },
  { code: 'BG', name: 'Bulgaria', callingCode: '+359' },
  { code: 'CA', name: 'Canada', callingCode: '+1' },
  { code: 'CL', name: 'Chile', callingCode: '+56' },
  { code: 'CN', name: 'China', callingCode: '+86' },
  { code: 'CO', name: 'Colombia', callingCode: '+57' },
  { code: 'HR', name: 'Croatia', callingCode: '+385' },
  { code: 'CY', name: 'Cyprus', callingCode: '+357' },
  { code: 'CZ', name: 'Czechia', callingCode: '+420' },
  { code: 'DK', name: 'Denmark', callingCode: '+45' },
  { code: 'EG', name: 'Egypt', callingCode: '+20' },
  { code: 'EE', name: 'Estonia', callingCode: '+372' },
  { code: 'FI', name: 'Finland', callingCode: '+358' },
  { code: 'FR', name: 'France', callingCode: '+33' },
  { code: 'DE', name: 'Germany', callingCode: '+49' },
  { code: 'GR', name: 'Greece', callingCode: '+30' },
  { code: 'HK', name: 'Hong Kong', callingCode: '+852' },
  { code: 'HU', name: 'Hungary', callingCode: '+36' },
  { code: 'IS', name: 'Iceland', callingCode: '+354' },
  { code: 'IN', name: 'India', callingCode: '+91' },
  { code: 'ID', name: 'Indonesia', callingCode: '+62' },
  { code: 'IE', name: 'Ireland', callingCode: '+353' },
  { code: 'IL', name: 'Israel', callingCode: '+972' },
  { code: 'IT', name: 'Italy', callingCode: '+39' },
  { code: 'JP', name: 'Japan', callingCode: '+81' },
  { code: 'KE', name: 'Kenya', callingCode: '+254' },
  { code: 'LV', name: 'Latvia', callingCode: '+371' },
  { code: 'LT', name: 'Lithuania', callingCode: '+370' },
  { code: 'LU', name: 'Luxembourg', callingCode: '+352' },
  { code: 'MY', name: 'Malaysia', callingCode: '+60' },
  { code: 'MX', name: 'Mexico', callingCode: '+52' },
  { code: 'MA', name: 'Morocco', callingCode: '+212' },
  { code: 'NL', name: 'Netherlands', callingCode: '+31' },
  { code: 'NZ', name: 'New Zealand', callingCode: '+64' },
  { code: 'NG', name: 'Nigeria', callingCode: '+234' },
  { code: 'NO', name: 'Norway', callingCode: '+47' },
  { code: 'PK', name: 'Pakistan', callingCode: '+92' },
  { code: 'PH', name: 'Philippines', callingCode: '+63' },
  { code: 'PL', name: 'Poland', callingCode: '+48' },
  { code: 'PT', name: 'Portugal', callingCode: '+351' },
  { code: 'RO', name: 'Romania', callingCode: '+40' },
  { code: 'SA', name: 'Saudi Arabia', callingCode: '+966' },
  { code: 'SG', name: 'Singapore', callingCode: '+65' },
  { code: 'SK', name: 'Slovakia', callingCode: '+421' },
  { code: 'SI', name: 'Slovenia', callingCode: '+386' },
  { code: 'ZA', name: 'South Africa', callingCode: '+27' },
  { code: 'KR', name: 'South Korea', callingCode: '+82' },
  { code: 'ES', name: 'Spain', callingCode: '+34' },
  { code: 'SE', name: 'Sweden', callingCode: '+46' },
  { code: 'CH', name: 'Switzerland', callingCode: '+41' },
  { code: 'TW', name: 'Taiwan', callingCode: '+886' },
  { code: 'TH', name: 'Thailand', callingCode: '+66' },
  { code: 'TR', name: 'Türkiye', callingCode: '+90' },
  { code: 'UA', name: 'Ukraine', callingCode: '+380' },
  { code: 'AE', name: 'United Arab Emirates', callingCode: '+971' },
  { code: 'GB', name: 'United Kingdom', callingCode: '+44' },
  { code: 'US', name: 'United States', callingCode: '+1' },
  { code: 'VN', name: 'Vietnam', callingCode: '+84' },
]

const id = useId()
const root = ref<HTMLElement | null>(null)
const searchInput = ref<HTMLInputElement | null>(null)
const isOpen = ref(false)
const searchQuery = ref('')
const popoverStyle = ref<Record<string, string>>({})
const selectedCountry = computed(() => countries.find(({ code }) => code === props.modelValue))
const filteredCountries = computed(() => {
  const query = searchQuery.value
    .trim()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()

  if (!query) return countries

  return countries.filter(({ name, callingCode }) => {
    const searchable = `${name} ${callingCode}`
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()

    return searchable.includes(query)
  })
})
const triggerId = `country-picker-${id}`
const listId = `country-options-${id}`
const popoverHeight = 154

function countryFlag(countryCode: string) {
  return new URL(`../../../assets/flags/${countryCode.toUpperCase()}.svg`, import.meta.url).href
}

function countryLabel(country: (typeof countries)[number]) {
  return props.mode === 'country' ? country.name : country.callingCode
}

function openPicker() {
  isOpen.value = true
  searchQuery.value = ''
  void nextTick(() => {
    updatePopoverPosition()
    searchInput.value?.focus({ preventScroll: true })
  })
}

function closePicker() {
  isOpen.value = false
  searchQuery.value = ''
}

function updatePopoverPosition() {
  const bounds = root.value?.getBoundingClientRect()
  if (!bounds) return

  const edge = 8
  const width = Math.min(Math.max(bounds.width, 220), window.innerWidth - edge * 2)
  const left = Math.min(Math.max(bounds.left, edge), window.innerWidth - width - edge)
  const spaceBelow = window.innerHeight - bounds.bottom - edge
  const spaceAbove = bounds.top - edge
  const placeAbove = spaceBelow < popoverHeight && spaceAbove > spaceBelow
  const top = placeAbove
    ? Math.max(edge, bounds.top - popoverHeight - 4)
    : Math.min(bounds.bottom + 4, window.innerHeight - popoverHeight - edge)

  popoverStyle.value = {
    top: `${top}px`,
    left: `${left}px`,
    width: `${width}px`,
  }
}

function togglePicker() {
  if (isOpen.value) {
    closePicker()
  } else {
    openPicker()
  }
}

function selectCountry(countryCode: string) {
  emit('update:modelValue', countryCode)
  closePicker()
  void nextTick(() => document.getElementById(triggerId)?.focus({ preventScroll: true }))
}

function focusFirstOption() {
  const firstOption = filteredCountries.value[0]
  if (firstOption) {
    document.getElementById(`${listId}-${firstOption.code}`)?.focus({ preventScroll: true })
  }
}

function focusAdjacentOption(countryCode: string, direction: -1 | 1) {
  const currentIndex = filteredCountries.value.findIndex(({ code }) => code === countryCode)
  const nextCountry = filteredCountries.value[currentIndex + direction]

  if (nextCountry) {
    document.getElementById(`${listId}-${nextCountry.code}`)?.focus({ preventScroll: true })
  } else {
    searchInput.value?.focus({ preventScroll: true })
  }
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape' && isOpen.value) {
    event.preventDefault()
    closePicker()
    void nextTick(() => document.getElementById(triggerId)?.focus({ preventScroll: true }))
  }

  if (event.key === 'ArrowDown' && event.target === searchInput.value) {
    event.preventDefault()
    focusFirstOption()
  }
}

function handleDocumentClick(event: PointerEvent) {
  if (event.target instanceof Node && !root.value?.contains(event.target)) {
    closePicker()
  }
}

onMounted(() => {
  document.addEventListener('pointerdown', handleDocumentClick)
  window.addEventListener('resize', updatePopoverPosition)
  window.addEventListener('scroll', updatePopoverPosition, true)
})
onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', handleDocumentClick)
  window.removeEventListener('resize', updatePopoverPosition)
  window.removeEventListener('scroll', updatePopoverPosition, true)
})
</script>

<template>
  <div ref="root" class="country-picker" @keydown="handleKeydown">
    <button
      :id="triggerId"
      class="picker-trigger"
      type="button"
      aria-haspopup="listbox"
      :aria-expanded="isOpen"
      :aria-label="label"
      aria-required="true"
      @click="togglePicker"
    >
      <template v-if="selectedCountry">
        <img class="country-flag" :src="countryFlag(selectedCountry.code)" alt="" />
        <span class="country-label">{{ countryLabel(selectedCountry) }}</span>
      </template>
      <span v-else class="country-placeholder">{{ mode === 'country' ? 'Select a country' : 'Code' }}</span>
      <span class="picker-chevron" aria-hidden="true"></span>
    </button>

    <div v-if="isOpen" class="picker-popover" :style="popoverStyle">
      <input
        ref="searchInput"
        v-model="searchQuery"
        class="picker-search"
        type="search"
        role="combobox"
        :aria-label="`Search ${label.toLowerCase()}`"
        :aria-expanded="isOpen"
        :aria-controls="listId"
        aria-autocomplete="list"
        :placeholder="`Search ${mode === 'country' ? 'countries' : 'countries or codes'}...`"
      />
      <ul :id="listId" class="picker-options" role="listbox" :aria-label="label">
        <li v-for="country in filteredCountries" :key="country.code" role="presentation">
          <button
            :id="`${listId}-${country.code}`"
            class="picker-option"
            type="button"
            role="option"
            :aria-selected="country.code === modelValue"
            @keydown.down.prevent="focusAdjacentOption(country.code, 1)"
            @keydown.up.prevent="focusAdjacentOption(country.code, -1)"
            @click="selectCountry(country.code)"
          >
            <img class="country-flag" :src="countryFlag(country.code)" alt="" />
            <span class="country-label">{{ countryLabel(country) }}</span>
          </button>
        </li>
        <li v-if="filteredCountries.length === 0" class="no-results" role="presentation">
          No countries found.
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.country-picker {
  position: relative;
  min-width: 0;
}

.picker-trigger {
  display: flex;
  width: 100%;
  height: 38px;
  align-items: center;
  gap: 10px;
  padding: 0 10px;
  border: 0;
  border-bottom: 1px solid #8a94a6;
  border-radius: 0;
  background: #fff;
  color: var(--color-ink);
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  text-align: left;
}

.picker-trigger:focus-visible {
  border-color: #8188f1;
  outline: none;
  box-shadow: 0 1px 0 var(--color-primary);
}

.country-flag {
  display: block;
  width: 22px;
  height: 16px;
  flex: 0 0 auto;
  object-fit: cover;
  box-shadow: 0 0 0 1px rgb(23 32 52 / 10%);
}

.country-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.country-placeholder {
  flex: 1;
  color: #a6adbb;
}

.picker-chevron {
  width: 7px;
  height: 7px;
  flex: 0 0 auto;
  margin-left: auto;
  transform: translateY(-2px) rotate(45deg);
  border-right: 1px solid #77839a;
  border-bottom: 1px solid #77839a;
}

.picker-popover {
  position: fixed;
  z-index: 5;
  box-sizing: border-box;
  max-height: calc(100dvh - 16px);
  padding: 8px;
  border: 1px solid #d8dce5;
  background: #fff;
  box-shadow: 0 8px 20px rgb(23 32 52 / 14%);
}

.picker-search {
  box-sizing: border-box;
  width: 100%;
  height: 36px;
  padding: 0 9px;
  border: 1px solid #d8dce5;
  border-radius: 0;
  color: var(--color-ink);
  font: inherit;
  font-size: 12px;
}

.picker-search:focus {
  border-color: var(--color-primary);
  outline: 2px solid rgb(90 98 232 / 18%);
}

.picker-options {
  max-height: min(90px, calc(100dvh - 88px));
  overflow-y: auto;
  overscroll-behavior: contain;
  margin: 6px 0 0;
  padding: 0;
  list-style: none;
}

.picker-option {
  display: flex;
  width: 100%;
  min-height: 36px;
  align-items: center;
  gap: 10px;
  padding: 5px 8px;
  border: 0;
  background: transparent;
  color: var(--color-ink);
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  text-align: left;
}

.picker-option:hover,
.picker-option:focus-visible,
.picker-option[aria-selected='true'] {
  background: #f0f0ff;
  outline: none;
}

.no-results {
  padding: 10px 8px;
  color: var(--color-muted);
  font-size: 12px;
}
</style>
