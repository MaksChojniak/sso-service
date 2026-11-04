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
    expect(wrapper.find('input[name="remember"]').exists()).toBe(false)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Login')
  })

  it('starts registration by asking for email and matching passwords', () => {
    const wrapper = mount(SignUpForm)

    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[name="password"]').exists()).toBe(true)
    expect(wrapper.find('input[name="confirmPassword"]').exists()).toBe(true)
    expect(wrapper.find('input[name="firstName"]').exists()).toBe(false)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Continue')
  })

  it('requires matching passwords before showing email verification', async () => {
    const wrapper = mount(SignUpForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('input[name="password"]').setValue('password1')
    await wrapper.find('input[name="confirmPassword"]').setValue('password2')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('[role="alert"]').text()).toBe('Your passwords do not match.')
    expect(wrapper.find('input[name="verificationCode"]').exists()).toBe(false)
  })

  it('verifies an 8-digit code before showing personal profile details', async () => {
    const wrapper = mount(SignUpForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('input[name="password"]').setValue('password1')
    await wrapper.find('input[name="confirmPassword"]').setValue('password1')
    await wrapper.find('form').trigger('submit')
    expect(wrapper.find('input[name="verificationCode"]').exists()).toBe(true)
    expect(wrapper.findAll('.code-cell')).toHaveLength(8)

    const codeInput = wrapper.find('input[name="verificationCode"]')
    expect(codeInput.attributes('pattern')).toBe('[0-9]{8}')
    await codeInput.setValue('12a345678')
    expect((codeInput.element as HTMLInputElement).value).toBe('12345678')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('input[name="firstName"]').exists()).toBe(true)
    expect(wrapper.find('input[name="lastName"]').exists()).toBe(true)
    expect(wrapper.find('button[aria-label="Country of origin"]').exists()).toBe(true)
    expect(wrapper.find('input[name="profilePicture"]').attributes('accept')).toBe('image/*')
    expect(wrapper.find('.avatar').text()).toBe('U')
    expect(wrapper.find('input[name="dateOfBirth"]').attributes('type')).toBe('date')
    expect(wrapper.find('button[type="submit"]').text()).toBe('Continue')

    await wrapper.find('form').trigger('submit')
    expect(wrapper.find('[role="alert"]').text()).toBe('Select your country of origin.')
    await wrapper.find('button[aria-label="Country of origin"]').trigger('click')
    const countrySearch = wrapper.find('input[role="combobox"]')
    expect(countrySearch.attributes('placeholder')).toContain('countries')
    await countrySearch.setValue('poland')
    expect(wrapper.findAll('[role="option"]')).toHaveLength(1)
    expect(wrapper.find('[role="option"]').text()).toContain('Poland')
    expect(wrapper.find('[role="option"] img').attributes('src')).toContain('/flags/PL.svg')
    await wrapper.find('[role="option"]').trigger('click')
    expect(wrapper.find('button[aria-label="Country of origin"]').text()).toContain('Poland')
    expect(
      wrapper.find('button[aria-label="Country of origin"] img').attributes('src'),
    ).toContain('/flags/PL.svg')

    await wrapper.find('form').trigger('submit')
    expect(wrapper.find('input[name="city"]').exists()).toBe(true)
    expect(wrapper.find('input[name="street"]').exists()).toBe(true)
    expect(wrapper.find('input[name="houseNumber"]').exists()).toBe(true)
    expect(wrapper.find('input[name="postalCode"]').exists()).toBe(true)
    expect(wrapper.find('input[name="profileEmail"]').element.hasAttribute('readonly')).toBe(true)
    expect((wrapper.find('input[name="profileEmail"]').element as HTMLInputElement).value).toBe(
      'user@example.com',
    )
    expect(wrapper.find('input[name="phoneNumber"]').exists()).toBe(true)
    const phoneInput = wrapper.find('input[name="phoneNumber"]')
    await phoneInput.setValue('111222333')
    expect((phoneInput.element as HTMLInputElement).value).toBe('111 222 333')
    await phoneInput.setValue('+48 111 222 333 444 5555')
    expect((phoneInput.element as HTMLInputElement).value).toBe('481 112 223 334 445')
    expect(wrapper.find('button[aria-label="Country calling code"]').exists()).toBe(true)
    await wrapper.find('form').trigger('submit')
    expect(wrapper.find('[role="alert"]').text()).toBe('Select your country calling code.')
    await wrapper.find('button[aria-label="Country calling code"]').trigger('click')
    const codeSearch = wrapper.find('input[role="combobox"]')
    expect(codeSearch.attributes('placeholder')).toContain('countries or codes')
    await codeSearch.setValue('+48')
    expect(wrapper.findAll('[role="option"]')).toHaveLength(1)
    expect(wrapper.find('[role="option"]').text()).toContain('+48')
    expect(wrapper.find('[role="option"]').text()).not.toContain('Poland')
    expect(wrapper.find('[role="option"] img').attributes('src')).toContain('/flags/PL.svg')
    await wrapper.find('[role="option"]').trigger('click')
    expect(wrapper.find('button[aria-label="Country calling code"]').text()).toContain('+48')
    expect(
      wrapper.find('button[aria-label="Country calling code"] img').attributes('src'),
    ).toContain('/flags/PL.svg')
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
    expect(wrapper.findAll('.code-cell')).toHaveLength(8)

    await codeInput.setValue('12a345678')
    expect((codeInput.element as HTMLInputElement).value).toBe('12345678')

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
