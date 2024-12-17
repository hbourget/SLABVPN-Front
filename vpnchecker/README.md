## URL de base

```
localhost:8000
```

## Endpoints

### 1. **Obtenir le nombre de pays uniques par fournisseurs**

- **URL**: `/api/providers/countries/`
- **Méthode**: `GET`
- **Paramètres de requête**:
  - `months` (optionnel) : Le nombre de mois à considérer pour le comptage des pays par fournisseur. Par défaut, il est de 3 mois s'il n'est pas spécifié.
- **Réponse**:
  - **200 OK** : Une liste des fournisseurs avec le nombre de pays auxquels ils sont associés pendant les derniers `months` mois.
  - **404 Not Found** : Si aucune donnée n'est trouvée.
  - **Exemple de requête**:
    ```
    /api/providers/countries/?months=3
    ```
  - **Exemple de réponse**:
    ```json
    [
      {
        "provider_id": "uuid",
        "provider_name": "Nom du fournisseur",
        "country_count": 5
      }
    ]
    ```

---

### 2. **Obtenir le nombre de serveurs par fournisseurs**

- **URL**: `/api/providers/servers/`
- **Méthode**: `GET`
- **Paramètres de requête**:
  - `months` (optionnel) : Le nombre de mois à considérer pour le comptage des serveurs par fournisseur. Par défaut, il est de 3 mois s'il n'est pas spécifié.
- **Réponse**:
  - **200 OK** : Une liste des fournisseurs avec le nombre de serveurs auxquels ils sont associés pendant les derniers `months` mois.
  - **404 Not Found** : Si aucune donnée n'est trouvée.
  - **Exemple de requête**:
    ```
    /api/providers/servers/?months=3
    ```
  - **Exemple de réponse**:
    ```json
    [
      {
        "provider_id": "uuid",
        "provider_name": "Nom du fournisseur",
        "server_count": 10
      }
    ]
    ```

---

### 3. **Obtenir les enregistrements d'IP entrantes depuis une période donnée**

- **URL**: `/api/in_ips/`
- **Méthode**: `GET`
- **Paramètres de requête**:
  - `ip` (obligatoire) : L'adresse IP à rechercher.
  - `date_since` (obligatoire) : La date à partir de laquelle filtrer les enregistrements.
- **Réponse**:
  - **200 OK** : Une liste des enregistrements filtrés correspondant à l'IP et à la date données.
  - **400 Bad Request** : Si les paramètres `ip` ou `date_since` sont manquants dans les paramètres de la requête.
  - **404 Not Found** : Si aucun enregistrement n'est trouvé.
  - **Exemple de requête**:
    ```
    /api/in_ips/?ip=192.168.1.1&date_since=2024-01-01T00:00:00Z
    ```
  - **Exemple de réponse**:
    ```json
    [
      {
        "id": "uuid",
        "ip": "192.168.1.1",
        "server": {
          "id": "uuid",
          "name": "Nom du serveur",
          "provider": {
            "id": "uuid",
            "name": "Nom du fournisseur"
          },
          "location_type": "City",
          "city_name": "Nom de la ville",
          "country_name": "Nom du pays"
        },
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
      }
    ]
    ```

---

### 4. **Obtenir les enregistrements d'IP sortantes depuis une période donnée**

- **URL**: `/api/out_ips/`
- **Méthode**: `GET`
- **Paramètres de requête**:
  - `ip` (obligatoire) : L'adresse IP à rechercher.
  - `date_since` (obligatoire) : La date à partir de laquelle filtrer les enregistrements.
- **Réponse**:
  - **200 OK** : Une liste des enregistrements filtrés correspondant à l'IP et à la date données.
  - **400 Bad Request** : Si les paramètres `ip` ou `date_since` sont manquants dans les paramètres de la requête.
  - **404 Not Found** : Si aucun enregistrement n'est trouvé.
  - **Exemple de requête**:
    ```
    /api/out_ips/?ip=192.168.1.1&date_since=2024-01-01T00:00:00Z
    ```
  - **Exemple de réponse**:
    ```json
    [
      {
        "id": "uuid",
        "ip": "192.168.1.1",
        "server": {
          "id": "uuid",
          "name": "Nom du serveur",
          "provider": {
            "id": "uuid",
            "name": "Nom du fournisseur"
          },
          "location_type": "City",
          "city_name": "Nom de la ville",
          "country_name": "Nom du pays"
        },
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
      }
    ]
    ```