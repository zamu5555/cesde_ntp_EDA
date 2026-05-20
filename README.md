# Instalación — Proyecto Análisis Base de Datos DENGUE

## Pasos

**1. Clonar el repositorio en la consola:**
```bash
git clone https://github.com/zamu5555/cesde_ntp_EDA.git
```

**2. Abrir el proyecto en VSCode.**

**3. Crear el entorno virtual** en una terminal (preferiblemente **Command Prompt**):
```bash
python -m venv .venv
```

**4. Activar el entorno virtual:**

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac / Linux:**
  ```bash
  source venv/bin/activate
  ```

**5. Instalar las dependencias** desde `requirements.txt`:
```bash
pip install -r requirements.txt
```

**6. Ejecutar la aplicación** con Streamlit:
```bash
streamlit run Inicio.py
```