# -*- coding: utf-8 -*-
with open("frontend/src/components/InstallAppButton.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { Smartphone, Download, Check } from 'lucide-react';

export const InstallAppButton = ({ isCollapsed = false }) => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    const handler = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };

    window.addEventListener('beforeinstallprompt', handler);

    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }

    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) {
      alert("To install this app on your phone: Tap your browser's menu (3 dots or share icon) and select 'Add to Home Screen' or 'Install App'.");
      return;
    }

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === 'accepted') {
      setIsInstalled(true);
      setDeferredPrompt(null);
    }
  };

  if (isInstalled) {
    return (
      <div className={`p-2 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold flex items-center ${isCollapsed ? 'justify-center' : 'gap-2'}`}>
        <Check className="w-4 h-4 text-emerald-600 shrink-0" />
        {!isCollapsed && <span>App Installed</span>}
      </div>
    );
  }

  return (
    <button
      onClick={handleInstallClick}
      title="Install Mobile App"
      className={`w-full py-2.5 px-3 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold text-xs shadow-md shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-500 transition-all flex items-center justify-center gap-2 ${
        isCollapsed ? 'p-2.5' : ''
      }`}
    >
      <Smartphone className="w-4 h-4 shrink-0" />
      {!isCollapsed && <span>Install App (APK/PWA)</span>}
    </button>
  );
};
""")
print("Created InstallAppButton.jsx")
