function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null
  }
  return null
}

export async function apiRequest<T = any>(
  path: string,
  options: RequestInit = {},
): Promise<{ data: T | null; error: string | null; status: number }> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  }

  // Include CSRF token on mutating requests if present
  const method = (options.method || 'GET').toUpperCase()
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    const csrfToken = getCookie('csrftoken')
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken
    }
  }

  try {
    const res = await fetch(path, {
      ...options,
      headers,
      credentials: 'same-origin',
    })

    const status = res.status
    let data = null
    try {
      data = await res.json()
    } catch {
      // no JSON body
    }

    if (!res.ok) {
      let errorMsg = `Request failed (${status})`
      if (data?.error) {
        errorMsg = typeof data.error === 'string' ? data.error : JSON.stringify(data.error)
      } else if (data?.errors) {
        // Collect field errors
        const allErrors = Object.entries(data.errors)
          .map(([field, errs]: [string, any]) => {
            if (Array.isArray(errs)) {
              return `${field}: ${errs.map(e => e.message || e).join(', ')}`
            }
            return `${field}: ${errs}`
          })
          .join(' | ')
        errorMsg = allErrors || errorMsg
      }
      return { data, error: errorMsg, status }
    }

    return { data, error: null, status }
  } catch (err: any) {
    return { data: null, error: err.message || 'Network error', status: 0 }
  }
}
