const DEFAULT_API_BASE_URL = 'http://localhost:8000';

function normalizeApiBaseUrl(value) {
  if (!value) return null;

  const trimmed = String(value).trim().replace(/^['"]|['"]$/g, '');

  if (!trimmed) return null;

  // Guard against accidentally deploying unresolved placeholders like ${API_BASE_URL}.
  if (trimmed.includes('${')) return null;

  return trimmed.replace(/\/+$/, '');
}

const resolvedApiBaseUrl =
  normalizeApiBaseUrl(import.meta.env.VITE_API_URL) ||
  normalizeApiBaseUrl(import.meta.env.API_BASE_URL) ||
  DEFAULT_API_BASE_URL;

console.log('Resolved API base URL:', resolvedApiBaseUrl);

export const API_BASE_URL = resolvedApiBaseUrl;
