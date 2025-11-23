import { useState, useEffect, useCallback } from "react";
import type { Bank } from "@/components/BankSelector";
import type { Criterion } from "@/components/CriteriaSelector";

interface ComparisonData {
  [bankId: string]: {
    [criterionId: string]: boolean;
  };
}

interface ApiResponse {
  date: string;
  sources: Array<{ id?: number; name: string; url: string }>;
  data: ComparisonData;
  confidence?: { [key: string]: number };
  note?: string;
  product?: string;
  is_mock?: boolean;
}

interface UseComparisonDataOptions {
  enabled?: boolean;
  refetchInterval?: number;
}

export const useComparisonData = (
  banks: Bank[],
  criteria: Criterion[],
  product: string,
  options: UseComparisonDataOptions = {}
) => {
  const { enabled = true, refetchInterval = 0 } = options;

  const [data, setData] = useState<ComparisonData>({});
  const [sources, setSources] = useState<Array<{ id?: number; name: string; url: string }>>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMock, setIsMock] = useState(false);
  const [lastFetchTime, setLastFetchTime] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<{ [key: string]: number }>({});

  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

  const fetchData = useCallback(async () => {
    if (!enabled || banks.length === 0 || criteria.length === 0) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const bankIds = banks.map((b) => b.id).join(",");
      const criteriaIds = criteria.map((c) => c.id).join(",");

      const url = new URL(`${API_BASE_URL}/compare/`);
      url.searchParams.append("banks", bankIds);
      url.searchParams.append("criteria", criteriaIds);
      url.searchParams.append("product", product);

      const response = await fetch(url.toString(), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const responseData: ApiResponse = await response.json();

      setData(responseData.data);
      setSources(responseData.sources);
      setIsMock(responseData.is_mock || false);
      setLastFetchTime(responseData.date);
      if (responseData.confidence) {
        setConfidence(responseData.confidence);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Unknown error";
      setError(errorMessage);
      console.error("Error fetching comparison data:", err);
      
      // Fallback to mock data if API fails
      setIsMock(true);
    } finally {
      setLoading(false);
    }
  }, [banks, criteria, product, enabled, API_BASE_URL]);

  // Initial fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Refetch interval
  useEffect(() => {
    if (refetchInterval <= 0) return;

    const interval = setInterval(fetchData, refetchInterval);
    return () => clearInterval(interval);
  }, [fetchData, refetchInterval]);

  return {
    data,
    sources,
    loading,
    error,
    isMock,
    lastFetchTime,
    confidence,
    refetch: fetchData,
  };
};
