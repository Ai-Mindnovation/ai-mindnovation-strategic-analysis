# Informe Interno de Seguridad  
## Plataforma de Análisis Empresarial (MVP Odoo)

---

## 1. Contexto General del Proyecto

El proyecto busca desarrollar una **plataforma para el análisis financiero, de costos, flujo de caja y prospectiva empresarial**, usando **Odoo Community** como framework principal.  

El sistema permite que los clientes suban archivos (documentos financieros, reportes, planillas, etc.) y obtengan resultados analíticos a partir de módulos internos desarrollados en Python.  
El cliente final **no interactúa directamente con Odoo**, sino a través de un **portal web** personalizado, donde carga sus documentos y recibe los reportes.

Actualmente, el proyecto se encuentra en fase de **MVP (producto mínimo viable)**, desplegado en infraestructura propia alojada en **Hetzner**, y se planea evolucionar hacia un entorno más seguro, modular y escalable.

---

## 2. Arquitectura Actual

**Infraestructura:**
- Despliegue basado en **contenedores Docker**.
- Servicios principales:
  - `odoo`: núcleo de la aplicación (Odoo Community).
  - `postgres`: base de datos principal.
  - `nginx`: ejecutándose en un servidor bastión externo, actuando como **proxy inverso** y punto de entrada HTTPS.
- Almacenamiento de archivos: actualmente en el **filesystem del servidor Odoo**.
- Comunicación interna: red Docker estándar (`bridge`).
- Autenticación de usuarios: nativa de Odoo (portal).
- Certificado SSL activo en el proxy inverso (HTTPS público).

**Procesamiento y análisis:**
- Módulos Python internos dentro de Odoo para realizar los análisis.
- Se prevé integrar servicios externos o locales (OCR, IA, modelos de análisis, etc.) a través de API o contenedores adicionales.

**Naturaleza de los datos:**
- Archivos subidos pueden contener información **financiera, estratégica o personal**.
- No existen requerimientos normativos explícitos aún, pero se prevé cumplir con principios de **Habeas Data / GDPR / ISO 27001** a futuro.

---

## 3. Riesgos Identificados

### 3.1. Archivos sensibles sin cifrado ni aislamiento
- Los documentos se almacenan sin cifrado en el filesystem.
- No hay segregación por cliente (riesgo de exposición cruzada entre usuarios).
- Permisos de acceso dependientes del sistema operativo, no del modelo de seguridad de Odoo.

### 3.2. Falta de control de auditoría e integridad
- No hay registro formal de las acciones de subida, descarga o eliminación.
- No se registran cambios ni acceso a los documentos, dificultando trazabilidad.

### 3.3. Gestión de secretos y credenciales
- Variables sensibles (DB, API keys, tokens) probablemente almacenadas en archivos `.env` sin cifrado ni gestor de secretos.
- Riesgo de exposición en caso de fuga del repositorio o acceso no autorizado al host.

### 3.4. Comunicación interna sin cifrar
- Posible conexión entre Odoo ↔ PostgreSQL sin TLS.
- La red Docker actual (`bridge`) no garantiza segmentación ni aislamiento frente a otros contenedores.

### 3.5. Cumplimiento y retención de datos
- No hay política de retención o eliminación segura.
- Los datos personales o financieros no tienen un ciclo de vida definido.
- Ausencia de cifrado en reposo y en backups.

### 3.6. Riesgo de exposición en el portal Odoo
- Posibles vistas o menús estándar habilitados innecesariamente.
- Falta de validaciones adicionales en el portal puede permitir filtrado o acceso cruzado de registros.

### 3.7. Monitoreo y respuesta a incidentes limitada
- Logs locales sin centralización.
- Sin sistema de alertas de acceso o error.
- No existen controles de detección temprana de anomalías.

---

## 4. Evaluación de Riesgo

| Riesgo | Impacto | Probabilidad | Nivel |
|--------|----------|--------------|--------|
| Archivos sensibles sin cifrado | Alto | Alta | **Crítico** |
| Falta de auditoría | Alto | Media | **Alto** |
| Gestión de secretos deficiente | Alto | Media | **Alto** |
| Comunicación interna sin TLS | Medio | Media | **Moderado** |
| Retención y borrado de datos indefinido | Medio | Media | **Moderado** |
| Exposición en portal Odoo | Alto | Media | **Alto** |
| Monitoreo insuficiente | Medio | Alta | **Alto** |

---

## 5. Plan de Mejora y Endurecimiento

### **Fase 1 – Endurecimiento del MVP (Corto Plazo)**

**Objetivo:** Garantizar una base segura para operar el MVP sin riesgos críticos.

1. **Aislamiento de datos por cliente**
   - Implementar `record rules` y `ir.rules` para restringir acceso a registros por cliente.
   - Estructurar el almacenamiento físico por cliente: `/data/odoo/storage/<cliente_id>/`.
   - Asignar permisos 700 a cada directorio.

2. **Cifrado de archivos en reposo**
   - Cifrar archivos antes de guardarlos (librería `cryptography` o `fernet`).
   - Alternativa: migrar el almacenamiento a **S3** o **MinIO** con cifrado SSE/KMS.

3. **TLS interno y segmentación**
   - Activar conexión TLS en PostgreSQL (`sslmode=require`).
   - Configurar red Docker interna exclusiva entre Odoo y Postgres.
   - Asegurar acceso a la base de datos solo desde el contenedor Odoo.

4. **Gestión de secretos**
   - Eliminar claves del código y `.env` públicos.
   - Centralizar en gestor de secretos (Vault, Doppler o AWS Secrets Manager).

5. **Auditoría y trazabilidad**
   - Instalar módulo `auditlog` o similar.
   - Registrar subida, descarga, análisis y eliminación de archivos.
   - Retener logs por al menos 90 días.

6. **Fortalecimiento del portal**
   - Revisar vistas y accesos del módulo `portal`.
   - Eliminar menús estándar no usados.
   - Aplicar validaciones adicionales a controladores de subida.

---

### **Fase 2 – Confiabilidad y Cumplimiento (Mediano Plazo)**

**Objetivo:** Avanzar hacia cumplimiento normativo y estándares empresariales.

1. **Backups y recuperación**
   - Implementar backups automáticos de base de datos y archivos cifrados.
   - Almacenamiento externo (Hetzner Storage Box / S3).
   - Pruebas de restauración documentadas.

2. **Política de seguridad documentada**
   - Redactar “Política de Seguridad y Privacidad de Datos”.
   - Definir ciclo de vida de los datos (retención, anonimización, eliminación).

3. **Autenticación avanzada**
   - Habilitar 2FA en el portal (módulo Odoo o integración con Auth0/Keycloak).
   - Políticas de contraseñas seguras y rotación periódica.

4. **Monitoreo y alertas**
   - Centralizar logs (Loki, Grafana, Graylog).
   - Configurar alertas para:
     - Errores HTTP 500 repetidos.
     - Intentos de login fallidos.
     - Accesos desde IPs inusuales.

5. **Pruebas de penetración**
   - Ejecutar escaneo OWASP ZAP o Nikto.
   - Validar cabeceras de seguridad (CSP, X-Frame-Options, etc.).
   - Revisar dependencias Odoo y módulos instalados.

---

## 6. Buenas Prácticas Operativas

- **Mantenimiento periódico**
  - Actualizar contenedores y dependencias mensualmente.
  - Revisar logs de seguridad y accesos.
  - Monitorear consumo y rendimiento de la base de datos.

- **Gestión de usuarios**
  - Principio de privilegio mínimo: cada usuario solo accede a sus datos.
  - Deshabilitar cuentas inactivas automáticamente.

- **Gestión de vulnerabilidades**
  - Auditorías trimestrales de configuración.
  - Escaneo de imágenes Docker con `trivy` o `grype`.

- **Transparencia y documentación**
  - Mantener registro actualizado de cambios de infraestructura.
  - Documentar incidentes y respuestas.

---

## 7. Próximos Pasos y Seguimiento

1. Implementar los controles de **Fase 1** antes del despliegue del MVP.  
2. Diseñar la **arquitectura segura definitiva** considerando almacenamiento externo y gestión de secretos.  
3. Redactar la **versión pública del informe de seguridad** para presentación al cliente.  
4. Planificar revisiones de seguridad trimestrales.

---

**Documento interno – Confidencial**  
El presente informe es de uso exclusivo del equipo de desarrollo y dirección técnica.  
No debe compartirse externamente ni reproducirse sin autorización.
