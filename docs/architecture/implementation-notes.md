# Implementation Notes

## Suggested services

- Access Control Service
- Behavioral Detection Service
- Threat Intelligence Broker
- Evidence Anchoring Service
- Investigation Orchestration Service

## Recommended controls

- Enforce mTLS and service identity with SPIFFE/SPIRE or equivalent.
- Use OPA for policy-as-code.
- Use Kafka, NATS, or Azure Service Bus for event streaming.
- Use a permissioned ledger such as Hyperledger Fabric or Quorum.
- Use object storage with WORM semantics for evidence retention.

## Data handling guidance

- Minimize personal data in telemetry and indicators.
- Use tokenization or secure matching for shared intel.
- Maintain chain-of-custody metadata for each evidence record.
- Separate raw evidence from derived analysis artifacts.

## Rollout phases

1. Foundation: identity, MFA, device posture, and policy engine.
2. Detection: telemetry ingestion, detection workflows, and containment.
3. Intelligence: privacy-preserving sharing and correlation.
4. Evidence: immutable anchoring and forensics operations.
