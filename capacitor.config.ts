import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.medsathi.app',
  appName: 'Medsathi',
  webDir: 'www',
  // Teal matches the branded splash screen and adaptive launcher icon.
  backgroundColor: '#005264',
  plugins: {
    LocalNotifications: {
      iconColor: '#005264'
    }
  }
};

export default config;
