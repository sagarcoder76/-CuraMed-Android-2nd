import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.medsathi.app',
  appName: 'Medsathi',
  webDir: 'www',
  backgroundColor: '#f3faff',
  plugins: {
    LocalNotifications: {
      iconColor: '#005264'
    }
  }
};

export default config;
