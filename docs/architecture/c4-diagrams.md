# C4-Style Diagrams

## 1. System Context Diagram

```mermaid
flowchart LR
    User[User / Remote Worker]
    Admin[Security Operator]
    Partner[Trusted Threat Intel Partner]
    Org[Business Application]

    subgraph ZTN[Zero Trust Network Platform]
        IDP[Identity & Access Plane]
        PDP[Policy Decision Engine]
        GATEWAY[ZTNA Gateway / SDP]
        DETECTOR[Behavioral Detection Engine]
        TI[Privacy-Preserving Intel Broker]
        EVIDENCE[Evidence & Ledger Service]
        SIEM[SIEM / SOAR]
    end

    User --> GATEWAY
    Admin --> SIEM
    Partner --> TI
    Org --> GATEWAY
    GATEWAY --> IDP
    GATEWAY --> PDP
    PDP --> DETECTOR
    DETECTOR --> TI
    DETECTOR --> EVIDENCE
    SIEM --> EVIDENCE
```

## 2. Container Diagram

```mermaid
flowchart TB
    subgraph Edge[Edge / Access]
        ZTNA[ZTNA Gateway]
        Agent[Endpoint Agent / eBPF Sensor]
    end

    subgraph Control[Control Plane]
        IAM[Identity Provider]
        PDP[Policy Decision Point]
        PIP[Policy Information Point]
        Orchestrator[Automation Orchestrator]
    end

    subgraph Analytics[Detection & Intelligence]
        Telemetry[Telemetry Collector]
        Behavioral[Behavioral Malware Engine]
        Intel[Threat Intelligence Broker]
        Correlator[Correlation Engine]
    end

    subgraph Evidence[Evidence & Compliance]
        Vault[Evidence Vault]
        Chain[Blockchain Anchoring Service]
        Audit[Audit / Forensics UI]
    end

    Agent --> Telemetry
    Telemetry --> Behavioral
    Behavioral --> Correlator
    Correlator --> Intel
    Correlator --> Orchestrator
    ZTNA --> IAM
    ZTNA --> PDP
    PDP --> PIP
    Orchestrator --> Vault
    Vault --> Chain
    Audit --> Vault
```

## 3. Component Diagram

```mermaid
flowchart LR
    subgraph App[Application Services]
        AccessSvc[Access Evaluation Service]
        RiskSvc[Risk Scoring Service]
        DetectionSvc[Behavioral Detection Service]
        IntelSvc[Threat Intel Service]
        EvidenceSvc[Evidence Service]
    end

    subgraph Domain[Domain Layer]
        Policies[Policy Rules]
        Entities[Entities / Value Objects]
        UseCases[Use Cases]
    end

    subgraph Infra[Infrastructure Adapters]
        IAMAdapter[IAM Adapter]
        EDRAdapter[EDR / NDR Adapter]
        OPAAdapter[OPA / Policy Adapter]
        LedgerAdapter[Ledger Adapter]
        StorageAdapter[Storage Adapter]
    end

    AccessSvc --> Policies
    RiskSvc --> Entities
    DetectionSvc --> UseCases
    IntelSvc --> Entities
    EvidenceSvc --> UseCases

    AccessSvc --> IAMAdapter
    AccessSvc --> OPAAdapter
    DetectionSvc --> EDRAdapter
    IntelSvc --> StorageAdapter
    EvidenceSvc --> LedgerAdapter
```

## Notes

- The control plane should be stateless and horizontally scalable.
- The evidence plane should be append-only and isolated from direct user access.
- The detection plane should support event replay and forensic investigation.
