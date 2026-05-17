# Ruiz Assistant para Android

Esta carpeta contiene el proyecto Kivy para crear una versión de Ruiz que funcione en tu celular Android.

## Archivos principales

- `main.py` — código de la aplicación Android.
- `buildozer.spec` — configuración para generar el APK.

## Cómo construir la APK

### Opción recomendada: Linux / WSL

1. Instala Buildozer y dependencias en Linux o WSL.
2. Abre terminal en `android_app`.
3. Ejecuta:
   ```bash
   buildozer android debug
   ```
4. El APK se generará en `bin/`.

### Si no tienes Linux

Puedes usar WSL en Windows:

1. Instala WSL y una distribución Linux.
2. Copia el proyecto a WSL o monta la carpeta.
3. Instala `buildozer` y `python3` en Linux.
4. Ejecuta `buildozer android debug`.

## Cómo usar en el celular

1. Copia el APK generado a tu teléfono.
2. Activa la instalación de aplicaciones de fuentes desconocidas.
3. Instala el APK.
4. Abre la app y pulsa en "Escuchar".
5. Di "ey ruiz" seguido del comando.

## Comandos disponibles

- "ey ruiz, ¿qué hora es?"
- "ey ruiz, abre YouTube"
- "ey ruiz, abre WhatsApp"
- "ey ruiz, busca <algo>"
- "ey ruiz, llama a <número>"
- "ey ruiz, envía mensaje a <número>"
