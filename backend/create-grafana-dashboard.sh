#!/bin/bash

# Grafana URL
GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASSWORD="admin228"

# Создаём datasource с TestData
echo "Создаём TestData datasource..."
curl -X POST $GRAFANA_URL/api/datasources \
  -H "Content-Type: application/json" \
  -u $GRAFANA_USER:$GRAFANA_PASSWORD \
  -d '{
    "name": "TestData",
    "type": "testdata",
    "access": "proxy",
    "isDefault": true
  }' 2>/dev/null

echo ""
echo "Создаём дашборд с графиками..."

# Дашборд JSON
DASHBOARD_JSON='{
  "dashboard": {
    "title": "Bank Comparison",
    "description": "Сравнение банков - demo данные",
    "timezone": "browser",
    "panels": [
      {
        "type": "graph",
        "title": "Interest Rates Trend",
        "targets": [
          {
            "refId": "A",
            "scenarioId": "random_walk"
          }
        ],
        "gridPos": {
          "x": 0,
          "y": 0,
          "w": 12,
          "h": 8
        }
      },
      {
        "type": "stat",
        "title": "Sberbank Rate",
        "targets": [
          {
            "refId": "A",
            "scenarioId": "random_walk"
          }
        ],
        "gridPos": {
          "x": 12,
          "y": 0,
          "w": 6,
          "h": 4
        }
      },
      {
        "type": "stat",
        "title": "VTB Rate",
        "targets": [
          {
            "refId": "A",
            "scenarioId": "random_walk"
          }
        ],
        "gridPos": {
          "x": 18,
          "y": 0,
          "w": 6,
          "h": 4
        }
      },
      {
        "type": "stat",
        "title": "Alfa Rate",
        "targets": [
          {
            "refId": "A",
            "scenarioId": "random_walk"
          }
        ],
        "gridPos": {
          "x": 12,
          "y": 4,
          "w": 6,
          "h": 4
        }
      },
      {
        "type": "stat",
        "title": "UralSib Rate",
        "targets": [
          {
            "refId": "A",
            "scenarioId": "random_walk"
          }
        ],
        "gridPos": {
          "x": 18,
          "y": 4,
          "w": 6,
          "h": 4
        }
      },
      {
        "type": "graph",
        "title": "Commissions Comparison",
        "targets": [
          {
            "refId": "A",
            "scenarioId": "random_walk"
          }
        ],
        "gridPos": {
          "x": 0,
          "y": 8,
          "w": 12,
          "h": 8
        }
      }
    ],
    "schemaVersion": 27,
    "version": 0,
    "refresh": "10s",
    "time": {
      "from": "now-6h",
      "to": "now"
    }
  },
  "overwrite": true
}'

# Загружаем дашборд
curl -X POST $GRAFANA_URL/api/dashboards/db \
  -H "Content-Type: application/json" \
  -u $GRAFANA_USER:$GRAFANA_PASSWORD \
  -d "$DASHBOARD_JSON" 2>/dev/null | jq .

echo "✅ Дашборд создан!"
