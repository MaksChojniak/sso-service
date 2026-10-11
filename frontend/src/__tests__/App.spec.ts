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

  it('starts password reset by asking for an email address', () => {
    const wrapper = mount(ResetPasswordForm)

    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[name="verificationCode"]').exists()).toBe(false)
    expect(wrapper.find('input[name="password"]').exists()).toBe(false)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Continue')
  })

  it('asks for an 8-digit code before allowing the new password step', async () => {
    const wrapper = mount(ResetPasswordForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('form').trigger('submit')
    expect(wrapper.find('input[name="verificationCode"]').exists()).toBe(true)
    expect(wrapper.find('input[name="password"]').exists()).toBe(false)

    const codeInput = wrapper.find('input[name="verificationCode"]')
    expect(codeInput.attributes('pattern')).toBe('[0-9]{8}')
    expect(codeInput.attributes('maxlength')).toBe('8')

    await codeInput.setValue('1234567')
    await wrapper.find('form').trigger('submit')
    expect(wrapper.find('input[name="password"]').exists()).toBe(false)

    await codeInput.setValue('12345678')
    await wrapper.find('form').trigger('submit')
    expect(wrapper.find('input[name="password"]').exists()).toBe(true)
    expect(wrapper.find('input[name="confirmPassword"]').exists()).toBe(true)
  })

  it('shows a validation message when the new passwords do not match', async () => {
    const wrapper = mount(ResetPasswordForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('form').trigger('submit')
    await wrapper.find('input[name="verificationCode"]').setValue('12345678')
    await wrapper.find('form').trigger('submit')
    await wrapper.find('input[name="password"]').setValue('password1')
    await wrapper.find('input[name="confirmPassword"]').setValue('password2')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('[role="alert"]').text()).toBe('Your passwords do not match.')
  })
})
