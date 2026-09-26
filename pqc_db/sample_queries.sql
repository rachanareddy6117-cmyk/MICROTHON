-- Most vulnerable algorithms in the controlled knowledge base
SELECT a.name, ck.quantum_risk, ck.classical_risk
FROM crypto_knowledge ck
JOIN algorithms a ON LOWER(a.name) = LOWER(ck.algorithm)
ORDER BY ck.quantum_risk DESC;

-- Open findings by severity
SELECT severity, COUNT(*) AS finding_count
FROM findings
WHERE status <> 'resolved'
GROUP BY severity
ORDER BY CASE severity
    WHEN 'critical' THEN 1
    WHEN 'high' THEN 2
    WHEN 'medium' THEN 3
    ELSE 4
END;

-- Active firewall policy decisions
SELECT service, tls_version, cipher, decision, reason, risk
FROM firewall_events
WHERE timestamp >= NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;

-- Dependencies for a repository
SELECT repository_id, package_name, library_name, protocol, dependency_type
FROM dependencies
WHERE repository_id = :repository_id;

-- Migration progress on a repository
SELECT repository_id, asset_count, algorithm_summary, risk_summary, migration_progress
FROM crypto_snapshots
WHERE repository_id = :repository_id
ORDER BY timestamp DESC;
