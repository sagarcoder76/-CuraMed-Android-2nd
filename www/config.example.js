// CuraMed build-time config — TEMPLATE ONLY.
// Copy to `config.js` for a local build. `config.js` is git-ignored, so real
// keys are never committed. The GitHub Actions build generates it from the
// repository secrets TINYFISH_API_KEY / OPENFDA_API_KEY / GEMINI_API_KEY.
//
// NOTE: anything in this file ships inside the APK and can be extracted by
// someone who downloads it. Only do this with free-tier keys you can rotate,
// or point the app at your own backend proxy instead (see README_ANDROID.md).
//
// Two ways to ship a working app:
//   A. fill apiKeys below  -> keys live inside the APK (convenient, extractable)
//   B. set backendUrl      -> keys stay on your server (safe for public release)
//      deploy medicine_assistant/ and point this at it, e.g.
//      backendUrl: 'https://curamed-api.vercel.app'
window.CURAMED_CONFIG = {
  backendUrl: '',
  apiKeys: {
    tinyfish: '', // https://agent.tinyfish.ai/api-keys   (free 12k searches/day)
    openfda: '', // https://open.fda.gov/apis/authentication/
    gemini: ''   // https://aistudio.google.com/apikey
  }
};
