# VISIÓN VENEZUELA

Sitio informativo estático, gratuito y preparado para **GitHub Pages**.

No requiere servidor, base de datos, Node.js, npm, Docker ni APIs. Los textos de cada área son **provisionales**: no representan propuestas políticas detalladas aprobadas, ni documentos jurídicos oficiales.

## 1. Publicar gratis en GitHub Pages

### Crear el repositorio

1. Entra a https://github.com/new e inicia sesión.
2. Repositorio: `Visi-n-Venezuela` (puedes escoger otro).
3. Elige **Public** para usar GitHub Pages en GitHub Free.
4. **No marques** «Add a README file» ni añadas `.gitignore` o licencia en este paso: ya están incluidos los archivos del sitio.
5. Crea el repositorio.

### Subir el sitio en Windows

Descarga el ZIP del sitio y **extrae su contenido** en una carpeta de Windows. Debes ver `index.html`, `assets`, `gobierno`, `leyes`, etc. en esa carpeta.

Desde PowerShell, ubicado dentro de esa carpeta:

```powershell
git init
git branch -M main
git add .
git commit -m "Publicar primera versión de Visión Venezuela"
git remote add origin https://github.com/HerroldB/Visi-n-Venezuela.git
git push -u origin main
```

Reemplaza `TU_USUARIO` por tu usuario de GitHub y `vision-venezuela` por el nombre real del repositorio. Si GitHub solicita autorización, autentícate desde el navegador. Puedes hacer lo mismo con GitHub Desktop si prefieres interfaz gráfica.

### Activar GitHub Pages

1. En el repositorio, abre **Settings → Pages**.
2. En **Build and deployment → Source** selecciona **Deploy from a branch**.
3. Selecciona **main** y la carpeta **/(root)**; presiona **Save**.
4. Abre el enlace **Visit site** cuando se publique.

Ejemplo de URL, que no existe hasta que publiques: `https://HerroldB.github.io/Visi-n-Venezuela/`.

**Nota:** GitHub Pages en la cuenta gratuita exige un repositorio público; **todo** lo que subas al repositorio es visible para terceros.

## 2. Cambiar título, secciones, textos y PDF

El archivo editable principal es `content/site.json`.

- `site_name`: nombre del proyecto (actualmente «VISIÓN VENEZUELA»).
- `sections`: menús, categorías y descripción inicial de cada página.
- `overrides`: contenido personalizado de páginas individuales.
- `faq`: preguntas frecuentes.

Después de cualquier cambio en ese JSON, ejecuta:

```powershell
python build.py
```

Esto regenera las páginas HTML y mantiene los enlaces correctos aunque GitHub Pages esté en un subdirectorio (`TU_USUARIO.github.io/REPOSITORIO/`). No necesitas instalar librerías de Python.

### Publicar un PDF y fotografías

1. Crea la carpeta `docs` y coloca allí el PDF, por ejemplo `docs/reforma-educativa.pdf`.
2. Crea la carpeta `images` y coloca allí las fotografías, por ejemplo `images/escuela.jpg`.
3. Agrega un bloque en la propiedad `overrides` de `content/site.json`. Ejemplo:

```json
"overrides": {
  "leyes/educacion": {
    "status": "Borrador publicado",
    "updated": "2026-11-09",
    "summary": "Aquí se describe el proyecto en lenguaje sencillo y con precisión.",
    "focus": [
      "Diagnóstico de la situación actual",
      "Contenido de la propuesta",
      "Etapas de implementación"
    ],
    "pdf": "docs/reforma-educativa.pdf",
    "images": [
      {
        "src": "images/escuela.jpg",
        "alt": "Descripción de lo que muestra la fotografía",
        "caption": "Fotografía referencial con su fuente y autorización de uso"
      }
    ]
  }
}
```

La propiedad `overrides` ya está creada y vacía: **reemplázala** por el objeto anterior, no añadas otra clave duplicada. Usa rutas relativas al inicio del proyecto, sin `/` inicial.

Después ejecuta `python build.py`, confirma que se creó `leyes/educacion/index.html`, añade al repositorio el PDF, las imágenes y todos los HTML actualizados y ejecuta:

```powershell
git add .
git commit -m "Añadir proyecto de educación"
git push
```

En la web, el PDF se mostrará dentro de su página y tendrá enlaces para abrirlo o descargarlo. Los visores PDF dependen del navegador del visitante; siempre habrá un enlace directo alternativo.

### Cambiar imágenes

Las áreas de fotografías son marcadores de posición. **No se incluyen fotografías externas ni se presupone que puedes utilizarlas sin licencia.** Utiliza imágenes propias o imágenes con permisos compatibles; documenta su atribución en el propio expediente.

## 3. Previsualizar localmente

Desde PowerShell dentro de la carpeta del proyecto:

```powershell
python -m http.server 8000
```

Abre `http://localhost:8000/` en el navegador. Finaliza el servidor con `Ctrl+C`.

## 4. Estructura

- `index.html`: inicio.
- `faq/index.html`: preguntas frecuentes.
- `gobierno/*`, `leyes/*`, `proyectos/*`, `objetivos/*`: páginas individuales.
- `assets/styles.css`: colores, tipografía, disposición y respuesta móvil.
- `assets/app.js`: navegación móvil y menús desplegables.
- `assets/favicon.svg`: icono del navegador.
- `content/site.json`: datos editables del sitio.
- `build.py`: generador de todas las páginas con Python estándar.
- `.nojekyll`: evita que GitHub Pages aplique Jekyll sobre archivos estáticos.

## 5. Estado y límites

- Sitio preparado para alojamiento estático, no desplegado automáticamente.
- No contiene backend ni formularios de contacto (mantiene el sitio simple y gratuito).
- No contiene propuestas legislativas redactadas ni PDFs adjuntos todavía.
- La clasificación de leyes es una estructura de navegación inicial; **no es un censo exhaustivo del ordenamiento jurídico venezolano**.
- Tipografía: Helvetica Neue / Helvetica / Arial según disponibilidad del dispositivo; Aribau Grotesk no se incluye porque requiere disponer legalmente de la fuente.
- El sitio presenta una visión política independiente, no una institución del Estado.

