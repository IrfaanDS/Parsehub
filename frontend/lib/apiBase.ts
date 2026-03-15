/**
 * Backend API key for x-api-key header. Read from NEXT_PUBLIC_BACKEND_API_KEY.
 * Never hardcode the key in code.
 */
export function getBackendApiKey(): string | undefined {
  return process.env.NEXT_PUBLIC_BACKEND_API_KEY;
}

/**
 * Headers to send with every request to /api/* (backend).
 * Includes x-api-key when NEXT_PUBLIC_BACKEND_API_KEY is set.
 */
export function getApiHeaders(): Record<string, string> {
  const key = getBackendApiKey();
  if (!key) return {};
  return { 'x-api-key': key };
}

export function getApiBaseUrl(): string {
    const isServer = typeof window === 'undefined';

    const envUrl = process.env.NEXT_PUBLIC_API_BASE_URL ||
        process.env.NEXT_PUBLIC_BACKEND_URL ||
        (isServer ? process.env.BACKEND_API_URL || process.env.BACKEND_URL : undefined);

    if (process.env.NODE_ENV === 'production') {
        if (!envUrl) {
            console.warn("WARNING: API base URL missing in production. Falling back to localhost.");
        }
        return envUrl || 'http://localhost:5000';
    }

    return envUrl || 'http://localhost:5000';
}

export function getFrontendApiUrl(): string {
    const envUrl = process.env.NEXT_PUBLIC_API_URL;

    if (process.env.NODE_ENV === 'production') {
        if (!envUrl) {
            // In production, Next.js relative paths work for frontend APIs if in browser
            if (typeof window !== 'undefined') {
                return '';
            }
            console.warn("WARNING: Frontend API URL missing in production. Falling back to localhost.");
        }
        return envUrl || 'http://localhost:3000';
    }

    return envUrl || 'http://localhost:3000';
}
