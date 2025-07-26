const fs = require('fs');
const path = require('path');

// Create out directory
const outDir = path.join(__dirname, 'out');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

// Copy static files from .next/server/pages to out
const srcDir = path.join(__dirname, '.next/server/pages');
const staticDir = path.join(__dirname, '.next/static');

function copyRecursive(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach(child => {
      copyRecursive(path.join(src, child), path.join(dest, child));
    });
  } else {
    // For HTML files, copy with directory structure
    if (src.endsWith('.html')) {
      const dir = path.dirname(dest);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.copyFileSync(src, dest);
    }
  }
}

// Copy HTML files
copyRecursive(srcDir, outDir);

// Copy static assets
const staticOutDir = path.join(outDir, '_next/static');
if (fs.existsSync(staticDir)) {
  copyRecursive(staticDir, staticOutDir);
}

// Copy public files
const publicDir = path.join(__dirname, 'public');
if (fs.existsSync(publicDir)) {
  fs.readdirSync(publicDir).forEach(file => {
    if (file !== 'index.html' && file !== '_redirects') {
      const src = path.join(publicDir, file);
      const dest = path.join(outDir, file);
      if (fs.statSync(src).isFile()) {
        fs.copyFileSync(src, dest);
      }
    }
  });
}

console.log('Static export completed to:', outDir);