# Clean Architecture Module Map

## Architectural principle

The system should keep business rules independent from frameworks, databases, and external services. Dependencies should point inward toward the domain layer.

## Layered structure

### 1. Domain layer

Purpose: define entities, value objects, domain rules, and interfaces.

Modules:

- IdentityDomain
  - User, Device, Asset, Session
- PolicyDomain
  - AccessPolicy, PolicyRule, DecisionContext, AccessDecision
- DetectionDomain
  - DetectionCase, BehavioralSignal, RiskScore, ContainmentAction
- IntelligenceDomain
  - Indicator, ThreatFeed, Confidence, PrivacyContext
- EvidenceDomain
  - EvidenceRecord, ChainAnchor, AuditEvent, Investigation

### 2. Application layer

Purpose: orchestrate use cases without depending on infrastructure details.

Modules:

- AccessUseCases
  - EvaluateAccess
  - RevokeSession
  - RequestJustInTimeAccess
- DetectionUseCases
  - ProcessTelemetry
  - ScoreBehavior
  - TriggerContainment
- IntelligenceUseCases
  - QueryIndicators
  - ShareIndicatorSafely
  - FusionAndScoring
- EvidenceUseCases
  - CreateEvidenceBundle
  - AnchorEvidence
  - VerifyChainOfCustody

### 3. Interface layer

Purpose: expose capabilities through APIs, CLI, and internal events.

Modules:

- REST API handlers
- Webhooks and event subscribers
- Admin console adapters
- Integration connectors for SIEM and SOAR

### 4. Infrastructure layer

Purpose: implement interfaces with concrete services and storage.

Modules:

- IAMAdapter
- OPAAdapter
- EDRAdapter
- TelemetryStoreAdapter
- EventBusAdapter
- LedgerAdapter
- ObjectStorageAdapter
- SecretStoreAdapter

## Dependency rules

- Outer layers may depend on inner layers.
- Inner layers define interfaces that outer layers implement.
- Domain logic must not import framework-specific packages.
- Infrastructure concerns must be isolated behind interfaces.

## Suggested package boundaries

```text
src/
  domain/
    identity/
    policy/
    detection/
    intelligence/
    evidence/
  application/
    access/
    detection/
    intelligence/
    evidence/
  interfaces/
    api/
    events/
  infrastructure/
    iam/
    telemetry/
    policy/
    ledger/
    storage/
    messaging/
```

## Operational advantages

- Easier auditing and unit testing
- Safer replacement of providers and storage backends
- Clear ownership of security policies and evidence flows
- Better support for regulatory review and incident response
