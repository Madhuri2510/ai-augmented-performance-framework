#!/bin/bash

echo "🚀 Running JMeter Test..."

jmeter -n \
-t jmeter/test-plans/booking_test.jmx \
-l results/raw/results.jtl \
-e -o results/html

echo "✅ Test Completed"