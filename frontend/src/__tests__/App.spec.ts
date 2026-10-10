import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import SignInForm from '../features/sign-in/ui/SignInForm.vue'
import SignUpForm from '../features/sign-up/ui/SignUpForm.vue'
import ResetPasswordForm from '../features/reset-password/ui/ResetPasswordForm.vue'

describe('authentication forms', () => {
  it('renders the email and password sign-in fields', () => {
    const wrapper = mount(SignInForm, { global: { stubs: ['RouterLink'] } })

    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[name="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Login')
  })

  it('renders the basic account registration fields', () => {
    const wrapper = mount(SignUpForm)

    expect(wrapper.find('input[name="name"]').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[name="password"]').exists()).toBe(true)
    expect(wrapper.find('input[name="confirmPassword"]').exists()).toBe(true)
  })

  it('requires an email, an 8-digit code, and a new password to reset access', () => {
    const wrapper = mount(ResetPasswordForm)
    const codeInput = wrapper.find('input[name="verificationCode"]')

    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(codeInput.attributes('pattern')).toBe('[0-9]{8}')
    expect(codeInput.attributes('maxlength')).toBe('8')
    expect(wrapper.find('input[name="password"]').exists()).toBe(true)
  })
})
