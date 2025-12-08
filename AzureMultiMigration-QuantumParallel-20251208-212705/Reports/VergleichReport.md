# Azure Migration Vergleich Report (2025-Quantum-Parallel Edition)

## Az.Tools.Migration Cmdlets Erklärung
- **New-AzUpgradeModulePlan**: Plant Migration, analysiert Cmdlets/Params, Tabelle mit Locations.
- **Invoke-AzUpgradeModulePlan**: Führt aus, neue Dateien mit _az_upgraded.
- **Set-AzToolsMigrationTelemetry**: Metrics.

## Vergleichstabelle
| Aspekt | PowerShell | Azure CLI | Python SDK |
|--------|------------|-----------|------------|
| Automatisierung | Hoch | Mittel | Niedrig |
| Updates | Az 15.1.0 | CLI 2.75+ | Mgmt v12+ |

Generiert: 12/08/2025 21:27:09
