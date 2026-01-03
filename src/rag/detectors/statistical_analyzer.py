#!/usr/bin/env python3
"""
Statistical Analysis Engine with Standard Deviation Calculations
Performs comprehensive statistical analysis on detection metrics
"""

import statistics
import json
from typing import List, Dict
from datetime import datetime

class StatisticalAnalyzer:
    """Advanced statistical analysis for RAG-Shield metrics"""
    
    def __init__(self):
        self.metrics_buffer = {
            "drift_scores": [],
            "detection_latencies": [],
            "similarity_scores": [],
            "vulnerability_scores": []
        }
    
    def add_metric(self, metric_type: str, value: float):
        """Add a metric value for analysis"""
        if metric_type in self.metrics_buffer:
            self.metrics_buffer[metric_type].append(value)
    
    def calculate_statistics(self, data: List[float]) -> Dict:
        """Calculate comprehensive statistics"""
        if not data or len(data) == 0:
            return {"error": "No data"}
        
        sorted_data = sorted(data)
        n = len(data)
        
        stats = {
            "count": n,
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "mode": statistics.mode(data) if n > 1 else data[0],
            "stdev": statistics.stdev(data) if n > 1 else 0.0,
            "variance": statistics.variance(data) if n > 1 else 0.0,
            "min": min(data),
            "max": max(data),
            "range": max(data) - min(data),
        }
        
        # Percentiles
        stats["p25"] = self._percentile(sorted_data, 0.25)
        stats["p50"] = self._percentile(sorted_data, 0.50)  # Median
        stats["p75"] = self._percentile(sorted_data, 0.75)
        stats["p90"] = self._percentile(sorted_data, 0.90)
        stats["p95"] = self._percentile(sorted_data, 0.95)
        stats["p99"] = self._percentile(sorted_data, 0.99)
        
        # Inter-quartile range
        stats["iqr"] = stats["p75"] - stats["p25"]
        
        # Coefficient of variation (CV)
        if stats["mean"] != 0:
            stats["cv"] = (stats["stdev"] / stats["mean"]) * 100
        else:
            stats["cv"] = 0.0
        
        # Z-scores for outlier detection
        if stats["stdev"] > 0:
            stats["outliers"] = self._detect_outliers(data, stats["mean"], stats["stdev"])
        else:
            stats["outliers"] = []
        
        return stats
    
    def _percentile(self, sorted_data: List[float], p: float) -> float:
        """Calculate percentile"""
        if not sorted_data:
            return 0.0
        k = (len(sorted_data) - 1) * p
        f = int(k)
        c = f + 1
        if c >= len(sorted_data):
            return sorted_data[-1]
        d0 = sorted_data[f] * (c - k)
        d1 = sorted_data[c] * (k - f)
        return d0 + d1
    
    def _detect_outliers(self, data: List[float], mean: float, stdev: float) -> List[Dict]:
        """Detect outliers using z-score method (|z| > 3)"""
        outliers = []
        for value in data:
            z_score = (value - mean) / stdev if stdev > 0 else 0
            if abs(z_score) > 3:
                outliers.append({"value": value, "z_score": z_score})
        return outliers
    
    def generate_full_report(self) -> Dict:
        """Generate comprehensive statistical report"""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {}
        }
        
        for metric_type, data in self.metrics_buffer.items():
            if data:
                report["metrics"][metric_type] = self.calculate_statistics(data)
        
        return report
    
    def compare_distributions(self, data1: List[float], data2: List[float], 
                            label1: str = "Distribution 1", 
                            label2: str = "Distribution 2") -> Dict:
        """Compare two distributions statistically"""
        stats1 = self.calculate_statistics(data1)
        stats2 = self.calculate_statistics(data2)
        
        comparison = {
            "distributions": {
                label1: stats1,
                label2: stats2
            },
            "differences": {
                "mean_diff": stats1["mean"] - stats2["mean"],
                "median_diff": stats1["median"] - stats2["median"],
                "stdev_diff": stats1["stdev"] - stats2["stdev"],
                "range_diff": stats1["range"] - stats2["range"]
            }
        }
        
        # Effect size (Cohen's d)
        pooled_stdev = ((stats1["stdev"]**2 + stats2["stdev"]**2) / 2) ** 0.5
        if pooled_stdev > 0:
            comparison["cohens_d"] = (stats1["mean"] - stats2["mean"]) / pooled_stdev
        else:
            comparison["cohens_d"] = 0.0
        
        return comparison

# Example usage
if __name__ == "__main__":
    analyzer = StatisticalAnalyzer()
    
    # Sample detection latencies
    latencies = [45.2, 38.7, 52.1, 41.3, 39.8, 48.5, 42.7, 36.9, 44.1, 40.5]
    for lat in latencies:
        analyzer.add_metric("detection_latencies", lat)
    
    # Generate report
    report = analyzer.generate_full_report()
    print(json.dumps(report, indent=2))
