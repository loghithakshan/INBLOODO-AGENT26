# 📱 INBLOODO MOBILE APP - SETUP GUIDE

**Status**: React Native app ready for iOS & Android  
**Framework**: Expo (easiest for cross-platform)

---

## 🚀 QUICK START

### **1. Prerequisites**
```bash
# Install Node.js (14+)
# Download: nodejs.org

# Install Expo CLI
npm install -g expo-cli

# Verify installation
expo --version
node --version
npm --version
```

### **2. Setup Project**
```bash
# Navigate to mobile directory
cd blood\ report\ ai/mobile

# Install dependencies
npm install

# Optional: Install Expo Go app on phone for live preview
# iOS: App Store
# Android: Google Play Store
```

### **3. Run the App**

**For Testing (Live Preview)**:
```bash
# Start development server
npm start

# Scan QR code with Expo Go app
# On Windows: Press 'w' for web preview
# On Mac/Linux: Press 'i' for iOS or 'a' for Android
```

**For Android Phone**:
```bash
npm run android
# Make sure Android emulator is running or USB connected
```

**For iOS (Mac Only)**:
```bash
npm run ios
# Requires Xcode installed
```

**For Web Browser**:
```bash
npm run web
# Opens at http://localhost:19006
```

---

## 🏗️ PROJECT STRUCTURE

```
mobile/
├── App.js               # Entry point
├── InbloodoApp.jsx      # Main app component
├── package.json         # Dependencies
├── app.json            # Expo configuration
├── babel.config.js     # Babel configuration
├── screens/             # (Optional) Navigation screens
│   ├── HomeScreen.js
│   ├── AnalysisScreen.js
│   └── ResultsScreen.js
├── components/          # (Optional) Reusable components
│   ├── UploadButton.js
│   └── ResultsDisplay.js
└── assets/              # Images, fonts, etc.
    ├── icon.png
    └── splash.png
```

---

## 🔧 CONFIGURATION

### **app.json** (Expo Configuration)
```json
{
  "expo": {
    "name": "INBLOODO",
    "slug": "inbloodo",
    "version": "2.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#1f4788"
    },
    "plugins": [
      [
        "expo-camera",
        {
          "cameraPermission": "Allow INBLOODO to access your camera"
        }
      ]
    ],
    "ios": {
      "supportsTabletMode": true,
      "bundleIdentifier": "com.inbloodo.health"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/icon.png",
        "backgroundColor": "#1f4788"
      },
      "package": "com.inbloodo.health"
    }
  }
}
```

---

## 📦 BUILD & DEPLOY

### **Build APK (Android)**

**Step 1: Create EAS Account**
```bash
npm install -g eas-cli
eas login
```

**Step 2: Configure Project**
```bash
eas build:configure
```

**Step 3: Build APK**
```bash
# Development APK (instant testing)
eas build -p android --profile preview

# Production APK (for Play Store)
eas build -p android --profile production

# Download APK and install on phone
adb install app-release.apk
```

### **Build IPA (iOS)**

```bash
# Build for TestFlight/AppStore
eas build -p ios --profile production

# Install on simulator
eas build -p ios --profile preview
```

### **Submit to Play Store**

**Prerequisites**:
- Google Play Developer Account ($25 one-time)
- App signing certificate

**Steps**:
```bash
# Configure for Play Store
eas submit -p android --latest

# Or manually upload APK to Play Console
# https://play.google.com/console
```

### **Submit to App Store**

**Prerequisites**:
- Apple Developer Account ($99/year)
- Mac with Xcode

**Steps**:
```bash
# Build and submit
eas submit -p ios --latest

# Or manual TestFlight distribution
# https://appstoreconnect.apple.com
```

---

## 🎨 CUSTOMIZATION

### **Change App Theme**
Edit `InbloodoApp.jsx` colors:
```javascript
// Primary color (header, buttons)
primaryButton: {
  backgroundColor: '#1f4788',  // Change here
}

// Secondary color
secondaryButton: {
  backgroundColor: '#3b6aa0',  // Change here
}
```

### **Update App Icons**

1. Generate icons (1024x1024 PNG):
   - https://www.adobe.com/express/create/icon
   - https://appicon.co

2. Place in `assets/`:
   ```bash
   cp your-icon.png assets/icon.png
   cp your-splash.png assets/splash.png
   ```

3. Update `app.json`:
   ```json
   "icon": "./assets/icon.png",
   "splash": {
     "image": "./assets/splash.png"
   }
   ```

### **Add Screen Navigation**

```javascript
// Install React Navigation
npm install @react-navigation/native @react-navigation/bottom-tabs

// Create screens directory
mkdir screens

// Add AnalysisScreen.js, ResultsScreen.js, etc.
// Update App.js to use NavigationContainer
```

---

## 🔌 API INTEGRATION

### **Connect to Backend**

The app is preconfigured to connect to:
```
🌍 PUBLIC: https://impalpable-perspectively-andria.ngrok-free.dev
🏠 LOCAL: http://localhost:8000
```

Edit API URL in `InbloodoApp.jsx`:
```javascript
const API_URL = 'https://your-domain.com';  // Change here
```

### **Authentication** (Optional)

Add API key:
```javascript
const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': 'your-api-key-here'  // Add if required
};

await axios.post(url, data, { headers });
```

---

## 🧪 TESTING

### **Unit Tests**
```bash
npm test

# Create __tests__/InbloodoApp.test.js
```

### **Device Testing**

**Real Device**:
1. Install Expo Go app (iOS/Android)
2. Run: `npm start`
3. Scan QR code with phone
4. Test on actual device

**Emulator**:
```bash
# Android Emulator
npm run android

# iOS Simulator (Mac only)
npm run ios
```

---

## 📊 PERFORMANCE OPTIMIZATION

### **Image Optimization**
```javascript
// Use React Native FastImage for better caching
npm install react-native-fast-image

// In component
<FastImage
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  cache={FastImage.cacheControl.immutable}
/>
```

### **List Optimization**
```javascript
// Use FlatList for large lists
<FlatList
  data={recommendations}
  renderItem={({ item }) => <Text>{item}</Text>}
  keyExtractor={(item, index) => index.toString()}
/>
```

### **Lazy Loading**
```javascript
// Load components on demand
const ResultsScreen = React.lazy(() => import('./screens/ResultsScreen'));
```

---

## 🚀 ADVANCED FEATURES TO ADD

### **1. Offline Support**
```bash
npm install @react-native-async-storage/async-storage

// Cache analysis results locally
AsyncStorage.setItem('analysis', JSON.stringify(data));
```

### **2. Push Notifications**
```bash
npm install expo-notifications

// Send notifications for report completion
await Notifications.scheduleNotificationAsync({
  content: {
    title: 'Analysis Complete',
    body: 'Your report is ready!'
  },
  trigger: { seconds: 2 }
});
```

### **3. Dark Mode**
```javascript
import { useColorScheme } from 'react-native';

const colorScheme = useColorScheme();
const isDarkMode = colorScheme === 'dark';
```

### **4. Multi-Language Support**
```bash
npm install react-native-localization

// Translations
const strings = new LocalizedStrings({
  en: { uploadPDF: 'Upload PDF' },
  es: { uploadPDF: 'Cargar PDF' },
  fr: { uploadPDF: 'Télécharger PDF' }
});
```

---

## 📱 DEVICE REQUIREMENTS

### **iOS**
- iOS 14.0+
- iPhone, iPad

### **Android**
- Android 7.0+ (API 24+)
- Phone, tablet

### **Web**
- Works in all modern browsers
- Chrome, Safari, Firefox

---

## 🐛 TROUBLESHOOTING

### **"Cannot find module"**
```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### **"Permission denied" on Android**
```bash
# Request permissions in AndroidManifest.xml
# Or use expo-permissions

npm install expo-permissions
```

### **"Metro bundler failed"**
```bash
# Kill process and restart
ps aux | grep expo
kill <PID>
npm start --reset-cache
```

### **Slow app performance**
```javascript
// Profile with React DevTools
npm install react-devtools
react-devtools

// Check performance in DevTools menu
```

---

## 📈 DISTRIBUTION CHECKLIST

Before publishing to app stores:

### iOS App Store
- [ ] App name finalized
- [ ] Icon & screenshots ready
- [ ] Description written
- [ ] Privacy policy URL
- [ ] Category selected
- [ ] Age rating completed
- [ ] TestFlight testing done

### Google Play Store
- [ ] App name finalized
- [ ] Icon (512x512) & screenshots
- [ ] Description (80 chars max)
- [ ] Short description
- [ ] Privacy policy URL
- [ ] Content rating
- [ ] Audience testing

---

## 💰 APP STORE COSTS

| Platform | Fee | Duration |
|----------|-----|----------|
| **iOS** | $99/year | Yearly subscription |
| **Android** | $25 | One-time |
| **Both** | $124/year | Recommended |

---

## 📞 USEFUL LINKS

- **Expo Docs**: https://docs.expo.dev
- **React Native**: https://reactnative.dev
- **EAS**: https://eas.expo.dev
- **Play Store**: https://play.google.com/console
- **App Store**: https://appstoreconnect.apple.com

---

## 🎉 LAUNCH CHECKLIST

```
✅ App built and tested locally
✅ API integration verified
✅ Icons and branding finalized
✅ Permissions configured
✅ Performance optimized
✅ Error handling implemented
✅ App store accounts created
✅ Beta testing completed
✅ Privacy policy written
✅ Submitted to stores
✅ Monitoring active
```

---

**Next Steps**:
1. Follow "Quick Start" section above
2. Test app on device
3. Customize branding
4. Build APK/IPA
5. Submit to stores
6. Monitor user feedback

**Questions?** Check Expo documentation or React Native docs!
