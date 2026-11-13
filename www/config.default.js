// Medsathi — shipped defaults (committed on purpose).
//
// Only PUBLIC values belong here:
//   * the Supabase project URL
//   * the Supabase anon / publishable key — a client key by design, it is
//     shipped inside every Supabase web and mobile app. Row level security is
//     what protects the data, never the key (see docs/SUPABASE_AUTH.md).
//   * the service_role / secret key must NEVER appear in this repo.
//
// Because these ship in the APK, login and cloud sync work on a fresh install
// with zero setup. `www/config.js` (git-ignored, generated from repository
// secrets) still wins over anything here, so personal API keys and a different
// Supabase project can be injected at build time without touching this file.
window.CURAMED_DEFAULT_CONFIG = {
  backendUrl: '',
  apiKeys: {
    tinyfish: '',
    openfda: '',
    gemini: ''
  },
  supabase: {
    url: 'https://ljuertzeznwzyskluptz.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxqdWVydHplem53enlza2x1cHR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ1NDE5MzksImV4cCI6MjExMDExNzkzOX0.uMYyL1AAK_BCVlhiwrwtYodJEsco81L4dtWZdfVA4fU'
  }
};
