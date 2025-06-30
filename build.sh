#!/usr/bin/env bash

# Instala los navegadores requeridos por Playwright
echo "📦 Instalando navegadores de Playwright..."
npx playwright install --with-deps

# Confirmación de instalación
echo "✅ Playwright y navegadores instalados correctamente"
