-- Sample queries (spend, on-time, payment speed, price trend, score)
SELECT v.vendor_name, SUM(p.total_amount) AS spend
FROM purchase_orders p
JOIN vendors v ON p.vendor_id = v.vendor_id
WHERE p.po_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY v.vendor_name
ORDER BY spend DESC
LIMIT 20;

SELECT v.vendor_name,
  COUNT(*) FILTER (WHERE d.delay_days <= 0)::float / NULLIF(COUNT(*),0) AS on_time_rate,
  AVG(d.delay_days) AS avg_delay_days
FROM deliveries d
JOIN purchase_orders p ON d.po_id = p.po_id
JOIN vendors v ON p.vendor_id = v.vendor_id
GROUP BY v.vendor_name
ORDER BY on_time_rate DESC NULLS LAST;

SELECT v.vendor_name,
  AVG(EXTRACT(DAY FROM (paid_date - invoice_date))) AS avg_payment_days,
  COUNT(*) AS invoices_count
FROM invoices i
JOIN purchase_orders p ON i.po_id = p.po_id
JOIN vendors v ON p.vendor_id = v.vendor_id
WHERE i.paid_date IS NOT NULL
GROUP BY v.vendor_name
ORDER BY avg_payment_days;
