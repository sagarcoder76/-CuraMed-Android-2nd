#!/bin/bash
set -e
cd "$(dirname "$0")"
npm install
npx cap add android || true
npx cap sync android
echo
 echo 'Android project prepared. Open Android Studio with: npx cap open android'
