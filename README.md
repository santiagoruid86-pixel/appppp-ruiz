# Ruiz - Asistente de voz

Este proyecto crea un asistente de voz activado por la frase "ey ruiz". El asistente responde con voz y puede ejecutar comandos básicos en Windows. Además, incluye funciones para controlar un teléfono Android conectado mediante ADB.

## Características

- Detección de la frase de activación: "ey ruiz"
- Respuestas habladas con voz de asistente
- Comandos básicos:
  - "¿Qué hora es?"
  - "abre YouTube"
  - "busca <algo>"
  - "llama a <número>" (requiere teléfono Android conectado y `adb`)
  - "abre WhatsApp" en el teléfono Android conectado
- Ejecución como aplicación descargable con PyInstaller

## Requisitos

- Windows 10 o 11
- Python 3.9+
- Micrófono
- Opcional: teléfono Android con USB debugging habilitado y `adb`

## Instalación

1. Abre PowerShell en la carpeta del proyecto.
2. Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
python -m pip install pipwin
python -m pipwin install pyaudio
```

3. Si vas a controlar un teléfono Android, instala `adb` y conéctalo al equipo.

## Uso

```powershell
python Ruiz.py
```

Di "ey ruiz" y luego el comando.

## Crear archivo ejecutable

Instala PyInstaller:

```powershell
python -m pip install pyinstaller
```

Genera el ejecutable:

```powershell
python -m pyinstaller --onefile --noconsole Ruiz.py
```

El ejecutable estará en `dist\Ruiz.exe`.

## App Android

Si quieres una versión para instalar en tu celular Android, en la carpeta `android_app/` hay un proyecto Kivy listo para generar un APK.

- `android_app/main.py` contiene el código de la app.
- `android_app/buildozer.spec` contiene la configuración para Buildozer.
- `android_app/README.md` explica cómo crear la APK y probarla en el teléfono.

> Nota: crear el APK en Windows requiere usar WSL o un entorno Linux con Buildozer.

## Subir el proyecto a GitHub

1) Crea un repositorio nuevo en GitHub.
2) En tu carpeta `app_celular`, ejecuta:

```powershell
cd c:\Users\Kiara\Downloads\app_celular
git init
git add .
git commit -m "Añadir Ruiz asistente y proyecto Android"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git
git push -u origin main
```

3) Reemplaza `TU_USUARIO` y `NOMBRE_DEL_REPO` por los tuyos.

### Qué subir a GitHub

- El código `Ruiz.py`
- La carpeta `android_app/` con `main.py` y `buildozer.spec`
- `README.md` y `requirements.txt`
- `.gitignore` para no subir archivos temporales

## Importante

Subirlo a GitHub te permite compartir el proyecto, pero no convierte el código automáticamente en una app instalable. Si quieres, también puedo decirte cómo crear un release con el APK una vez generado.
