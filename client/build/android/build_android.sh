#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

if command -v python3 >/dev/null 2>&1; then
  python3 -m pip install Pillow cairosvg || echo "WARN: logo renderer dependencies failed. Using existing icon assets."
  if ! python3 build/assets/prepare_logo_assets.py; then
    echo "WARN: logo asset preparation failed. Using existing icon assets."
  fi
fi

cd android
GRADLE_CMD=""

if command -v gradle >/dev/null 2>&1; then
  GRADLE_CMD="gradle"
elif [[ -x "./gradlew" ]]; then
  GRADLE_CMD="./gradlew"
else
  GRADLE_VERSION="8.7"
  CACHE_DIR="${HOME}/.cache/kabootar/gradle-${GRADLE_VERSION}"
  GRADLE_BIN="${CACHE_DIR}/gradle-${GRADLE_VERSION}/bin/gradle"
  if [[ ! -x "${GRADLE_BIN}" ]]; then
    echo "Gradle not found. Downloading Gradle ${GRADLE_VERSION}..."
    mkdir -p "${CACHE_DIR}"
    ZIP_PATH="${CACHE_DIR}/gradle.zip"
    curl -fsSL "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" -o "${ZIP_PATH}"
    rm -rf "${CACHE_DIR}/gradle-${GRADLE_VERSION}"
    unzip -oq "${ZIP_PATH}" -d "${CACHE_DIR}"
  fi
  GRADLE_CMD="${GRADLE_BIN}"
fi

"${GRADLE_CMD}" :app:clean :app:assembleDebug :app:assembleRelease

RELEASE_DIR="app/build/outputs/apk/release"
UNIVERSAL_SOURCE="${RELEASE_DIR}/app-universal-release.apk"
[[ -f "${UNIVERSAL_SOURCE}" ]] || UNIVERSAL_SOURCE="${RELEASE_DIR}/app-release.apk"
ARM64_SOURCE="${RELEASE_DIR}/app-arm64-v8a-release.apk"
X64_SOURCE="${RELEASE_DIR}/app-x86_64-release.apk"

if [[ ! -f "${UNIVERSAL_SOURCE}" ]]; then
  echo "ERROR: universal release APK not found" >&2
  exit 1
fi
if [[ ! -f "${ARM64_SOURCE}" ]]; then
  echo "ERROR: arm64-v8a release APK not found" >&2
  exit 1
fi
if [[ ! -f "${X64_SOURCE}" ]]; then
  echo "ERROR: x86_64 release APK not found" >&2
  exit 1
fi
cp -f "${UNIVERSAL_SOURCE}" "${RELEASE_DIR}/kabootar-android-universal.apk"
cp -f "${ARM64_SOURCE}" "${RELEASE_DIR}/kabootar-android-arm64-v8a.apk"
cp -f "${X64_SOURCE}" "${RELEASE_DIR}/kabootar-android-x86_64.apk"

echo "Debug APK: app/build/outputs/apk/debug/app-debug.apk"
echo "Universal APK: ${RELEASE_DIR}/kabootar-android-universal.apk"
echo "ARM64 APK: ${RELEASE_DIR}/kabootar-android-arm64-v8a.apk"
echo "x86_64 APK: ${RELEASE_DIR}/kabootar-android-x86_64.apk"
