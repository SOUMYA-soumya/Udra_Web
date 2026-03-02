#!/bin/bash
# This script tells Render how to build a Flutter Web app

echo "Downloading Flutter SDK..."
git clone https://github.com/flutter/flutter.git -b stable

echo "Adding Flutter to path..."
export PATH="$PATH:`pwd`/flutter/bin"

echo "Enabling Flutter Web..."
flutter config --enable-web

echo "Generating missing Web Platform files..."
flutter create . --platforms web

echo "Fetching dependencies..."
flutter pub get

echo "Building the web app..."
flutter build web --release

echo "Build complete!"
