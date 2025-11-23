import { Sparkles, TrendingUp, AlertCircle, Award, Loader } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useState, useEffect } from "react";
import type { Bank } from "./BankSelector";
import type { Criterion } from "./CriteriaSelector";

interface Insight {
  type: "best" | "advantage" | "improvement";
  title: string;
  description: string;
}

interface AIAnalysis {
  competitor: string;
  product: string;
  criterion: string;
  value: string;
  confidence_score?: number;
  analysis_type: string;
}

interface AIInsightsProps {
  banks?: Bank[];
  criteria?: Criterion[];
  product?: string;
  insights?: Insight[];
}

// Mock insights for demo - используется если нет данных с backend
const DEFAULT_INSIGHTS: Insight[] = [
  {
    type: "best",
    title: "Лучшее предложение на рынке",
    description:
      "По результатам анализа, Альфа-Банк демонстрирует лучшие условия по кредитным картам с кэшбэком до 10% и беспроцентным периодом 100 дней. Однако Сбербанк лидирует по доступности отделений и качеству мобильного приложения.",
  },
  {
    type: "advantage",
    title: "Преимущества Сбербанка",
    description:
      "Сбербанк превосходит конкурентов по следующим критериям: наличие программы лояльности СберСпасибо (до 30% кэшбэка), развитая инфраструктура (более 14 000 отделений), бесплатные СМС-уведомления для всех категорий клиентов, процент на остаток до 3.5% годовых.",
  },
  {
    type: "improvement",
    title: "Зоны для улучшения",
    description:
      "Рекомендуется пересмотреть следующие аспекты: снизить стоимость обслуживания премиальных карт (сейчас выше на 15-20% чем у конкурентов), увеличить лимиты снятия наличных в банкоматах других банков без комиссии, внедрить расширенные возможности бесконтактных платежей через Apple Pay/Google Pay.",
  },
];

export const AIInsights = ({ 
  banks = [], 
  criteria = [], 
  product = "deposits",
  insights = DEFAULT_INSIGHTS 
}: AIInsightsProps) => {
  const [aiData, setAiData] = useState<AIAnalysis[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (banks.length === 0 || criteria.length === 0) {
      return;
    }

    fetchAIInsights();
  }, [banks, criteria, product]);

  const fetchAIInsights = async () => {
    try {
      setLoading(true);
      setError(null);

      const bankIds = banks.map(b => b.id).join(',');
      const criterionIds = criteria.map(c => c.id).join(',');

      const response = await fetch(
        `/api/ai/insights/?banks=${bankIds}&product=${product}&criterion=${criterionIds}`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch AI insights');
      }

      const data = await response.json();
      setAiData(data.insights || []);
    } catch (err) {
      console.error('Error fetching AI insights:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const formatInsights = (): Insight[] => {
    if (!aiData || aiData.length === 0) {
      return DEFAULT_INSIGHTS;
    }

    // Группируем по типам анализа
    const facts = aiData.filter(a => a.analysis_type === 'facts');
    const comparisons = aiData.filter(a => a.analysis_type === 'comparison');
    const recommendations = aiData.filter(a => a.analysis_type === 'recommendation');

    const insights: Insight[] = [];

    // Добавляем факты
    if (facts.length > 0) {
      insights.push({
        type: 'best',
        title: `Фактические данные по ${product}`,
        description: facts.map(f => `• ${f.competitor}: ${f.value}`).join('\n')
      });
    }

    // Добавляем сравнения
    if (comparisons.length > 0) {
      insights.push({
        type: 'advantage',
        title: 'Сравнительный анализ',
        description: comparisons.map(c => `• ${c.competitor}: ${c.value}`).join('\n')
      });
    }

    // Добавляем рекомендации
    if (recommendations.length > 0) {
      insights.push({
        type: 'improvement',
        title: 'Рекомендации для улучшения',
        description: recommendations.map(r => `• ${r.value}`).join('\n')
      });
    }

    return insights.length > 0 ? insights : DEFAULT_INSIGHTS;
  };

  const getIcon = (type: string) => {
    switch (type) {
      case "best":
        return <Award className="w-5 h-5 text-warning" />;
      case "advantage":
        return <TrendingUp className="w-5 h-5 text-success" />;
      case "improvement":
        return <AlertCircle className="w-5 h-5 text-secondary" />;
      default:
        return <Sparkles className="w-5 h-5 text-primary" />;
    }
  };

  const getBadgeVariant = (type: string) => {
    switch (type) {
      case "best":
        return "default";
      case "advantage":
        return "secondary";
      case "improvement":
        return "outline";
      default:
        return "default";
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center gap-2 p-6">
        <Loader className="w-5 h-5 animate-spin text-primary" />
        <span className="text-sm text-muted-foreground">Загрузка AI анализа...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Card className="border-red-200 bg-red-50 dark:bg-red-950/20">
        <CardContent className="pt-6">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4 animate-fade-in" style={{ animationDelay: "0.2s" }}>
      <div className="flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-primary" />
        <h2 className="text-xl font-semibold text-foreground">
          AI-анализ и рекомендации
        </h2>
        <Badge variant="secondary" className="ml-auto bg-primary/10 text-primary">
          {aiData.length > 0 ? 'Из данных' : 'Demo'}
        </Badge>
      </div>

      {aiData.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-3">
          {formatInsights().map((insight, index) => (
            <Card
              key={index}
              className="transition-all hover:shadow-md animate-scale-in border-l-4"
              style={{
                animationDelay: `${0.1 * (index + 1)}s`,
                borderLeftColor:
                  insight.type === "best"
                    ? "hsl(var(--warning))"
                    : insight.type === "advantage"
                    ? "hsl(var(--success))"
                    : "hsl(var(--secondary))",
              }}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 mt-1">{getIcon(insight.type)}</div>
                  <div className="space-y-1 flex-1">
                    <CardTitle className="text-base leading-tight">
                      {insight.title}
                    </CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                  {insight.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-3">
          {DEFAULT_INSIGHTS.map((insight, index) => (
            <Card
              key={index}
              className="transition-all hover:shadow-md animate-scale-in border-l-4"
              style={{
                animationDelay: `${0.1 * (index + 1)}s`,
                borderLeftColor:
                  insight.type === "best"
                    ? "hsl(var(--warning))"
                    : insight.type === "advantage"
                    ? "hsl(var(--success))"
                    : "hsl(var(--secondary))",
              }}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 mt-1">{getIcon(insight.type)}</div>
                  <div className="space-y-1 flex-1">
                    <CardTitle className="text-base leading-tight">
                      {insight.title}
                    </CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {insight.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Card className="border-primary/30 bg-primary/5">
        <CardContent className="pt-6">
          <div className="flex gap-3">
            <Sparkles className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
            <div className="space-y-1">
              <p className="text-sm font-medium text-foreground">
                Рекомендация системы
              </p>
              <p className="text-sm text-muted-foreground">
                На основе анализа 9 критериев по 3 банкам, Сбербанк демонстрирует сильные
                позиции в 6 категориях. Для улучшения конкурентоспособности рекомендуется
                сфокусироваться на оптимизации тарифной сетки и расширении льгот для
                премиальных клиентов.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
