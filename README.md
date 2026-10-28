Estudio de caso: uso y costo de la IA en estudiantes y profesionales

Análisis con las seis fases de Google Data Analytics (Preguntar, Preparar, Procesar, Analizar, Compartir, Actuar).

Contenido
informe_estudio_de_caso.docx: informe completo.
datos_limpios.csv: base limpia con variables nuevas.
codigo/limpieza.py: limpieza y normalización.
codigo/graficos.py: tablas y gráficos.
graficos/: 13 gráficos en PNG.
Cómo reproducir

Colocar AI_Usage_and_Impact_on_Students_and_Professionals.csv en la carpeta de trabajo y ejecutar, en orden:

python codigo/limpieza.py
python codigo/graficos.py

Requiere pandas, numpy y matplotlib. graficos.py escribe tablas auxiliares en la carpeta actual.# Estudio-de-Caso-para-Coursera-Google-
Generación de un estudio de caso correspondiente al proyecto final del Curso Analista de Datos Google
En este Proyecto Final se ha utilizado la siguiente información para crear el estudio de caso.
Uso de la IA e impacto en estudiantes y profesionales - Eisha Tuz Zuhra (Owner)

Sources
The AI Usage and Impact on Students & Professionals dataset was developed using a synthetic
data-generation methodology for educational and Data Science purposes. Instead of collecting personal
information from real individuals, realistic records were generated to represent different types of students 
and professionals and their interaction with Artificial Intelligence tools. The dataset was designed around 
common AI-use scenarios, including education, coding, research, writing, data analysis, content creation, 
office work, and other professional activities.

Collection Methodology
The data structure was designed to include demographic, educational, professional, financial, AI-usage, 
and impact-related variables. Users were represented across different age groups, countries, education 
levels, professions, and income ranges. Information about AI tools, frequency of use, purpose of use, 
AI experience, monthly cost, productivity, accuracy, satisfaction, and time saved was then incorporated 
to create a realistic representation of AI adoption. To make the dataset suitable for data-cleaning and 
preprocessing practice, several realistic data-quality conditions were included, such as missing values, 
duplicate records, inconsistent categorical formats, and numerical values represented in different formats. 
These imperfections allow students to practice identifying and correcting common problems found in real-world datasets. 
The final dataset is intended for academic and practical learning, particularly for Data Inspection, 
Data Cleaning, Exploratory Data Analysis (EDA), Feature Engineering, Data Visualization, Correlation Analysis, 
and Machine Learning. Because the dataset is synthetic, it should not be interpreted as a statistically representative 
survey of actual students or professionals.

Licencia
CC0: Dominio público
