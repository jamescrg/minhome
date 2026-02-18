// E2E encryption utilities using Web Crypto API
// AES-256-GCM with PBKDF2 key derivation

const PBKDF2_ITERATIONS = 100000;
const SALT_BYTES = 16;
const IV_BYTES = 12;
const SESSION_KEY = "notes_encryption_key";

export const KEY_TTL_MS = 15 * 60 * 1000; // 15 minutes

// Generate a random 16-byte salt, returned as base64
export function generateSalt() {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_BYTES));
  return uint8ToBase64(salt);
}

// Derive an AES-256-GCM CryptoKey from passphrase + base64 salt
export async function deriveKey(passphrase, saltB64) {
  const enc = new TextEncoder();
  const salt = base64ToUint8(saltB64);

  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    enc.encode(passphrase),
    "PBKDF2",
    false,
    ["deriveKey"]
  );

  return crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: salt,
      iterations: PBKDF2_ITERATIONS,
      hash: "SHA-256",
    },
    keyMaterial,
    { name: "AES-GCM", length: 256 },
    true, // extractable for JWK export
    ["encrypt", "decrypt"]
  );
}

// Encrypt plaintext string, returns base64(iv || ciphertext)
export async function encrypt(plaintext, key) {
  const enc = new TextEncoder();
  const iv = crypto.getRandomValues(new Uint8Array(IV_BYTES));

  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv: iv },
    key,
    enc.encode(plaintext)
  );

  // Prepend IV to ciphertext
  const combined = new Uint8Array(IV_BYTES + ciphertext.byteLength);
  combined.set(iv, 0);
  combined.set(new Uint8Array(ciphertext), IV_BYTES);

  return uint8ToBase64(combined);
}

// Decrypt base64(iv || ciphertext), returns plaintext string. Throws on wrong key.
export async function decrypt(encoded, key) {
  const combined = base64ToUint8(encoded);

  const iv = combined.slice(0, IV_BYTES);
  const ciphertext = combined.slice(IV_BYTES);

  const plainBuffer = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: iv },
    key,
    ciphertext
  );

  return new TextDecoder().decode(plainBuffer);
}

// Key management (JWK in localStorage for persistence across sessions)
export function hasStoredKey() {
  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) return false;
  const stored = JSON.parse(raw);
  // Support both old (plain JWK) and new (JWK + timestamp) formats
  return stored && (stored.jwk || stored.kty);
}

export function hasFreshKey(ttlMs) {
  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) return false;
  const stored = JSON.parse(raw);
  if (!stored || !stored.jwk || !stored.timestamp) return false;
  return (Date.now() - stored.timestamp) < ttlMs;
}

export function refreshKeyTimestamp() {
  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) return;
  const stored = JSON.parse(raw);
  if (!stored || !stored.jwk) return;
  stored.timestamp = Date.now();
  localStorage.setItem(SESSION_KEY, JSON.stringify(stored));
}

export async function getStoredKey() {
  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) return null;

  const stored = JSON.parse(raw);
  // Support old format (plain JWK object with "kty" property)
  const jwk = stored.jwk || stored;
  return crypto.subtle.importKey(
    "jwk",
    jwk,
    { name: "AES-GCM", length: 256 },
    true,
    ["encrypt", "decrypt"]
  );
}

export async function storeKey(key) {
  const jwk = await crypto.subtle.exportKey("jwk", key);
  localStorage.setItem(SESSION_KEY, JSON.stringify({
    jwk: jwk,
    timestamp: Date.now(),
  }));
}

export function clearStoredKey() {
  localStorage.removeItem(SESSION_KEY);
}

// Base64 helpers
function uint8ToBase64(bytes) {
  let binary = "";
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function base64ToUint8(b64) {
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}
