# Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ DEVICE : owns
    USER ||--o{ ACCESS_SESSION : initiates
    DEVICE ||--o{ TELEMETRY_EVENT : emits
    DEVICE ||--o{ DETECTION_CASE : participates_in
    ACCESS_POLICY ||--o{ ACCESS_DECISION : governs
    ACCESS_SESSION ||--|| ACCESS_DECISION : evaluates
    TELEMETRY_EVENT ||--o{ DETECTION_CASE : contributes_to
    DETECTION_CASE ||--o{ INDICATOR : references
    DETECTION_CASE ||--o{ EVIDENCE_RECORD : produces
    INVESTIGATION ||--o{ EVIDENCE_RECORD : contains
    THREAT_FEED ||--o{ INDICATOR : supplies

    USER {
        uuid id PK
        string subject
        string email
        string tenant_id
        boolean mfa_enforced
    }

    DEVICE {
        uuid id PK
        uuid user_id FK
        string device_id
        string os
        string posture_state
        string certificate_thumbprint
    }

    ACCESS_POLICY {
        uuid id PK
        string name
        string effect
        json rules
        boolean active
    }

    ACCESS_SESSION {
        uuid id PK
        uuid user_id FK
        uuid device_id FK
        string source_ip
        string target_asset
        datetime started_at
        datetime ended_at
        string decision_state
    }

    ACCESS_DECISION {
        uuid id PK
        uuid session_id FK
        uuid policy_id FK
        string outcome
        float risk_score
        datetime decided_at
    }

    TELEMETRY_EVENT {
        uuid id PK
        uuid device_id FK
        string event_type
        json payload
        datetime occurred_at
    }

    DETECTION_CASE {
        uuid id PK
        uuid device_id FK
        string severity
        string status
        string detection_type
        float confidence
        datetime created_at
    }

    INDICATOR {
        uuid id PK
        uuid detection_case_id FK
        uuid threat_feed_id FK
        string indicator_type
        string value
        string privacy_class
        datetime observed_at
    }

    THREAT_FEED {
        uuid id PK
        string provider_name
        string sharing_mode
        string trust_level
    }

    EVIDENCE_RECORD {
        uuid id PK
        uuid detection_case_id FK
        uuid investigation_id FK
        string hash
        string storage_uri
        string chain_ref
        datetime recorded_at
    }

    INVESTIGATION {
        uuid id PK
        string case_id
        string owner
        string status
        datetime opened_at
    }
```

## Relationships summary

- A user may own multiple devices.
- A device emits telemetry and participates in detections.
- Access sessions are evaluated against policies and yield decisions.
- Telemetry contributes to detection cases.
- Detection cases produce indicators and evidence.
- Evidence records are grouped into investigations and anchored to a ledger.
